
from flask import Flask
import serial
import threading
from twilio.rest import Client  # Twilio import

app = Flask(__name__)

# Initialize the sensor data dictionary
sensor_data = {
    "temperature": 0.0,
    "weight": 0.0,
    "pressure": 0.0
}

# === Twilio Configuration ===
account_sid = "YOUR_SID"
auth_token = "YOUR_SECRETCODE"
twilio_number = "TWILIO_NUMBER"
to_number = "MOBILE_NO"

twilio_client = Client(account_sid, auth_token)
alert_sent = False  # Flag to prevent repeated messages

# === Serial Thread ===
def read_serial():
    global alert_sent
    try:
        ser = serial.Serial("COM7", 115200, timeout=1)  # Adjust to your serial port
        print(f"[Serial] Connected to COM7 at 115200 baud.")

        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print(f"[Serial] {line}")

                # Parsing the data string
                if "LM35 Raw:" in line and "Load Raw:" in line and "Pressure Raw:" in line:
                    try:
                        # Split the string by commas and extract values
                        parts = line.split(", ")
                        temp_raw = int(parts[0].split(":")[1].strip())
                        load_raw = int(parts[1].split(":")[1].strip())
                        pressure_raw = int(parts[2].split(":")[1].strip())

                        # Convert to appropriate units and update the sensor data
                        sensor_data["temperature"] = temp_raw * 3.3 / 4095 / 0.01  # LM35 conversion
                        sensor_data["weight"] = load_raw / 1000.0  # Adjust scale if necessary
                        sensor_data["pressure"] = pressure_raw / 1000.0  # Adjust scale if necessary

                        # === SMS Condition Check ===
                        if (sensor_data["pressure"] > 100.0) or (sensor_data["temperature"] > 10.0) or (sensor_data["weight"] > 1.0):
                          if not alert_sent:
                            try:
                              message = twilio_client.messages.create(
                                body=(
                                  f"ALERT 🚨:\n"
                                  f"Pressure: {sensor_data['pressure']:.2f} bar\n"
                                  f"Temp: {sensor_data['temperature']:.2f} °C\n"
                                  f"Load: {sensor_data['weight']:.2f} kg"
                                ),
                                from_=twilio_number,
                                to=to_number
                              )
                              alert_sent = True
                              print("[Twilio] Alert SMS sent!")
                            except Exception as twilio_error:
                              print(f"[Twilio Error] Could not send alert: {twilio_error}")
                    except Exception as e:
                            print(f"[Error] Parsing sensor data: {e}")
    except serial.SerialException as e:
        print(f"[Serial Error] {e}")

# Start the thread
serial_thread = threading.Thread(target=read_serial, daemon=True)
serial_thread.start()

# === Flask route ===
@app.route("/")
def index():
    return f"""
    <html>
    <head>
    <title>ESP32 Sensor Data</title>
    <meta http-equiv="refresh" content="5">
    <style>
    body {{
      font-family: 'Arial', sans-serif;
      margin: 0;
      padding: 0;
      background: url('1647263685112.jpg') no-repeat center center/cover;
      background-size: cover;
      color: #333;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
    }}

    body::before {{
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(255, 255, 255, 0.6);
      z-index: -1;
    }}

    h1 {{
      font-size: 2.5rem;
      color: #3a7bd5;
      margin-bottom: 20px;
      text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
    }}

    .tyre-container {{
      display: flex;
      gap: 20px;
      margin-bottom: 20px;
    }}

    .column {{
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}

    .tyre-card {{
      background-color: #f4f4f9;
      padding: 20px;
      border-radius: 16px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      width: 260px;
    }}

    .tyre-card h2 {{
      font-size: 1.4rem;
      color: #3a7bd5;
      margin-bottom: 10px;
    }}

    .tyre-card p {{
      font-size: 1rem;
      margin: 5px 0;
      color: #555;
    }}

    .tyre-card span {{
      font-weight: bold;
      color: #000;
    }}

    .tyre-card:hover {{
      transform: translateY(-5px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    }}
    </style>
    </head>
    <body>
    <h1>Tyre Monitoring System</h1>

    <div class="tyre-container">
      <div class="column">
        <div class="tyre-card">
          <h2>Tyre 1</h2>
          <p>Pressure: {sensor_data["pressure"]:.2f} bar</p>
          <p>Temperature: {sensor_data["temperature"]:.2f} °C</p>
          <p>Tread Depth: 1.1mm</p>
          <p>Weight: {sensor_data["weight"]:.2f} kg</p>
        </div>
        <div class="tyre-card">
          <h2>Tyre 2</h2>
          <p>Pressure: </p>
          <p>Temperature: </p>
          <p>Tread Depth: </p>
          <p>Load: </p>
        </div>
      </div>
      <div class="column">
        <div class="tyre-card">
          <h2>Tyre 3</h2>
          <p>Pressure: </p>
          <p>Temperature: </p>
          <p>Tread Depth: </p>
          <p>Load: </p>
        </div>
        <div class="tyre-card">
          <h2>Tyre 4</h2>
          <p>Pressure: </p>
          <p>Temperature: </p>
          <p>Tread Depth: </p>
          <p>Load: </p>
        </div>
      </div>
    </div>
    </body>
    </html>
    """

# === Run the server ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)