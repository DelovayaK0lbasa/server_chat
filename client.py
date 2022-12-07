import socket
import threading
import time


def messaging(name, sock):
    while not shutdown:
        try:
            while True:
                data, address = sock.recvfrom(1024)

                decrypt = ''
                k = False
                for i in data.decode('utf-8'):
                    if i == ':':
                        k = True
                        decrypt += i
                    elif k == False or i == ' ':
                        decrypt += i
                    else:
                        decrypt += chr(ord(i) ^ key)
                print(decrypt)

                time.sleep(0.5)
        except:
            pass


key = 1488
shutdown = False
join = False

host = socket.gethostbyname(socket.gethostname())
port = 0

server = (host, 9090)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(False)
name = input('Type your name: ')

rT = threading.Thread(target=messaging, args=('recvThread', s))
rT.start()

while not shutdown:
    if not join:
        s.sendto(f'{name} joined chat'.encode('utf-8'), server)
        join = True
    else:
        try:
            msg = input()

            crypt = ''
            for i in msg:
                crypt += chr(ord(i) ^ key)
            msg = crypt

            if msg != '':
                s.sendto(f'{name}: {msg}'.encode('utf-8'), server)

            time.sleep(0.5)
        except:
            s.sendto(f'{name} left chat'.encode('utf-8'), server)
            shutdown = True

rT.join()
s.close()
