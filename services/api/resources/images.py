import os

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user

from models.image import ImageModel
from libs.image_helpers import get_basename, upload_file, allowed_file


class Images(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        file = request.files.get("imageFile")
        if file is None:
            return {"error": "Missing image file."}, 400

        if file.filename == "":
            return {"error": "No selected file."}, 400

        if not allowed_file(file):
            return {"error": "Invalid file type."}

        destination = f"{current_user.id}/{get_basename(file)}"
        bucket_name = os.getenv("GCS_BUCKET", "travelmas-bucket")
        image_url = upload_file(bucket_name, file, destination)
        image = ImageModel(url=image_url)
        image.save_to_db()

        return image.to_dict(), 201


class Image(Resource):
    @classmethod
    @jwt_required()
    def get(cls, image_id: int):
        image = ImageModel.find_by_id(image_id)
        if image is None:
            return {"error": f"Image with image_id: {image_id} not found."}, 404
        return image.to_dict(), 200

    @classmethod
    @jwt_required()
    def delete(cls, image_id: int):
        image = ImageModel.find_by_id(image_id)
        if image is None:
            return {"error": f"Image with imgage_id: {image_id} not found."}, 404
        image.delete_from_db()
        return {}, 202
