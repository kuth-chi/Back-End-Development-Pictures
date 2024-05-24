from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if not data:
        return {'message': 'There is no data!'}
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return picture, 200

    return {'message': 'Picture not found!'}, 404


######################################################################
# CREATE A PICTURE
######################################################################

def post_picture_duplicate(picture):
    # Implement your logic to check for duplicates
    for existing_picture in data:
        if existing_picture["id"] == picture["id"]: 
            return {'Message': f"picture with id {picture['id']} already present"}, 302
    return None

@app.route('/picture', methods=['POST'])
def create_picture():
    picture = request.json
    existing_data = post_picture_duplicate(picture)
    if existing_data:
        return existing_data
    elif not picture:
        return {'message': 'Invalid data'}, 422
    else:   
        data.append(picture)
        return picture, 201
    
    return {'message': 'Internal error'}, 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    req_picture = request.json
    for picture in data:
        if picture["id"] == int(id):
            picture.update(req_picture)
            return (picture),204
    
    return {'message': 'picture not found'}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture["id"] == int(id):
            data.remove(picture)
            return {"message":f"{id}"}, 204
    return {"message": "picture not found"}, 404
