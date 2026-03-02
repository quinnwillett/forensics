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



#Loop through each file in the input directory
for filename in os.listdir(args.input):
    print(f"Processing {filename}")
