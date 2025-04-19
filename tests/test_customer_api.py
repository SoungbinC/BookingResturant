import unittest
import uuid
from fastapi.testclient import TestClient
from main import app  # Assuming your FastAPI app is instantiated here

client = TestClient(app)


class TestCustomerAPI(unittest.TestCase):

    def setUp(self):
        """Setup mock customer registration and login."""
        # Generate a unique username and email to avoid collisions
        unique_username = f"test_customer_{uuid.uuid4().hex[:6]}"
        unique_email = f"{unique_username}@example.com"

        self.customer_data = {
            "username": unique_username,
            "email": unique_email,
            "password": "testpassword123",
        }

        # Register the customer
        self.registration_response = client.post(
            "/auth/register", json=self.customer_data
        )

        # Ensure registration is successful (201 status code)
        if self.registration_response.status_code != 201:
            raise Exception(
                f"Customer registration failed with response: {self.registration_response.json()}"
            )

        # Log the successful registration response
        print(
            f"Customer registered successfully with response: {self.registration_response.json()}"
        )

        # Log in to get the JWT token
        login_data = {
            "username": self.customer_data["username"],
            "password": self.customer_data["password"],
        }
        login_response = client.post("/auth/login", json=login_data)

        # Ensure login is successful (200 status code)
        self.assertEqual(login_response.status_code, 200)
        self.token = login_response.json()["access_token"]  # Get the token

    def test_search_restaurants(self):
        """Test searching for restaurants."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = client.get("/customers/restaurants/search", headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)  # Expecting a list of restaurants

    def test_get_profile(self):
        """Test retrieving customer profile."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = client.get("/customers/profile", headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertIn("username", data)
        self.assertIn("email", data)
        self.assertIn("role", data)

    def test_view_my_reservations(self):
        """Test viewing the customer's reservations."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = client.get("/customers/reservations/me", headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)  # Expecting a list of reservations
        if data:
            self.assertIn("reservation_time", data[0])
            self.assertIn("number_of_people", data[0])
            self.assertIn("status", data[0])

    def test_create_reservation(self):
        """Test creating a reservation."""
        reservation_data = {
            "restaurant_id": 1,  # Replace with valid restaurant ID
            "booking_slot_id": 3,  # Replace with valid booking slot ID
            "reservation_time": "2025-04-07T18:00:00",
            "number_of_people": 2,
            "status": "PENDING",
        }
        headers = {"Authorization": f"Bearer {self.token}"}
        response = client.post(
            "/customers/reservations", json=reservation_data, headers=headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("reservation_time", data)
        self.assertIn("number_of_people", data)
        self.assertEqual(data["status"], "PENDING")

    def test_cancel_reservation(self):
        """Test canceling a reservation."""
        payload = {
            "restaurant_id": 1,  # Replace with valid restaurant ID
            "booking_slot_id": 3,  # Replace with valid booking slot ID
        }
        headers = {"Authorization": f"Bearer {self.token}"}
        response = client.post(
            "/customers/reservations/cancel", json=payload, headers=headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("reservation_time", data)
        self.assertEqual(data["status"], "CANCELED")


if __name__ == "__main__":
    unittest.main()
