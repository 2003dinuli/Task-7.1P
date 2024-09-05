import csv
import time
from datetime import datetime
from arduino_iot_cloud import ArduinoCloudClient

DEVICE_ID = "141e425c-a422-4aec-8a87-4e7e2d32c955"
SECRET_KEY = "ihm0MdSv!GY6nEXe9cMrnwnvz"

# CSV file name
csv_file = "6.1.csv"

# Callback function for temperature changes
def on_temperature_changed(client, value):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_data(timestamp, value, None)  # Save temperature only

# Callback function for humidity changes
def on_humidity_changed(client, value):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_data(timestamp, None, value)  # Save humidity only

# Function to save data to CSV
def save_data(timestamp, temperature, humidity):
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Check if both values are None
        if temperature is None and humidity is None:
            return  # Skip writing empty row
        writer.writerow([timestamp, temperature, humidity])
        print(f"Data saved: {timestamp}, {temperature}, {humidity}")

def main():
    print("Starting the IoT client...")

    # Instantiate Arduino cloud client
    client = ArduinoCloudClient(
        device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY
    )

    # Register with cloud variables
    client.register("temperature", value=None, on_write=on_temperature_changed)
    client.register("humidity", value=None, on_write=on_humidity_changed)

    # Initialize CSV file with headers
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Temperature (°C)", "Humidity (%)"])

    # Start cloud client
    client.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Script terminated by user.")

if __name__ == "__main__":
    main()
