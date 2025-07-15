# 🚗 Tyre Maintenance for Accident prevention

A smart IoT-integrated web application for real-time tyre parameter monitoring and service management.

---

## 📌 Key Concepts

- **Real-Time Sensor Monitoring:** Collects data from sensors (pressure, temperature, load, tread depth) connected via USB to the ESP32.
- **Threshold Alerts:** Sends alerts if any abnormal conditions detected.
- **SMS & Email Notifications:** Uses Twilio to notify users if tyre conditions are unsafe or if service is overdue.
- **User Authentication:** Login and registration system with user data stored in MongoDB.
- **Car Info Management:** Users can register their vehicle (brand/model/type), dynamically fetched from the database.
- **Service Reminder System:** Tracks last service date and alerts users after 6 months via SMS.
- **Responsive Web UI:** Designed with a modern look using HTML, CSS, and JavaScript.

---

## 🛠 Tech Stack

**Frontend:**
- HTML5
- CSS3 (Modern, gradient-based UI)
- JavaScript (vanilla)

**Backend:**
- Python (Flask 3.1.0)

**Database:**
- MongoDB (Compass)
  - `tyre_projects` database
  - Collections: `users`, `vehicle`, `sensors_data`

**Hardware:**
- ESP32
- Pressure Sensor
- Temperature Sensor
- Load Cell
- Ultrasonic Sensor (for tread depth)

**Notifications:**
- Twilio API (SMS)

---

## 📷 Preview

Have a look at the live preview screenshots:  
🔗 [Preview](https://drive.google.com/file/d/1oQHk1PJR5hsv6KX-aurE3H1SEk9DsJwX/view?usp=drivesdk)

---

## 🚀 Clone the Project

```bash
git clone https://github.com/your-username/tyre_project.git
cd tyre_project

```
---

## 📞 Contact

Feel free to connect with me:

- 🔗 [LinkedIn Profile](https://www.linkedin.com/in/mandlem-sirivarshini?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
