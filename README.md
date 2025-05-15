#Geolocation IP tracker

This is a python script that reads a list of IP address, fetches their geographical locations using the IP-API, clusters them using K-Means, and displays them on an interactive map.

##Features 
- IP geolocation using [ip-api.com](http://ip-api.com)
- Clustering of locations using KMeans (scikit-learn)
- Interactive map generation with Folium

##Usage
1. Add IP addresses (one per line) to `ips.txt`
2. Run the script:


#how to run
```bash
python geolocation_tracker.py