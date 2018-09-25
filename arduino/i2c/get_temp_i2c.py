import smbus
import time
import datetime 
bus = smbus.SMBus(1)

address = 0x04

def StringToBytes(val):
    retVal = []
    for c in val:
        retVal.append(ord(c))
    return retVal

def writeNumber(value):
#    bus.write_byte(address, value)
    bus.write_i2c_block_data(address, 0, StringToBytes(value))
    return -1

def readNumber():
    number = bus.read_byte(address)
    return number;

def readstring():
    number = readNumber()
#    print "number is ", number
    out = ""
    for i in bus.read_i2c_block_data(address, 0, number):
        out += (str(unichr(i)))
    return out

writeNumber("send info")
#    print"RPI: Hi arduino, I sent you ", var
time.sleep(1)
print datetime.datetime.now().strftime("%Y/%m/%d:%H:%M:%S"), readstring()
