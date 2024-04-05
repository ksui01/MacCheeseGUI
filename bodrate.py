import serial
import time

serial_port = 'COM12'
common_baud_rates = [38400, 57600, 115200]
timeout = 1  # seconds

def try_readline(ser):
    try:
        line = ser.read(size=1)
        return line
    except Exception as e:
        print(f"Exception reading from serial: {e}")
        return None

def check_data_validity(data):
    # Implement this based on your criteria for valid data
    # For now, just check if data is not empty
    return bool(data)

for baud in common_baud_rates:
    try:
        with serial.Serial(serial_port, baud, timeout=timeout) as ser:
            print(f"Trying baud rate: {baud}")
            time.sleep(0.5)  # Wait a bit for the serial port to initialize
            
            for _ in range(10):  # Try reading a few lines to check validity
                data = try_readline(ser)
                print(f"Data received at baud rate {baud}: {data}")
                if data and check_data_validity(data):
                    print(f"Data received at baud rate {baud}: {data}")
            else:  # No valid data found at this baud rate
                continue  # Try the next baud rate
            
            # If we found valid data, no need to continue trying other baud rates
            break
    except serial.SerialException as e:
        print(f"Could not open serial port at baud rate {baud}: {e}")
