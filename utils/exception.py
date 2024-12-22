from pyexpat.errors import messages

import mongoengine.errors
from flask import jsonify
from mongoengine.errors import DoesNotExist, NotUniqueError, InvalidQueryError, InvalidDocumentError, ValidationError, \
    OperationError, BulkWriteError, FieldDoesNotExist

import logging



class CustomException(Exception):
    """
    description:
                This is Custom Exception class which inherit the Exception and take Handle
                mongodb related errors.
                please note that we are using mongo-engine ODM for these errors.
    """

    def __init__(self,ex):
        self.ex= ex
        self.response =self.check()


    def check(self):

        logging.error(str(self.ex),exc_info=False)
        print(self.ex)


        if self.ex.__class__==NotUniqueError:
            return jsonify({"data":[], "status":"failed", "message":"User already exist."}),409

        elif self.ex.__class__==ValidationError:
            return jsonify({"data":[], "status":"failed", "message":"Validation Error of Field."}),422

        elif self.ex.__class__==InvalidQueryError:
            return jsonify({"data":[], "status":"failed", "message":"Invalid Query Error."}),400

        elif self.ex.__class__==DoesNotExist:
            return jsonify({"data":[], "status":"failed", "message":"Not Data Found."}),400

        elif self.ex.__class__==FieldDoesNotExist:
            return jsonify({"data":[], "status":"failed", "message":"Field Does Not Exist."}),400

        elif self.ex.__class__==InvalidDocumentError:
            return jsonify({"data":[], "status":"failed", "message":"Invalid Document Error."}),400

        elif self.ex.__class__==OperationError:
            return jsonify({"data":[], "status":"failed", "message":"Saving Document Operation Failed."}),409

        elif self.ex.__class__==BulkWriteError:
            return jsonify({"data":[], "status":"failed", "message":"Bulk Write Error."}),409

        else:
            return jsonify({"data":[], "status":"failed", "message":str(self.ex)}),500
