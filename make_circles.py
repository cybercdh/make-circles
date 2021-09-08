#!/usr/bin/env python3

import simplekml
import os.path
import sys
import pandas as pd
from argparse import ArgumentParser
from math import asin,cos,pi,sin

kml = simplekml.Kml()

# coordinate logic taken from
# https://stackoverflow.com/questions/877524/calculating-coordinates-given-a-bearing-and-a-distance

rEarth = 6371.01 # Earth's average radius in km
epsilon = 0.000001 # threshold for floating-point equality

def deg2rad(angle):
    return angle*pi/180

def rad2deg(angle):
    return angle*180/pi

def pointRadialDistance(lat1, lon1, bearing, distance):
    """
    Return final coordinates (lat2,lon2) [in degrees] given initial coordinates
    (lat1,lon1) [in degrees] and a bearing [in degrees] and distance [in km]
    """
    rlat1 = deg2rad(lat1)
    rlon1 = deg2rad(lon1)
    rbearing = deg2rad(bearing)
    rdistance = distance / rEarth # normalize linear distance to radian angle

    rlat = asin( sin(rlat1) * cos(rdistance) + cos(rlat1) * sin(rdistance) * cos(rbearing) )

    if cos(rlat) == 0 or abs(cos(rlat)) < epsilon: # Endpoint a pole
        rlon=rlon1
    else:
        rlon = ( (rlon1 - asin( sin(rbearing)* sin(rdistance) / cos(rlat) ) + pi ) % (2*pi) ) - pi

    lat = rad2deg(rlat)
    lon = rad2deg(rlon)

    return (lon,lat)

def ProcessPoint(lat, lon, radius, outfile):

	# plot a point within the circle
	pnt = kml.newpoint()
	pnt.coords = [(lon, lat)]

	circle_coords = []

	# loop through each degree in a circle and plot a point radius distance away
	for deg in range(360,-1,-1):
		circle_coords.append(pointRadialDistance(lat,lon,deg,radius))

	# generate linestring for the circle
	ls = kml.newlinestring(description=str(radius) + " radius")
	ls.coords=circle_coords
	ls.style.linestyle.color = simplekml.Color.red 
	ls.style.linestyle.width = 5 # px

	kml.save(outfile)

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle

def main(argv):

	parser = ArgumentParser(description="plot radius circles around points on a map")
	parser.add_argument("-i", dest="inputfile", required=True, help="input csv file", metavar="FILE", type=lambda x: is_valid_file(parser, x))
	parser.add_argument("-o", dest="outputfile", required=False, default="circles.kml", help="output kml file", metavar="FILE")
	args = parser.parse_args()

	df = pd.read_csv(args.inputfile)

	for index, row in df.iterrows():
		ProcessPoint(row['latitude'], row['longitude'], row['accuracy_radius'], args.outputfile)

if __name__ == "__main__":
	main(sys.argv[1:])


