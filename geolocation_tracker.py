# A geolocation tracker that fetches the user's geolocation using IP addresses and displays it on a map

import requests
import folium
from sklearn.cluster import KMeans

# Read the IPs from a file
def read_ip_list(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except IOError as e:
        print(f"Error reading file '{filename}': {e}")
        return []

# Get geolocation data for an IP address  
def get_geo_data(ip):
    print(f"Getting location for IP: {ip}")
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        response.raise_for_status()  # Raises HTTPError for 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error for IP {ip}: {e}")
        return {"status": "fail"}

def main():
    ip_list = read_ip_list("ips.txt")
    if not ip_list:
        print("No IPs to process.")
        return

    geo_data_list = []
    coords = []

    for ip in ip_list:
        data = get_geo_data(ip)
        if data.get("status") == "success":
            try:
                lat = data["lat"]
                lon = data["lon"]
                coords.append([lat, lon])
                geo_data_list.append({
                    "ip": ip,
                    "lat": lat,
                    "lon": lon,
                    "city": data.get("city", "Unknown"),
                    "country": data.get("country", "Unknown")
                })
                print(f"Fetched data for {ip}: {data['city']}, {data['country']}")
            except KeyError as e:
                print(f"Missing data for IP {ip}: {e}")
        else:
            print(f"Failed to get data for IP: {ip}")

    if not coords:
        print("No valid IP locations found.")
        return

    try:
        n_clusters = min(5, len(coords))
        kmeans = KMeans(n_clusters=n_clusters, n_init=10)
        kmeans.fit(coords)
        labels = kmeans.labels_
    except Exception as e:
        print(f"Clustering failed: {e}")
        return

    cluster_colors = ['blue', 'red', 'green', 'orange', 'purple']
    m = folium.Map(location=[0, 0], zoom_start=2)

    for i, data in enumerate(geo_data_list):
        try:
            folium.Marker(
                location=[data["lat"], data["lon"]],
                popup=f"{data['ip']} - {data['city']}, {data['country']} (cluster {labels[i]})",
                icon=folium.Icon(color=cluster_colors[labels[i] % len(cluster_colors)])
            ).add_to(m)
        except Exception as e:
            print(f"Error adding marker for IP {data['ip']}: {e}")

    try:
        m.save("clustered_ips_map.html")
        print("Map saved as clustered_ips_map.html")
    except Exception as e:
        print(f"Failed to save map: {e}")

if __name__ == "__main__":
    main()
