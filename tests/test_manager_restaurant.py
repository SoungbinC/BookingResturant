import unittest
from fastapi.testclient import TestClient
from main import app  # Assuming your FastAPI app is instantiated here
from datetime import datetime
import random

client = TestClient(app)


class TestRestaurantManagerAPI(unittest.TestCase):

    def setUp(self):
        """Setup manager, restaurant, and booking slots before manager API tests."""

        # Create a unique email and username for each test run
        unique_email = f"manager_{random.randint(1000, 9999)}@example.com"
        unique_username = f"test_manager_{random.randint(1000, 9999)}"

        # Register the manager user or log in if they already exist
        self.manager_token = self._register_or_login_user(unique_username, unique_email)

        # Create a restaurant as the manager
        self.restaurant_id = self._create_restaurant()

        # Create booking slots for the restaurant
        self._create_booking_slots()

    def _register_or_login_user(self, username, email):
        """Helper method to register or log in the manager."""
        manager_data = {
            "username": username,
            "email": email,
            "password": "managerpassword123",
            "role": "MANAGER",
        }

        # Try registering the manager
        manager_response = client.post("/auth/register", json=manager_data)

        # If registration fails because email is already registered, log in
        if (
            manager_response.status_code == 400
            and "email already registered" in manager_response.json().get("detail", "")
        ):
            print(f"Manager with email {email} already registered. Logging in instead.")
            login_data = {
                "username": email,  # email is used as the username here
                "password": "managerpassword123",  # password is the user's password
            }
            login_response = client.post("/auth/login", data=login_data)
            if login_response.status_code != 200:
                print(f"Failed to log in. Response: {login_response.json()}")

            self.assertEqual(login_response.status_code, 200)
            return login_response.json()["access_token"]

        # If registration is successful, log in
        elif manager_response.status_code == 200:
            login_data = {
                "username": email,  # email is used as the username here
                "password": "managerpassword123",  # password is the user's password
            }
            login_response = client.post("/auth/login", data=login_data)

            if login_response.status_code != 200:
                print(
                    f"Failed to log in after registration. Response: {login_response.status_code}"
                )
            self.assertEqual(login_response.status_code, 200)
            return login_response.json()["access_token"]

        # Handle unexpected failures
        else:
            raise Exception(
                f"Manager registration/login failed with response: {manager_response.json()}"
            )

    def _create_restaurant(self):
        """Helper method to create a restaurant."""
        unique_restaurant_name = f"Test Restaurant {random.randint(1000, 9999)}"
        restaurant_data = {
            "name": unique_restaurant_name,  # Unique restaurant name
            "address": "123 Test St.",
            "city": "Test City",
            "state": "TC",
            "zipcode": "12345",
            "cuisine": "Italian",
            "cost_rating": 3,
            "open_time": "10:00:00",  # Time format: 'HH:MM:SS'
            "close_time": "22:00:00",  # Time format: 'HH:MM:SS'
            "description": "A test restaurant",
            "photo_url": "http://example.com/photo.jpg",
            "status": "open",
        }

        headers = {"Authorization": f"Bearer {self.manager_token}"}
        restaurant_response = client.post(
            "/manager/restaurants", json=restaurant_data, headers=headers
        )
        self.assertEqual(restaurant_response.status_code, 200)

        return restaurant_response.json()["id"]

    # Update the _create_booking_slots method to send a list of booking slots

    def _create_booking_slots(self):
        """Helper method to create booking slots for the restaurant."""
        booking_slots = [
            {
                "start_time": "2025-04-08T15:00:00",
                "end_time": "2025-04-08T17:00:00",
                "is_booked": False,
                "table_size": 4,  # Ensure this field is included
            },
            {
                "start_time": "2025-04-09T15:00:00",
                "end_time": "2025-04-09T17:00:00",
                "is_booked": False,
                "table_size": 4,  # Ensure this field is included
            },
            {
                "start_time": "2025-04-10T15:00:00",
                "end_time": "2025-04-10T17:00:00",
                "is_booked": False,
                "table_size": 4,  # Ensure this field is included
            },
        ]

        headers = {"Authorization": f"Bearer {self.manager_token}"}

        # Ensure we are sending the correct body with table_size included
        slot_response = client.post(
            f"/manager/restaurants/{self.restaurant_id}/slots",  # Ensure the path is correct
            json=booking_slots,  # Use json to properly format the request body
            headers=headers,
        )
        self.booking_slots = slot_response.json()

        self.assertEqual(
            slot_response.status_code, 201
        )  # Status code should be 201 for resource creation
        # Optionally, validate that the 'table_size' is present in the response body
        for slot in slot_response.json():
            self.assertIn("table_size", slot)

    def test_create_restaurant(self):
        """Test restaurant creation."""
        restaurant_data = {
            "name": f"New Test Restaurant {random.randint(1000, 9999)}",
            "address": "456 Test Avenue",
            "city": "New City",
            "state": "NC",
            "zipcode": "67890",
            "cuisine": "Mexican",
            "cost_rating": 4,
            "open_time": "09:00:00",
            "close_time": "21:00:00",
            "description": "A new test restaurant.",
            "photo_url": "http://example.com/photo2.jpg",
        }
        headers = {"Authorization": f"Bearer {self.manager_token}"}
        response = client.post(
            "/manager/restaurants", json=restaurant_data, headers=headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], restaurant_data["name"])

    def test_update_restaurant(self):
        """Test updating restaurant details."""
        restaurant_data = {
            "name": "Updated Test Restaurant " + str(random.randint(1000, 9999)),
            "address": "789 Updated St.",
            "city": "Updated City",
            "state": "UC",
            "zipcode": "10112",
            "cuisine": "Mexican",
            "cost_rating": 5,
            "open_time": "08:00:00",
            "close_time": "22:00:00",
            "description": "An updated test restaurant.",
            "photo_url": "http://example.com/photo_updated.jpg",
        }
        headers = {"Authorization": f"Bearer {self.manager_token}"}
        response = client.put(
            f"/manager/restaurants/{self.restaurant_id}",
            json=restaurant_data,
            headers=headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], restaurant_data["name"])

    def test_add_booking_slots(self):
        """Test adding booking slots to a restaurant."""
        new_slot_data = {
            "start_time": "2025-04-11T16:00:00",
            "end_time": "2025-04-11T18:00:00",
            "table_size": 4,
        }
        headers = {"Authorization": f"Bearer {self.manager_token}"}
        response = client.post(
            f"/manager/restaurants/{self.restaurant_id}/slots",
            json=[new_slot_data],
            headers=headers,
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["start_time"], new_slot_data["start_time"])

    def test_view_reservations(self):
        """Test viewing restaurant reservations as a manager."""

        headers = {"Authorization": f"Bearer {self.manager_token}"}
        response = client.get(
            f"/manager/restaurants/{self.restaurant_id}/reservations",
            headers=headers,
        )
        print("View Response:", response.status_code, response.json())
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)


def test_cancel_reservation(self):
    """Test manager cancels a reservation made by a customer."""

    # 1. Register and login a customer
    customer_email = f"customer_{random.randint(1000, 9999)}@example.com"
    customer_username = f"test_customer_{random.randint(1000, 9999)}"
    customer_data = {
        "username": customer_username,
        "email": customer_email,
        "password": "customerpass123",
        "role": "CUSTOMER",
    }
    client.post("/auth/register", json=customer_data)
    login_response = client.post(
        "/auth/login",
        data={
            "username": customer_email,
            "password": "customerpass123",
        },
    )
    self.assertEqual(login_response.status_code, 200)
    customer_token = login_response.json()["access_token"]

    # 2. Create a reservation using customer credentials
    reservation_data = {
        "restaurant_id": self.restaurant_id,
        "booking_slot_id": self.booking_slots[0]["id"],
        "reservation_time": self.booking_slots[0]["start_time"],
        "number_of_people": 2,
        "status": "PENDING",
    }
    headers_customer = {"Authorization": f"Bearer {customer_token}"}
    reservation_response = client.post(
        "/customers/reservations",
        json=reservation_data,
        headers=headers_customer,
    )
    print(
        "Reservation creation response:",
        reservation_response.status_code,
        reservation_response.json(),
    )
    self.assertEqual(reservation_response.status_code, 200)
    reservation_id = reservation_response.json()["id"]

    # 3. Now cancel the reservation using manager token
    headers_manager = {"Authorization": f"Bearer {self.manager_token}"}
    cancel_response = client.post(
        f"/manager/reservations/{reservation_id}/cancel",
        headers=headers_manager,
    )
    print("Cancel response:", cancel_response.status_code, cancel_response.json())
    self.assertEqual(cancel_response.status_code, 200)
    data = cancel_response.json()
    self.assertEqual(data["status"], "CANCELED")


if __name__ == "__main__":
    unittest.main()
