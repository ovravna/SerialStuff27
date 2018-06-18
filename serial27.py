
import serial


ser = serial.Serial('/dev/ttyUSB0', 19200, timeout=6)

print(ser.name)


def checksum(msg: bytes) -> bytes:
	return sum(msg).to_bytes(2, byteorder='big')

def msgpacker(msg: bytes) -> bytes:
	return msg + checksum(msg) + b'\r'


messages = [b'AT+SBDWB=4\r', msgpacker(b'ABCD'), b'AT+SBDI\r', b'AT+SBDD0\r']

for m in messages:
	print('sent:', m)
	ser.write(m)
	s = ser.readlines()
	print(s)


ser.close()
