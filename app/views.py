from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import time, datetime, timedelta
from .models import Appointment
from .serializers import AppointmentSerializer
from django.db.utils import IntegrityError
from rest_framework import status

@api_view(["GET"])
def available_slots(request):
    """Returns available 30-minute slots between 10 AM and 5 PM, excluding 1 PM - 2 PM."""

    try:
        date_str = request.query_params.get("date")
        if not date_str:
            return Response({"error": "Date parameter is required."}, status=400)

        # Convert date string to a proper date object
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        # Define available time slots (10 AM - 5 PM, excluding 1 PM - 2 PM)
        start_time = datetime.strptime("10:00", "%H:%M").time()
        end_time = datetime.strptime("17:00", "%H:%M").time()
        break_start = datetime.strptime("13:00", "%H:%M").time()
        break_end = datetime.strptime("14:00", "%H:%M").time()
        
        slots = []
        current_time = start_time

        while current_time < end_time:
            next_time = (datetime.combine(datetime.today(), current_time) + timedelta(minutes=30)).time()

            # Skip the break time
            if not (break_start <= current_time < break_end):
                # Format slot as "HH:MM AM/PM - HH:MM AM/PM"
                slot_label = f"{current_time.strftime('%I:%M %p')} - {next_time.strftime('%I:%M %p')}"
                
                # Check if this slot is already booked
                if not Appointment.objects.filter(date=date, time=current_time).exists():
                    slots.append(slot_label)

            current_time = next_time  # Move to the next 30-minute slot

        return Response({"date": date_str, "available_slots": slots}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)





@api_view(["POST"])
def book_appointment(request):
    try:
        data = request.data

        # **Extracting fields**
        name = data.get("name")
        phone = data.get("phone")
        date = data.get("date")
        time_str = data.get("time")

        # **Checking for empty fields**
        if not all([name, phone, date, time_str]):
            return Response({"error": "All fields are required."}, status=400)

        # **Phone number validation**
        if not (phone.isdigit() and len(phone) == 10):
            return Response({"error": "Phone number must be exactly 10 digits."}, status=400)

        # **Date validation (checks invalid dates like Feb 30)**
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date. Please provide a valid date in YYYY-MM-DD format."}, status=400)

        # **Time validation (ensures no invalid times like 25:61)**
        try:
            time_obj = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            print(f'################{time_str}')
            return Response({"error": "Invalid time. Use HH:MM in 24-hour format."}, status=400)

        # **Ensure time is between 10:00 AM and 5:00 PM, excluding 1:00 PM - 2:00 PM**
        start_time = time(10, 0)
        end_time = time(17, 0)
        break_start = time(13, 0)
        break_end = time(14, 0)

        if not (start_time <= time_obj < end_time) or (break_start <= time_obj < break_end):
            return Response({"error": "Appointments can only be booked between 10:00 AM and 5:00 PM, excluding 1:00 PM - 2:00 PM."}, status=400)

        # **Check if slot is already booked**
        if Appointment.objects.filter(date=date_obj, time=time_obj).exists():
            return Response({"error": "This time slot is already booked."}, status=400)

        # **Save appointment**
        appointment = Appointment.objects.create(name=name, phone=phone, date=date_obj, time=time_obj)

        return Response({"message": "Appointment booked successfully."}, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=500)