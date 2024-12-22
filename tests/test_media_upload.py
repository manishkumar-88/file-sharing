import unittest
from io import BytesIO
import base64
from tests.test_BaseClass import BaseTestCase
from resources.media.upload import MediaUpload 

class TestFileUploadEndpoint(BaseTestCase):

    def test_operation_can_upload(self):
        self.access_token = self.login('operation')
        data = {
            "file": (open("she.xlsx", "rb"), "she.xlsx"),
        }

        response = self.app.post(
            "/api/v1/media-upload",
            headers=self.get_form_headers(),
            data=data,
        )
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json["status"])

    def test_client_cannot_upload(self):
        self.access_token = self.login()
        data = {
            "file": (open("she.xlsx", "rb"), "she.xlsx"),
        }

        response = self.app.post(
            "/api/v1/media-upload",
            headers=self.get_form_headers(),
            data=data,
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("failed", response.json["status"])




import unittest
from tests.test_BaseClass import BaseTestCase


class TestFileDownloadProcess(BaseTestCase):
    def test_client_can_fetch_file_list_and_download(self):
        self.access_token = self.login()
        
        
        
        response = self.app.get(
            "/api/v1/media-list",
            headers=self.get_headers(),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json["status"])
        self.assertGreater(len(response.json["data"]), 0)

        file_id = response.json["data"][0]["id"]

        download_url_response = self.app.get(
            f"/api/v1/media-download/{file_id}",
            headers=self.get_headers(),
        )
        self.assertEqual(download_url_response.status_code, 200)
        self.assertIn("download_url", download_url_response.json)
        encrypted_url = download_url_response.json["download_url"]

        file_download_response = self.app.get(
            encrypted_url,
            headers=self.get_headers(),
        )
        self.assertEqual(file_download_response.status_code, 200)

    def test_operation_cannot_download_file(self):
        
        self.access_token = self.login("operation")
        response = self.app.get(
            "/api/v1/media-list",
            headers=self.get_headers(),
        )
        self.assertEqual(response.status_code, 400)
        # file_id = response.json["data"][0]["id"]

        # download_url_response = self.app.get(
        #     f"/api/v1/media-download/{file_id}",
        #     headers=self.get_headers(),
        # )
        # self.assertEqual(download_url_response.status_code, 403)
        # self.assertIn("failed", download_url_response.json["status"])

    def test_client_cannot_access_expired_or_invalid_encrypted_url(self):
        """
        Test that a client cannot access an expired or invalid encrypted URL.
        """
        self.access_token = self.login()
        invalid_url_path = "invalid_encrypted_url"
        response = self.app.get(
            f"/api/v1/media-secure-file/{invalid_url_path}",
            headers=self.get_headers(),
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("failed", response.json["status"])
        self.assertIn("Invalid or tampered URL", response.json["message"])
