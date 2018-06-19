
import serial
from serial import SerialException


class AT:
	class C:
		SBD = b'AT+SBD'
		END = b'\r'
		IX = b'IX'
		I = b'I'
		DRT_OFF = b'D0'
		WB = b'WB='
		CSQ = b'AT+CSQ'

	def init_serial(self, port: str, baudrate: int, **kwargs) -> bool:

		try:
			self.connection = serial.Serial(port, baudrate, **kwargs)
			self.isConnected = True
		except SerialException:
			self.isConnected = False

			#https://stackoverflow.com/questions/27858041/oserror-errno-13-permission-denied-dev-ttyacm0-using-pyserial-from-pyth

		return self.isConnected


	def __init__(self, port: str, baudrate: int, **kwargs):
		self.connection: serial.Serial = None
		self.isConnected = False
		self.init_serial(port, baudrate, **kwargs)


	def send(self, msg: bytes = b'', *instuctions):

		for inst in instuctions:
			i = inst(msg)
			print(i)
			self.connection.write(i)
			s = self.connection.readlines()
			print(s)



	def close(self):
		if self.isConnected:
			self.connection.close()
			self.connection = None
			self.isConnected = False
		elif self.connection:


			self.connection.close()
			self.connection = None



	@staticmethod
	def checksum(msg: bytes) -> bytes:
		return sum(msg).to_bytes(2, byteorder='big')

	@staticmethod
	def wb_of(msg: bytes) -> bytes:
		return bytes(str(len(msg)), 'utf-8')

	@staticmethod
	def initiate(msg: bytes) -> bytes:
		return AT.C.SBD + AT.C.WB + AT.wb_of(msg)

	WB = lambda msg: AT.C.SBD + AT.C.WB + AT.wb_of(msg) + AT.C.END
	BTF = lambda msg: msg + AT.checksum(msg) + AT.C.END
	IX = lambda msg: AT.C.SBD + AT.C.IX + AT.C.END
	I = lambda msg: AT.C.SBD + AT.C.I + AT.C.END
	DRT_OFF = lambda msg: AT.C.SBD + AT.C.DRT_OFF + AT.C.END
	CSQ = lambda msg: AT.C.CSQ + AT.C.END


at = AT('/dev/ttyUSB0', 19200, timeout=10)

at.send(b'', AT.CSQ)
at.send(b'ABCD', AT.WB, AT.BTF, AT.IX, AT.DRT_OFF)
at.send(b'', AT.CSQ)

at.close()


