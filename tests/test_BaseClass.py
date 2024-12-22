import unittest
from flask import Flask
from flask_jwt_extended import create_access_token
from app import app

class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """This runs once before any tests are executed."""
        cls.app = app.test_client()  
        cls.app.testing = True  
        cls.populate_db()
    
    @classmethod
    def populate_db(cls):
        """Populate the database only once before running the tests."""
        # Add client
        data = {
            "email": "client1@example.com",
            "password": "1234",
            "role": "client",
            "is_verified": True
        }
        cls.app.post("/api/v1/user/signup", json=data)

        # Add operation
        data["role"] = "operation"
        data["email"] = "operation1@example.com"
        cls.app.post("/api/v1/user/signup", json=data)
    
    def setUp(self):
        """This runs before every individual test method."""
        self.access_token = self.login()
    
    def login(self, role='client'):
        """Helper method to perform login for specific roles."""
        login_data = {
            "email": f"{role}1@example.com", 
            "password": "1234"    
        }

        login_response = self.app.post("/api/v1/user/login", json=login_data)
        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_response.json['status'], "success")
        return login_response.json["data"][0]["token"]

    def get_headers(self):
        """Helper method to generate headers for authenticated requests."""
        return {
            "Authorization": f"Bearer {self.access_token}"
        }

    def get_form_headers(self):
        """Helper method to generate headers for file upload requests."""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'multipart/form-data' 
        }

    def tearDown(self):
        """This runs after each individual test method."""
        pass
