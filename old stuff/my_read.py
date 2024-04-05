import serial

serial_port = 'COM16' #Its either com3 or com16, most likely 16
baud = 9600 #Just putting the standard value here
ser = serial.Serial(serial_port, baud, timeout=1)

try:
    while True:
        line = ser.readline() #.decode('utf-8')
        print(line)

except KeyboardInterrupt:
    ser.close 


