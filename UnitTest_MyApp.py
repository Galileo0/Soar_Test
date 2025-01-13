import unittest
from task import app  # Assuming your Flask app is in task.py
import json

class FlaskTestCase(unittest.TestCase):

    # Set up the test client
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test client registration endpoint
    def test_client_registration(self):
        # Valid registration
        response = self.app.post('/client_registeration',
                                 data=dict(
                                     fullName='John Doe',
                                     userName='johndoe',
                                     email='johndoe@gmail.com',  # Changed to gmail.com
                                     password='password123',
                                     phone='1234567890'
                                 ))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'User Registered')

    # Negative test: email already exists
    def test_email_already_exists(self):
        # Register first user
        self.app.post('/client_registeration',
                      data=dict(
                          fullName='John Doe',
                          userName='johndoe',
                          email='johndoe@gmail.com',  # Changed to gmail.com
                          password='password123',
                          phone='1234567890'
                      ))
        # Try to register the same email again
        response = self.app.post('/client_registeration',
                                 data=dict(
                                     fullName='Jane Doe',
                                     userName='janedoe',
                                     email='johndoe@gmail.com',  # Changed to gmail.com
                                     password='password123',
                                     phone='0987654321'
                                 ))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'Email already Exist')

    # Test client login endpoint with valid credentials
    def test_client_login(self):
        # Register user first (necessary step before login)
        self.app.post('/client_registeration',
                      data=dict(
                          fullName='John Doe',
                          userName='johndoe',
                          email='johndoe@gmail.com',  # Changed to gmail.com
                          password='password123',
                          phone='1234567890'
                      ))

        # Then test login with correct credentials
        response = self.app.post('/client_login',
                                 data=dict(
                                     userName='johndoe',
                                     email='johndoe@gmail.com',  # Changed to gmail.com
                                     password='password123'
                                 ))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)  # Token should be present in the response

    # Negative test: invalid login (incorrect email)
    def test_invalid_email_login(self):
        # Test login with wrong email
        response = self.app.post('/client_login',
                                 data=dict(
                                     userName='johndoe',
                                     email='wrongemail@gmail.com',  # Changed to gmail.com
                                     password='password123'
                                 ))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'In correct email or password')

    # Negative test: invalid login (incorrect username)
    def test_invalid_username_login(self):
        # Test login with wrong username
        response = self.app.post('/client_login',
                                 data=dict(
                                     userName='wrongusername',
                                     email='johndoe@gmail.com',  # Changed to gmail.com
                                     password='password123'
                                 ))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'In correct username or password')

    # Negative test: missing required fields during registration
    def test_missing_required_fields_registration(self):
        # Missing fullName
        response = self.app.post('/client_registeration',
                                 data=dict(
                                     userName='johndoe',
                                     email='johndoe@gmail.com',  # Changed to gmail.com
                                     password='password123',
                                     phone='1234567890'
                                 ))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'Invalid Data')

    # Negative test: empty email during login
    def test_empty_email_login(self):
        response = self.app.post('/client_login',
                                 data=dict(
                                     userName='johndoe',
                                     email='',
                                     password='password123'
                                 ))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'Failed')

    # Integration Test: Test full registration and login flow
    def test_full_registration_and_login_flow(self):
        # Step 1: Register a user
        response = self.app.post('/client_registeration',
                                 data=dict(
                                     fullName='John Doe',
                                     userName='johndoe',
                                     email='johndoe@gmail.com',  # Changed to gmail.com
                                     password='password123',
                                     phone='1234567890'
                                 ))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'User Registered')

        # Step 2: Log in with the registered user
        response = self.app.post('/client_login',
                                 data=dict(
                                     userName='johndoe',
                                     email='johndoe@gmail.com',  # Changed to gmail.com
                                     password='password123'
                                 ))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)  # Token should be returned

    # Corner Case: SQL Injection attempt during registration
    def test_sql_injection_registration(self):
        response = self.app.post('/client_registeration',
                                 data=dict(
                                     fullName="John'; DROP TABLE users; --",
                                     userName='johndoe',
                                     email='johndoe@gmail.com',  # Changed to gmail.com
                                     password='password123',
                                     phone='1234567890'
                                 ))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'User Registered')  # Check if injection is ignored

    # Corner Case: SQL Injection attempt during login
    def test_sql_injection_login(self):
        response = self.app.post('/client_login',
                                 data=dict(
                                     userName="johndoe' OR '1'='1",
                                     email='johndoe@gmail.com',  # Changed to gmail.com
                                     password='password123'
                                 ))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'In correct username or password')  # Check if SQL injection is blocked

    # Test edge case: very long user name
    def test_long_username_registration(self):
        long_username = 'a' * 255  # 255 characters username
        response = self.app.post('/client_registeration',
                                 data=dict(
                                     fullName='John Doe',
                                     userName=long_username,
                                     email='johndoe@gmail.com',  # Changed to gmail.com
                                     password='password123',
                                     phone='1234567890'
                                 ))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'User Registered')

    # Test edge case: very long email
    def test_long_email_registration(self):
        long_email = 'a' * 100 + '@gmail.com'  # Changed to gmail.com
        response = self.app.post('/client_registeration',
                                 data=dict(
                                     fullName='John Doe',
                                     userName='johndoe',
                                     email=long_email,
                                     password='password123',
                                     phone='1234567890'
                                 ))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'User Registered')

if __name__ == '__main__':
    unittest.main()
