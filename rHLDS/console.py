__author__ = 'chmod'

from rHLDS import const
from io import BytesIO
import socket
import sys

class Console:
	host = ''
	port = ''
	password = ''

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def __init__(self, *, host, port=27015, password):
		self.host = host
		self.port = port
		self.password = password

	def connect(self):
		self.sock.settimeout(4)
		self.sock.connect((self.host, int(self.port)))
		if self.execute('stats') == 'Bad rcon_password.':
			print('Bad password!')
			self.disconnect()
			sys.exit(1)

	def disconnect(self):
		self.sock.close()

	def getChallenge(self):
		try:
			#Format message to server
			msg = BytesIO()
			msg.write(const.startBytes)
			msg.write(b'getchallenge')
			msg.write(const.endBytes)
			self.sock.send(msg.getvalue())

			response = BytesIO(self.sock.recv(const.packetSize))
			return str(response.getvalue()).split(" ")[1]
		except Exception as e:
			print(e)
			self.disconnect()
			sys.exit(1)

	def execute(self, cmd):
		try:
			challenge = self.getChallenge()

			#Format message to server
			msg = BytesIO()
			msg.write(const.startBytes)
			msg.write('rcon '.encode())
			msg.write(challenge.encode())
			msg.write(b' ')
			msg.write(self.password.encode())
			msg.write(b' ')
			msg.write(cmd.encode())
			msg.write(const.endBytes)

			self.sock.send(msg.getvalue())
			response = BytesIO(self.sock.recv(const.packetSize))

			return response.getvalue()[5:-3].decode()
		except Exception as e:
			print(e)
			self.disconnect()
			sys.exit(1)
