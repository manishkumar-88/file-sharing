from mongoengine import Document, StringField, EmailField, DateTimeField, BooleanField
from models.baseclass.basemetaclass import BaseMetaClass
import bcrypt

class Users(BaseMetaClass):
    first_name = StringField()
    middle_name = StringField()
    last_name = StringField()
    username = StringField()
    contact_number = StringField()
    role = StringField(default='operation')
    email = EmailField(unique=True,required=True)
    password = StringField(required=True)
    is_verified = BooleanField(default=False)


    def check_password(self, raw_password):
        if not raw_password:
            return False
        password_bytes = raw_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, self.password.encode('utf-8'))