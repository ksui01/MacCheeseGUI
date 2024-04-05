import serial



def setupSerial(serial_port, baud_rate):
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    return ser


def readByteFromSerial(ser):
    try:
        line = ser.read(size=1)
    except:
        ser.close()
    return line


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