from flask import Blueprint, request, jsonify
from firebase_admin import firestore

db = firestore.client()
intersections_ref = db.collection('intersections')

intersectionsAPI = Blueprint('intersectionsAPI', __name__)



@intersectionsAPI.route('/intersections', methods=['GET'])
def get_all_intersections():
    try:
        all_docs = intersections_ref.stream()
        intersections = {}
        for doc in all_docs:
            intersections[doc.id] = doc.to_dict()
        return jsonify(intersections), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@intersectionsAPI.route('/intersections/geo-json', methods=['GET'])
def get_intersection():
    try:
        all_docs = intersections_ref.stream()
        intersections = {
        }
        geoJson = {
                    "type":"FeatureCollection",
                    "features":[],
                    "image_url": []
                }

        for doc in all_docs:
            intersections[doc.id] = doc.to_dict()

        for key in intersections:
            new_feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        intersections[key]["longitude"], 
                        intersections[key]["latitude"]
                    ]
                },
                "properties": {
                    "id": intersections[key]["id"],
                    "name": intersections[key]["name"],
                    "status": intersections[key]["status"],
                    "timestamp": intersections[key]["timestamp"],
                    "image_url": intersections[key].get("imagepath", None)
                }
            }
        geoJson["features"].append(new_feature)
        return jsonify(geoJson), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500


# @intersectionsAPI.route('/intersections/geo-json2', methods=['GET'])
# def get_intersection_image():
#     try:
#         # all_docs = intersections_ref.stream()
#         # intersections = {
#         # }
#         geoJson = {
#                     "type":"Feature",
#                     "geometry":{
#                         "type": "Polygon",
#                         "coordinates": [
#                             [
#                             [-100.0, 40.0],
#                             [-100.0, 40.0],
#                             [-100.0, 35.0],
#                             [-100.0, 35.0]
#                             ]
#                         ],
#                         "properties": {
#                             "name": "ELL1"
#                         }
#                     },
#                     "image_url": ["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3c3JkyQWf2fFhd5qMPKw__Mm7FeAzXrxYmQ&s"]
#                 }

        # for doc in all_docs:
        #     intersections[doc.id] = doc.to_dict()

        # for key in intersections:
        #     new_feature = {
        #         "type": "Feature",
        #         "geometry": {
        #             "type": "Point",
        #             "coordinates": [
        #                 intersections[key]["longitude"], 
        #                 intersections[key]["latitude"]
        #             ]
        #         },
        #         "properties": {
        #             "id": intersections[key]["id"],
        #             "name": intersections[key]["name"],
        #             "status": intersections[key]["status"],
        #             "timestamp": intersections[key]["timestamp"]
        #         }
        #     }
        # geoJson["features"].append(new_feature)
        # geoJson["image_url"].append(intersections[key]["imagepath"])
    #     return jsonify(geoJson), 200
    # except Exception as e:
    #     return jsonify({"error": f"An error occurred: {e}"}), 500
    