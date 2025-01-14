from locust import HttpUser, task, between
import random
import string

class LoadTestUser(HttpUser):
    host = "http://localhost:5000"
    wait_time = between(1, 2)  # Random wait time between tasks (1-2 seconds)

    def generate_random_string(self, length=8):
        """Helper function to generate random strings for user details"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @task(2)
    def register_user_valid(self):
        """Simulate valid user registration"""
        full_name = "John Doe"
        user_name = self.generate_random_string(8)
        email = f"{user_name}@gmail.com"
        password = "Password@123"
        phone = f"123456789{random.randint(0, 99)}"

        payload = {
            "fullName": full_name,
            "userName": user_name,
            "email": email,
            "password": password,
            "phone": phone
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Correct URL: /client_register
        response = self.client.post("/client_registeration", data=payload, headers=headers)
        if response.status_code == 200:
            print(f"User {user_name} registered successfully.")
        else:
            print(f"Failed to register user {user_name}.")

    @task(1)
    def register_user_missing_fields(self):
        """Simulate registration with missing fields (invalid data)"""
        full_name = "John Doe"
        user_name = self.generate_random_string(8)
        email = f"{user_name}@gmail.com"
        password = "Password@123"
        phone = ""  # Missing phone number

        payload = {
            "fullName": full_name,
            "userName": user_name,
            "email": email,
            "password": password,
            "phone": phone
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Correct URL: /client_register
        response = self.client.post("/client_registeration", data=payload, headers=headers)
        if response.status_code != 200:
            print(f"Registration with missing phone failed as expected.")
        else:
            print(f"Unexpected success when registering with missing phone.")

    @task(1)
    def login_user_valid(self):
        """Simulate valid user login after registration"""
        user_name = f"user_{random.randint(1, 10000)}"
        password = "Password@123"
        email = f"{user_name}@gmail.com"

        payload = {
            "userName": user_name,
            "email": email,
            "password": password
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Correct URL: /client_login
        response = self.client.post("/client_login", data=payload, headers=headers)
        if response.status_code == 200:
            print(f"User {user_name} logged in successfully.")
        else:
            print(f"Failed to login user {user_name}.")

    @task(1)
    def login_user_invalid(self):
        """Simulate invalid user login"""
        user_name = f"user_{random.randint(1, 10000)}"
        password = "WrongPassword"
        email = f"{user_name}@gmail.com"

        payload = {
            "userName": user_name,
            "email": email,
            "password": password
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Correct URL: /client_login
        response = self.client.post("/client_login", data=payload, headers=headers)
        if response.status_code != 200:
            print(f"Login with invalid credentials failed as expected.")
        else:
            print(f"Unexpected success when logging in with invalid credentials.")
