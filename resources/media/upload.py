import os
import logging
import random
import string
from configs import settings
from flask import request
from models.user_model import Users
from models.media_model import Media
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask_restful import Resource
from werkzeug.utils import secure_filename
from datetime import datetime
from cryptography.fernet import Fernet
from utils.exception import CustomException

ALLOWED_EXTENSIONS = {'pptx','docx' ,'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



class MediaList(Resource):

    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            user = Users.objects.filter(id=current_user,role="client").first()
            if not user:
                return {"data": [], "status": "failed", "message": "User for this operation does not exist."}, 400 

            media_data = Media.objects.all()
            final_data = [{"id": str(media.id), "file_type": media.file_type, "file_name": media.file_name, "uploaded_by": media.file_uploaded_by} for media in media_data]
            return {"data": final_data, "status": "success", "message": "Data found"}, 200

        except Exception as ex:
            raise CustomException(ex)
        
    

class MediaUpload(Resource):

    @jwt_required()
    def post(self):
        try:
            
            current_user = get_jwt_identity()
            
            user = Users.objects.filter(id=current_user,role="operation").first()
            if not user:
                return {"data": [], "status": "failed", "message": "User for this operation does not exist."}, 400 
            base_directory = "media"
            current_time = datetime.now()
            year = current_time.strftime('%Y')
            month = current_time.strftime('%B')
            day = current_time.strftime('%d')

            media_directory = os.path.join(base_directory, year, month, day)
            os.makedirs(media_directory, exist_ok=True)


            file = request.files.get('file')
            if not file:
                return {"data": [],"message": "No file provided", "status": "failed"}, 400

            filename = secure_filename(file.filename)

            if not allowed_file(filename):
                return {"data": [],"message": "File type not allowed", "status": "failed"}, 400

         
            unique_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            filename = f"{unique_id}_{filename}"
            file_upload_to = os.path.join(media_directory, filename)
            file.save(file_upload_to)

            media_entry = Media(
                file_type=filename.split('.')[-1],
                file_name=filename,
                file_path=file_upload_to,
                file_uploaded_by=current_user
            )
            media_entry.save()


            return {"data": [], "status": "success", "message": "File uploaded successfully."}, 200

        except Exception as ex:
            raise CustomException(str(ex))

