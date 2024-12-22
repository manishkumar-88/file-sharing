import logging

from flask_restful import Resource
from flask import request, make_response
from mongoengine import DoesNotExist
from models.user_model import Users
from utils.hash_password import hash_password
from utils.exception import CustomException
from utils.mail_sender import Sender
from utils.jwt_token import verify_token,generate_verification_token
from flask_jwt_extended import create_access_token




class UserLoginResources(Resource):
        @staticmethod
        def post():

            final_data = []
            try:
                body = request.get_json()
                email = body.get("email")
                password = body.get("password")
                if email is None or password is None:
                    return {"data": [], "status": "failed", "message": "email or password not provided"}, 400
                
                user = Users.objects.filter(email=email).first()
                if not user :
                    return {"data": [], "status": "failed", "message": "User Does Not Exist."}, 400
                
                if user.role =="client" and  not user.is_verified:
                    return {"data": [], "status": "failed", "message": "Email not verified."}, 403
                
                if user.check_password(password):
                    access_token = create_access_token(identity=str(user.id))
                    # ----------------------------------- This line set token in the headers    --------------------------------------#
                    # Set the access token in the headers
                    # response = make_response({"message": "User found"}, 200)
                    # response.headers['Authorization'] = f'Bearer {access_token}'
                    # return response
                    final_data.append({"id": str(user.id), "email": user.email,"token": access_token})

                    response = make_response({"data": final_data,"status":"success","message": "Data Found"},200)
                    return response
                else:
                    return {"data": [],"status":"failed","message": "Invalid Password."},400

            except DoesNotExist:
                return {"data": [], "status": "failed", "message": "User Does Not Exist."}, 400

            except Exception as ex:
                raise CustomException(ex)
            




class UserSignUpResources(Resource):


    @staticmethod
    def post():
        try:
            body = request.get_json()
            email=body.get('email')
            password =body.get('password')
            role = body.get('role')
            

            if not email and not password :
                return {"data": [], "status": "failed", "message": "email or password is not provided."}, 400
            
                   
            if role == "client":
                token= generate_verification_token(email)
                sender = Sender()
                sender.send_mail(email,token=token)
                
            body['password'] =   hash_password(password)
            user =Users(**body)
            print(user.password)
            user.save()
            return {"data": [], "status": "success", "message": "User created successfully."}, 201

        except Exception as ex:
            raise CustomException(ex)
            


class  VerfilyUserResource(Resource):
    
    
    def get(self):
        
        try:
            token= request.args.get('token')
            if not token:
                return {"data": [], "status": "failed", "message": "Token not provided."}, 400
            payload = verify_token(token)
            if not payload:
                return {"data": [], "status": "failed", "message": "Invalid Token."}, 401
            email= payload.get('email')
            user = Users.objects.filter(email=email, role='client').first()
            if not user:
                return {"data": [], "status": "failed", "message": "User not found."}, 404
            user.is_verified=True
            user.save()
            
            return {"data": [], "status": "success", "message": "User verified successfully."}, 200
        
        except Exception as ex:
            raise CustomException(ex)            