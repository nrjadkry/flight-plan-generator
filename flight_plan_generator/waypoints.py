import simplekml
import geopy
import geojson
import json
from shapely.geometry import Polygon, Point, shape, LineString


def generate_waypoints_within_polygon(polygon, home_point, distance_between_lines):
    minx, miny, maxx, maxy = polygon.bounds
    waypoints = []

    # Add home point as the starting waypoint
    waypoints.append(home_point)

    # Generate waypoints within the polygon
    y = miny
    row_count = 0

    # Extend the loop by one iteration so that the point will be outside the polygon
    while y <= maxy + distance_between_lines:
        x = minx
        x_row_waypoints = []
        while x <= maxx + distance_between_lines:
            x_row_waypoints.append((y, x))  # Coordinates are reversed for Folium
            x += distance_between_lines
        y += distance_between_lines

        if x_row_waypoints:
            if row_count % 2 == 0:
                waypoints.append(x_row_waypoints[0])
                if len(x_row_waypoints) > 1:
                    waypoints.append(x_row_waypoints[-1])  # Append last point
            else:
                if len(x_row_waypoints) > 1:
                    waypoints.append(x_row_waypoints[-1])  # Append last point
                waypoints.append(x_row_waypoints[0])

        row_count += 1

    # Add home point as the last waypoint
    waypoints.append(home_point)

    return waypoints
