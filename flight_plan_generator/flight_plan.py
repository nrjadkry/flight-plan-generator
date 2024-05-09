import os
import zipfile
import xml.dom.minidom
from .utils import (
    dict_to_xml,
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

    def generate_wpml(self):

        # stringify the coordinate points
        coordinates = [f"{x[0]}, {x[1]}" for x in self.coordinate_points]

        final_kml_json = {
            "Document": {
                "missionConfig": get_mission_config_json(),
                "Folder": get_folder_json(coordinates),
            }
        }
        return self.generate_wpml_base(final_kml_json)


def write_wpml_content(wpml_content):
    with open("wpmz/waylines.wpml", "w") as f:
        f.write(wpml_content)


def zip_directory(directory_path, zip_path):
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                zipf.write(
                    os.path.join(root, file),
                    os.path.relpath(
                        os.path.join(root, file), os.path.join(directory_path, "..")
                    ),
                )


def create_zip_file(wpml_content, template_kml_content):
    # Create the wpmz folder if it doesn't exist
    os.makedirs("wpmz", exist_ok=True)

    # Write wpml_content to waylines.wpml inside the wpmz folder
    write_wpml_content(wpml_content)

    # Write template.kml content to template.kml inside the wpmz folder
    with open("wpmz/template.kml", "w") as f:
        f.write(template_kml_content)

    # Create a Zip file containing the contents of the wpmz folder directly
    zip_directory("wpmz", "output.kmz")


def get_flight_plan(
    aoi: str,
    distance_between_lines: int,
    altitude: int,
    speed: int,
    gimble_angle: int,
):
    points = generate_waypoints_within_polygon(aoi, distance_between_lines)

    wpml_generator = WPMLGenerator(points)
    wpml_content = wpml_generator.generate_wpml()

    # Read content of template.kml
    with open("flight_plan_generator/data/template.kml", "r") as f:
        template_kml_content = f.read()

    # Create the Zip file
    create_zip_file(wpml_content, template_kml_content)
