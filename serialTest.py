import serial
import time

# Initialize serial port
ser = serial.Serial('/dev/cu.usbserial-210', 230400, timeout=1)
print("Writing S")
ser.write(b'S')

try:
    while True:
        if ser.in_waiting > 0:
          data = ser.read(size=1)
          print(data)
        time.sleep(0.1)  # Small delay to prevent CPU overuse
except KeyboardInterrupt:
    print("Program terminated by user")
finally:
    ser.close()
    print("Serial connection closed")