import time
import json,os
from configs import settings
from models.user_model import Users
from models.media_model import Media
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask_restful import Resource
from cryptography.fernet import Fernet
from utils.exception import CustomException




class MediaDownload(Resource):
    @jwt_required()
    def get(self, file_id):
        try:
            current_user = get_jwt_identity()
            user = Users.objects.filter(id=current_user, role="client").first()
            if not user:
                return {"data": [], "status": "failed", "message": "User for this operation does not exist."}, 400

            media_file = Media.objects.filter(id=file_id).first()
            if not media_file:
                return {"data": [], "status": "failed", "message": "Media file not found."}, 404

            file_path = media_file.file_path
            encryption_key = settings.encryption_key  
            fernet = Fernet(encryption_key)
            payload = {
                "file_path": file_path,
                "user_id": str(current_user),
                "exp": time.time() + float(settings.url_validity_period)
            }
            encrypted_url = fernet.encrypt(json.dumps(payload).encode()).decode()

            return {
                "download_url": f"{settings.base_media_url}{encrypted_url}",
                "status": "success",
                "message": "URL encrypted successfully.",
            }, 200

        except Exception as ex:
            raise CustomException(str(ex))

        



from flask import send_file
import json

class SecureFileDownload(Resource):
    @jwt_required()
    def get(self, encrypted_url):
        try:
            current_user = get_jwt_identity()
            user = Users.objects.filter(id=current_user, role="client").first()
            if not user:
                return {"data": [], "status": "failed", "message": "Access denied."}, 403

            encryption_key = settings.encryption_key
            fernet = Fernet(encryption_key)

            try:
                decrypted_payload = json.loads(fernet.decrypt(encrypted_url.encode()).decode())
            except Exception:
                return {"data": [], "status": "failed", "message": "Invalid or tampered URL."}, 400

            if decrypted_payload["user_id"] != str(current_user):
                return {"data": [], "status": "failed", "message": "Unauthorized access."}, 403

            if time.time() > decrypted_payload["exp"]:
                return {"data": [], "status": "failed", "message": "URL has expired."}, 400

            file_path = decrypted_payload["file_path"]
            if not os.path.exists(file_path):
                return {"data": [], "status": "failed", "message": "File not found."}, 404

            return send_file(file_path, as_attachment=True)

        except Exception as ex:
            raise CustomException(str(ex))
        