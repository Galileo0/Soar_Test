from locust import HttpUser, task, between
import random
import string

class StressTestUser(HttpUser):
    host = "http://localhost:5000"  # Your Flask app's host
    wait_time = between(0.5, 1)  # Simulate user think time with small wait time

    def generate_random_string(self, length=8):
        """Helper function to generate random strings for user details."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def generate_invalid_email(self):
        """Generate a random string that is not a valid email."""
        return f"{self.generate_random_string(8)}@invalid.com"

    def generate_invalid_username(self):
        """Generate a random username with special characters to simulate invalid input."""
        return self.generate_random_string(8) + "$%^&*"

    @task(2)
    def login_user_valid(self):
        """Simulate a valid user login."""
        user_name = f"user_{random.randint(1, 10000)}"  # Assume this user exists
        email = f"{user_name}@gmail.com"  # Valid email
        password = "Password@123"  # Correct password

        payload = {
            "userName": user_name,
            "email": email,
            "password": password
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = self.client.post("/client_login", data=payload, headers=headers)
        if response.status_code == 200:
            print(f"User {user_name} logged in successfully.")
        else:
            print(f"Failed to login user {user_name}. Status code: {response.status_code}")

    @task(3)
    def login_user_invalid(self):
        """Simulate an invalid user login (incorrect password)."""
        user_name = f"user_{random.randint(1, 10000)}"  # Assume user exists but wrong password
        email = f"{user_name}@gmail.com"  # Valid email
        password = "WrongPassword"  # Invalid password

        payload = {
            "userName": user_name,
            "email": email,
            "password": password
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = self.client.post("/client_login", data=payload, headers=headers)
        if response.status_code != 200:
            print(f"Invalid login attempt for {user_name} failed as expected.")
        else:
            print(f"Unexpected success when logging in with invalid credentials for {user_name}.")

    @task(1)
    def login_user_missing_fields(self):
        """Simulate login with missing fields (empty username or password)."""
        user_name = ""  # Empty username
        email = ""  # Empty email
        password = "Password@123"  # Valid password

        payload = {
            "userName": user_name,
            "email": email,
            "password": password
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = self.client.post("/client_login", data=payload, headers=headers)
        if response.status_code != 200:
            print(f"Login with missing fields failed as expected.")
        else:
            print(f"Unexpected success when logging in with missing fields.")

    @task(1)
    def login_user_sql_injection(self):
        """Simulate SQL Injection attempt in the login request."""
        user_name = "' OR 1=1 --"  # Malicious input (SQL injection attempt)
        email = "malicious@example.com"
        password = "Password@123"  # Valid password to avoid false positives

        payload = {
            "userName": user_name,
            "email": email,
            "password": password
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = self.client.post("/client_login", data=payload, headers=headers)
        if response.status_code != 200:
            print(f"SQL injection attempt was blocked as expected.")
        else:
            print(f"Unexpected success with SQL injection attempt.")

    @task(1)
    def login_user_excessive_requests(self):
        """Flood the system with multiple login requests in a short time."""
        user_name = f"user_{random.randint(1, 10000)}"  # Valid user for login attempt
        email = f"{user_name}@gmail.com"  # Valid email
        password = "Password@123"  # Correct password

        payload = {
            "userName": user_name,
            "email": email,
            "password": password
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        for _ in range(50):  # Sending 50 requests in a loop to stress the system
            self.client.post("/client_login", data=payload, headers=headers)

        print(f"Flooded login attempts for {user_name}.")

