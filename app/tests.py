from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import datetime, timedelta
from app.models import Appointment


class AvailableSlotsTests(APITestCase):
    """Tests for available slots API"""

    def setUp(self):
        """Setup test data"""
        self.available_slots_url = reverse("available_slots")
        self.test_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

        # Pre-book a slot to test exclusion from available slots
        Appointment.objects.create(name="Booked User", phone="9876543210", date=self.test_date, time="10:30")

    def test_available_slots_success(self):
        """✅ Fetch available slots successfully"""
        response = self.client.get(f"{self.available_slots_url}?date={self.test_date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("10:30 AM - 11:00 AM", response.data["available_slots"])  # Booked slot should be excluded

    def test_available_slots_invalid_date(self):
        """❌ Request with an invalid date format"""
        response = self.client.get(f"{self.available_slots_url}?date=2025-02-30")  # Invalid date
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid date format. Use YYYY-MM-DD.")

    def test_available_slots_missing_date(self):
        """❌ Request without a date parameter"""
        response = self.client.get(self.available_slots_url)  # No date
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Date parameter is required.")


class BookAppointmentTests(APITestCase):
    """Tests for book appointment API"""

    def setUp(self):
        """Setup test data"""
        self.book_appointment_url = reverse("book_appointment")
        self.test_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        self.valid_data = {
            "name": "John Doe",
            "phone": "1234567890",
            "date": self.test_date,
            "time": "11:00"
        }

        # Pre-book a slot to test duplicate booking
        Appointment.objects.create(name="Booked User", phone="9876543210", date=self.test_date, time="10:30")

    def test_valid_booking(self):
        """✅ Successfully book an appointment"""
        response = self.client.post(self.book_appointment_url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Appointment booked successfully.")

    def test_booking_already_booked_slot(self):
        """❌ Attempt to book a slot that is already taken"""
        data = self.valid_data.copy()
        data["time"] = "10:30"  # Already booked time
        response = self.client.post(self.book_appointment_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "This time slot is already booked.")

    def test_booking_invalid_phone(self):
        """❌ Attempt to book with an invalid phone number"""
        data = self.valid_data.copy()
        data["phone"] = "12345"  # Invalid phone
        response = self.client.post(self.book_appointment_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Phone number must be exactly 10 digits.")

    def test_booking_invalid_date(self):
        """❌ Attempt to book with an invalid date"""
        data = self.valid_data.copy()
        data["date"] = "2025-02-30"  # Invalid date
        response = self.client.post(self.book_appointment_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid date. Please provide a valid date in YYYY-MM-DD format.")

    def test_booking_invalid_time(self):
        """❌ Attempt to book with an invalid time format"""
        data = self.valid_data.copy()
        data["time"] = "25:61"  # Invalid time
        response = self.client.post(self.book_appointment_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid time. Use HH:MM in 24-hour format.")

    def test_booking_outside_allowed_hours(self):
        """❌ Attempt to book before 10 AM or after 5 PM"""
        data_before_10am = self.valid_data.copy()
        data_before_10am["time"] = "09:30"  # Before allowed time

        data_after_5pm = self.valid_data.copy()
        data_after_5pm["time"] = "17:30"  # After allowed time

        response1 = self.client.post(self.book_appointment_url, data_before_10am, format="json")
        response2 = self.client.post(self.book_appointment_url, data_after_5pm, format="json")

        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response1.data["error"], "Appointments can only be booked between 10:00 AM and 5:00 PM, excluding 1:00 PM - 2:00 PM.")

        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.data["error"], "Appointments can only be booked between 10:00 AM and 5:00 PM, excluding 1:00 PM - 2:00 PM.")



