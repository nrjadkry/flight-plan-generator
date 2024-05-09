import xml.dom.minidom
from .utils import (
    dict_to_xml,
    generate_dynamic_placemarks,
    get_mission_config_json,
    get_folder_json,
)
from .waypoints import generate_waypoints_within_polygon


class WPMLGenerator:
    def __init__(self, coordinate_points):
        self.coordinate_points = coordinate_points

    def generate_wpml_base(self, final_kml_json):
        # Create XML document
        doc = xml.dom.minidom.Document()

        # Create root element <kml> with namespace declaration
        kml = doc.createElementNS("http://www.opengis.net/kml/2.2", "kml")
        kml.setAttribute("xmlns", "http://www.opengis.net/kml/2.2")
        kml.setAttribute("xmlns:wpml", "http://www.dji.com/wpmz/1.0.2")
        doc.appendChild(kml)

        dict_to_xml(doc, kml, final_kml_json)

        return doc.toprettyxml()

    def generate_wpml(self, mission_config_json, folder_json):
        final_kml_json = {
            "Document": {"missionConfig": mission_config_json, "Folder": folder_json}
        }
        return self.generate_wpml_base(final_kml_json)


def get_flight_plan(
    aoi: str,
    distance_between_lines: int,
    altitude: int,
    speed: int,
    gimble_angle: int,
):
    points = generate_waypoints_within_polygon(aoi, distance_between_lines)

    # stringify the coordinate points
    coordinate_points = [f"{x[0]}, {x[1]}" for x in points]

    wpml_generator = WPMLGenerator(coordinate_points)
    wpml_content = wpml_generator.generate_wpml(
        get_mission_config_json(), get_folder_json(coordinate_points)
    )
    print(wpml_content)
