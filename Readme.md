# Booking Appointment System

This project allows users to book appointments through a backend built with Django REST Framework (DRF) and a frontend JavaScript plugin that can be embedded in any webpage.

## 1️⃣ Instructions to Run the Project Locally

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Django
- Django REST Framework
- Node.js (optional, for frontend testing)
### Prerequisites
- 📂 Project Structure


```
booking-appointment-system/
│── app/                     # Django app directory
│── booking/                 # Main Django project directory (settings, URLs, WSGI)
│── frontend/                # Contains booking plugin files (JavaScript, HTML, CSS)
│   ├── bookingPlugin.js            # JavaScript plugin for embedding the booking system
│   ├── styles.css           # Stylesheet for the booking plugin
│   ├── index.html           # Standalone frontend test page
│── db.sqlite3               # SQLite database
│── manage.py                # Django management script
│── requirements.txt         # Dependencies for the project
│── README.md                # Documentation
│── .gitignore               # Git ignore file
```


### 🔹 Step 1: Clone the Repository
```bash
git clone https://github.com/samuelmatt1998/appointment-booking.git
cd appointment-booking
```

### 🔹 Step 2: Set Up a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 🔹 Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### 🔹 Step 4: Run Database Migrations
```bash
python manage.py migrate
```

### 🔹 Step 5: Start the Django Server
```bash
python manage.py runserver
```
The API will now be available at `http://127.0.0.1:8000/`.

---

## 2️⃣ Embed the Plugin on Any Webpage
To use the booking plugin on any webpage, add the following script:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Appointment Booking</title>
</head>
<body>
    <div id="booking-container"></div>
    <script src="https://yourwebsite.com/bookingPlugin.js" data-api-url="http://127.0.0.1:8000"></script>
</body>
</html>
```

Replace `https://yourwebsite.com/bookingPlugin.js` with the actual path to your hosted `bookingPlugin.js` file.

---

## 3️⃣ API Requests & Responses Format

### 🔹 Book an Appointment
**Endpoint:** `POST http://127.0.0.1:8000/api/book-appointment/`

**Request Body (JSON):**
```json
{
    "name": "John Doe",
    "phone": "1234567890",
    "date": "2025-03-15",
    "time": "14:30"
}
```

**Response (Success, 201):**
```json
{
    "message": "Appointment booked successfully."
}
```

**Response (Error, 400):**
```json
{
    "error": "This time slot is already booked."
}
```

### 🔹 Get Available Time Slots
**Endpoint:** `GET http://127.0.0.1:8000/api/available-slots/?date=YYYY-MM-DD`

**Response (Success, 200):**
```json
{
    "available_slots": ["10:00 AM - 10:30 AM", "2:30 PM - 3:00 PM"]
}
```

### 🔹 Validation Errors
- Phone number must be **exactly 10 digits**.
- Time must be in **24-hour format (HH:MM)**.
- Appointments can be booked **only between 10:00 AM - 5:00 PM, excluding 1:00 PM - 2:00 PM**.

---

## 🚀 Deployment
To deploy the plugin, host `bookingPlugin.js` on your server or a CDN and use the `<script>` tag to embed it in any webpage.

For backend deployment, use **Heroku, AWS, or DigitalOcean** to host your Django application.

---

## 📌 Notes
- Ensure the API URL matches your backend server's domain.
- If testing locally, update the `data-api-url` in the script tag accordingly.
- The plugin automatically fetches available slots when a date is selected.

Happy Coding! 🚀

