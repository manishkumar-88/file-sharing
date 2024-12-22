import json
from tests.test_BaseClass import BaseTestCase


class TestUserResources(BaseTestCase):
    def test_user_client_signup(self):
        response = self.app.post('/api/v1/user/signup', json={
            "email": "client@example.com",
            "password": "1234",
            "role": "client"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["status"], "success")

    def test_user_operation_signup(self):
        response = self.app.post('/api/v1/user/signup', json={
            "email": "operation@example.com",
            "password": "1234",
            "role": "operation"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["status"], "success")


    def test_user_login(self):
        
        response = self.app.post('/api/v1/user/login', json={
            "email": "operation1@example.com",
            "password": "1234"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json["data"][0])
