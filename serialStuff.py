import serial

# Check if this is a valid serial port.
def check_serial_port(port):
    try:
        # Attempt to open the serial port
        ser = serial.Serial(port)
        ser.close()  # Immediately close the port if it was successfully opened
        print(f"Serial port {port} is valid.")
        return True
    except serial.SerialException as e:
        # Handle errors in opening the serial port
        print(f"Error opening serial port {port}: {e}")
        return False
    except Exception as e:
        # Handle other possible exceptions
        print(f"An unexpected error occurred when checking {port}: {e}")
        return False
# '''Tries to read from a serial port. If it fails, returns False.'''
# def try_read_from_serial(ser):
#     if (ser.in_waiting > 0):
#         try:
#             # Attempt to read a bit from the serial port
#             bit = ser.read(size=1)
            
#             # If it's empty, return False
#             if (bit == b''):
#                 print(f"Empty serial input: {bit}")
#                 return False

#             # If there is a bit, return true 
#             print(f"Read from serial port: {bit}")
#             return True
        
#         # Handles errors
#         except serial.SerialException as e:
#             # Handle errors in reading from serial port
#             print(f"Error reading from serial port: {e}")
#             return False
#         except Exception as e:
#             # Handle other possible exceptions
#             print(f"An unexpected error occurred: {e}")
#             return False
#     else:
#         print("No bytes waiting to be read. Bye")
#         return False


def setupSerial(serial_port, baud_rate):
    ser = serial.Serial(serial_port, baud_rate, timeout=3)
    return ser


def readByteFromSerial(ser):
    # If there are bytes waiting to be read
    if (ser.in_waiting > 0):
        try:
            line = ser.read(size=1)
            return line
        except:
            print("Error reading byte from serial")
            ser.close()
            return None
    else:
        #print("No bytes waiting to be read")
        return None
        


'''
This converts a byte (such as b'A') into a binary representation (01000001)
'''
def convertByteToBinary(byte_read):
    # convert to int
    byte_as_int = ord(byte_read)

    # convert to binary string and remove the b'
    binary_representation = bin(byte_as_int)[2:]

    # pad with zeros to get 8 bits
    return binary_representation.zfill(8)


def updateArrays(ser, psig1, psig2, psig3, psig4, psig5, psig6, psig7, psig8):
    byte_read = readByteFromSerial(ser)
    if (byte_read != None):
        binary = convertByteToBinary(byte_read)

        # update arrays
        psig1.append(int(binary[0]))
        psig2.append(int(binary[1]))
        psig3.append(int(binary[2]))
        psig4.append(int(binary[3]))
        psig5.append(int(binary[4]))
        psig6.append(int(binary[5]))
        psig7.append(int(binary[6]))
        psig8.append(int(binary[7]))
    return psig1, psig2, psig3, psig4, psig5, psig6, psig7, psig8


'''
Script
'''
# # setup arrays
# psig1 = []
# psig2 = []
# psig3 = []
# psig4 = []
# psig5 = []
# psig6 = []
# psig7 = []
# psig8 = []


# # setup serial
# ser = setupSerial('COM12', 38400)


# # loop for 10s
# start_time = time.time()
# duration = 5
# while (time.time() - start_time) < duration:
#     # Update arrays
#     psig1, psig2, psig3, psig4, psig5, psig6, psig7, psig8 = updateArrays()


# # print array
# print("psig1:", psig1)