import copy

placemark_data = {
    "Point": {"coordinates": "85.32847797583463,27.73034357804735"},
    "index": "0",  # unique for every placemark
    "executeHeight": "60",  # Height (float)
    "waypointSpeed": "2.5",  # Speed (in m/s) (required if wpml:useGlobalSpeed in template.kml is 0)
    "waypointHeadingParam": {
        "waypointHeadingMode": "smoothTransition",
        "waypointHeadingAngle": "180",
        "waypointPoiPoint": "0.000000,0.000000,0.000000",
        "waypointHeadingAngleEnable": "1",
        "waypointHeadingPathMode": "followBadArc",
    },
    "waypointTurnParam": {
        "waypointTurnMode": "toPointAndStopWithContinuityCurvature",
        "waypointTurnDampingDist": "0",
    },
    "useStraightLine": "0",  # 1 for straight line, 0 for spiral line (this is in template.kml too)
    "actionGroup": {
        "actionGroupId": "1",
        "actionGroupStartIndex": "0",  # start index for this point (placemark_index)
        "actionGroupEndIndex": "0",  # end index for this point  (placemark_index)
        "actionGroupMode": "parallel",
        "actionTrigger": {"actionTriggerType": "reachPoint"},
        "action": {
            "actionId": "1",
            "actionActuatorFunc": "gimbalRotate",
            "actionActuatorFuncParam": {
                "gimbalHeadingYawBase": "aircraft",
                "gimbalRotateMode": "absoluteAngle",
                "gimbalPitchRotateEnable": "1",
                "gimbalPitchRotateAngle": "-81",
                "gimbalRollRotateEnable": "0",
                "gimbalRollRotateAngle": "0",
                "gimbalYawRotateEnable": "0",
                "gimbalYawRotateAngle": "0",
                "gimbalRotateTimeEnable": "0",
                "gimbalRotateTime": "0",
                "payloadPositionIndex": "0",
            },
        },
    },
}


def dict_to_xml(doc, parent_element, data):
    for key, value in data.items():
        create_xml_element(doc, parent_element, key, value)


def create_xml_element(doc, parent_element, key, value):
    if key in ["Document", "Folder", "Placemark", "Point", "coordinates"]:
        element = doc.createElement(key)
    else:
        element = doc.createElementNS("http://www.dji.com/wpmz/1.0.2", f"wpml:{key}")
    parent_element.appendChild(element)
    if isinstance(value, dict):
        dict_to_xml(doc, element, value)
    elif isinstance(value, list):
        for sub_value in value:
            create_xml_element(doc, element, key, sub_value)
    else:
        print("Value =", value)
        element.appendChild(doc.createTextNode(value))


def generate_dynamic_placemarks(coordinate_points):
    placemark_coordinate_points = []

    for index, coord in enumerate(coordinate_points):
        placemark = copy.deepcopy(placemark_data)  # Perform a deep copy
        placemark["Point"]["coordinates"] = coord
        placemark["index"] = str(index)

        # TODO: properly handle everything inside <wpml:actionGroup>
        if isinstance(placemark["actionGroup"], list):
            for x in placemark["actionGroup"]:
                x["actionGroupStartIndex"] = str(index)
                x["actionGroupEndIndex"] = str(index)
        else:
            placemark["actionGroup"]["actionGroupStartIndex"] = str(index)
            placemark["actionGroup"]["actionGroupEndIndex"] = str(index)

        placemark_coordinate_points.append(placemark)
    return placemark_coordinate_points


def get_folder_json(points):
    return {
        "Folder": {
            "templateId": "0",
            "executeHeightMode": "relativeToStartPoint",
            "waylineId": "0",
            "distance": "0",
            "duration": "0",
            "autoFlightSpeed": "2.5",
            "Placemark": generate_dynamic_placemarks(points),
        }
    }


def get_mission_config_json():
    return {
        "missionConfig": {
            "flyToWaylineMode": "safely",
            "finishAction": "goHome",  # goHome on Mission Complete
            "exitOnRCLost": "executeLostAction",
            "executeRCLostAction": "goBack",
            "globalTransitionalSpeed": "2.5",
            "droneInfo": {  # Drone Types (Drone Info)
                "droneEnumValue": "68",
                "droneSubEnumValue": "0",
            },
        }
    }
