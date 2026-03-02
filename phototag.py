# Assignment 3: Photo Location Tags
# Quinn Willett

# Import required packages
import folium
import subprocess
import argparse
import os

# Parse command line arguments
parser = argparse.ArgumentParser(description='Photo Location Tags')
parser.add_argument('-i','--input', help='Directory containing photos', required=True)
args = parser.parse_args()


# Create a map centered on the average location of the photos
m = folium.Map(location=[0, 0], zoom_start=2)

# Create a list to store the locations of the photos
locations = []



#Loop through each file in the input directory
for filename in os.listdir(args.input):
    print(f"Processing {filename}")
    # Check if the file is a photo (you can add more extensions if needed)
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        # Get the full path of the photo
        photo_path = os.path.join(args.input, filename)
        
        # Use exiftool to extract GPS data from the photo
        try:
            result = subprocess.run(['exiftool', '-gpslatitude', '-gpslongitude', '-n', photo_path], 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout
            
            # Parse the output to get latitude and longitude
            lat = None
            lon = None
            for line in output.splitlines():
                if 'GPS Latitude' in line:
                    lat = float(line.split(':')[1].strip())
                    print (f"Found GPS Latitude: {lat}")
                elif 'GPS Longitude' in line:
                    lon = float(line.split(':')[1].strip())
                    print (f"Found GPS Longitude: {lon}")
            
            # If both latitude and longitude are found, add a marker to the map
            if lat is not None and lon is not None:
                folium.Marker(location=[lat, lon], popup=filename).add_to(m)
                locations.append((lat, lon))
        except Exception as e:
            print(f"Error processing {filename}: {e}")
# If we have locations, center the map on the average location
if locations:
    avg_lat = sum(lat for lat, lon in locations) / len(locations)
    avg_lon = sum(lon for lat, lon in locations) / len(locations)
    m.location = [avg_lat, avg_lon]
    m.zoom_start = 10
# Save the map to an HTML file
m.save('photo_locations.html')
print("Map saved to photo_locations.html")

