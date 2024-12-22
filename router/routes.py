from resources.users.user_auth import UserLoginResources,UserSignUpResources,VerfilyUserResource
from resources.media.upload import MediaUpload,MediaList
from resources.media.download import MediaDownload,SecureFileDownload
from resources.base.base import BaseResources
import logging


def initialize_routes(api):
    logging.info('Initializing the route')

    api.add_resource(BaseResources, '/')

    api.add_resource(UserSignUpResources, '/user/signup')
    api.add_resource(UserLoginResources, '/user/login')
    api.add_resource(VerfilyUserResource, '/user/verify-email')
    
   
    api.add_resource(MediaUpload, '/media-upload')
    api.add_resource(MediaDownload, '/media-download/<file_id>')
    api.add_resource(SecureFileDownload, '/media-secure-file/<encrypted_url>')

    api.add_resource(MediaList, '/media-list')
    
