from wearable_api import BLE
import time

notifications = 0
sleep_time = 5

def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    global notifications
    print( BLE.format_notification_data(data) )
    notifications += 1

# Simple example to show how to use the interface
ble = BLE() # This is an instance of the BLE object, it handles all of the BLE connection logic

# Connect to the wearable device, will have to specify the address of the Wearable, (for our purposes this won't change)
connected = ble.connect("00:A0:50:81:22:E0")

if not connected:
  print("Failed to connect to the wearable device")

# Start Force and IMU notifications 
ble.enable_notifications( BLE.DATA_CHARACTERISTIC_UUID, notification_handler )

# Sleep for 5 seconds to receive notification data (the notification data is being received in the background)
time.sleep(sleep_time)

# Stop receiving the notifications
ble.disable_notifications( BLE.DATA_CHARACTERISTIC_UUID )

# At the end of this file the wearable will automatically disconnect (after the timeout period) or we can call ble.disconnect()
ble.disconnect()

# Will print the notifications per second for the duration of the connection
print( notifications / sleep_time )