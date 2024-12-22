import unittest 
from app import app

from tests.test_media_upload import TestFileDownloadProcess,TestFileUploadEndpoint
from tests.test_user_auth import TestUserResources



def run_tests():
    # Create a test suite combining all the test cases
    suite = unittest.TestSuite()
    
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestUserResources))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestFileDownloadProcess))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestFileUploadEndpoint))



    # Set up application context for testing
    with app.app_context():
        # Run the test suite
        runner = unittest.TextTestRunner()
        runner.run(suite)

if __name__ == "__main__":
    run_tests()