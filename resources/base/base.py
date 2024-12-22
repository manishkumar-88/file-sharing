
from flask import make_response
from flask import render_template
from flask_restful import Resource

from utils.exception import CustomException


class BaseResources(Resource):

    def get(self):
        try:

            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('index.html'), 200, headers)

        except Exception as ex:
            raise CustomException(ex)