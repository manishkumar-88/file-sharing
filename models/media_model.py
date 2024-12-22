from mongoengine import StringField, BooleanField
from models.baseclass.basemetaclass import BaseMetaClass

   
    



class Media(BaseMetaClass):
    """
    description: File collection.
    """
    
    
    file_type = StringField()
    file_name = StringField()
    file_path = StringField()
    file_uploaded_by = StringField()
   