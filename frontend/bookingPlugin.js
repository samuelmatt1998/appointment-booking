const BookingPlugin = (() => {
    let apiBaseUrl = "";

    function createUI(container) {
        container.innerHTML = `
            <div class="booking-widget">
                <h2>Book an Appointment</h2>
                <input type="text" id="name" placeholder="Enter your name" required>
                <input type="text" id="phone" placeholder="Enter phone (10 digits)" required>
                <small id="phone-error" style="color: red; display: none;">Phone number must be exactly 10 digits!</small>
                <input type="date" id="date" required>
                <select id="time-slot">
                    <option value="">Select a time slot</option>
                </select>
                <button id="book-btn">Book Now</button>
                <p id="booking-message"></p>
            </div>
        `;

        document.getElementById("date").addEventListener("change", fetchAvailableSlots);
        document.getElementById("book-btn").addEventListener("click", bookAppointment);
        document.getElementById("phone").addEventListener("input", validatePhone);
    }

    function fetchAvailableSlots() {
        const date = document.getElementById("date").value;
        if (!date) return;

        fetch(`${apiBaseUrl}/available-slots/?date=${date}`)
            .then(response => response.json())
            .then(data => {
                const select = document.getElementById("time-slot");
                select.innerHTML = `<option value="">Select a time slot</option>`; // Reset dropdown
                
                if (data.available_slots.length === 0) {
                    select.innerHTML += `<option value="">No slots available</option>`;
                } else {
                    data.available_slots.forEach(slot => {
                        const option = document.createElement("option");
                        option.value = formatTime(slot); // Ensure correct format
                        option.textContent = slot;
                        select.appendChild(option);
                    });
                }
            })
            .catch(error => console.error("Error fetching slots:", error));
    }

    function bookAppointment() {
        const name = document.getElementById("name").value.trim();
        const phone = document.getElementById("phone").value.trim();
        const date = document.getElementById("date").value;
        let time = document.getElementById("time-slot").value;

        if (!name || !phone || !date || !time) {
            document.getElementById("booking-message").innerText = "All fields are required!";
            return;
        }

        // Ensure phone number is exactly 10 digits
        if (!/^\d{10}$/.test(phone)) {
            showPhoneError();
            return;
        }

        // Trim seconds (if present) to ensure "HH:MM" format
        time = time.slice(0, 5);

        fetch(`${apiBaseUrl}/book-appointment/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, phone, date, time })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("booking-message").innerText = data.message || data.error;
            if (data.message) {
                // Refresh available slots after successful booking
                fetchAvailableSlots();
            }
        })
        .catch(error => console.error("Error booking appointment:", error));
    }

    function validatePhone() {
        const phone = document.getElementById("phone").value.trim();
        if (!/^\d{10}$/.test(phone)) {
            showPhoneError();
        }
    }

    function showPhoneError() {
        const phoneError = document.getElementById("phone-error");
        phoneError.style.display = "block";
        setTimeout(() => {
            phoneError.style.display = "none";
        }, 3000); // Hide after 3 seconds
    }

    function formatTime(slotText) {
        // Converts "10:30 AM - 11:00 AM" → "10:30"
        const timePart = slotText.split(" - ")[0].trim(); // Extract start time
        let [hourMin, period] = timePart.split(" "); // Splitting "10:30 AM"
        let [hours, minutes] = hourMin.split(":"); // Splitting "10:30"

        hours = parseInt(hours);
        if (period === "PM" && hours !== 12) {
            hours += 12; // Convert PM times
        } else if (period === "AM" && hours === 12) {
            hours = 0; // Convert 12 AM to 00
        }

        return `${hours.toString().padStart(2, "0")}:${minutes}`; // Returns "HH:MM"
    }

    return {
        init: (selector, options) => {
            apiBaseUrl = options.apiBaseUrl;
            const container = document.querySelector(selector);
            if (container) createUI(container);
        }
    };
})();
