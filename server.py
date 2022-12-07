import socket
import time


host = socket.gethostbyname(socket.gethostname())
port = 9090

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

q = False
print('Server started')

while not q:
    try:
        data, address = s.recvfrom(1024)
        if address not in clients:
            clients.append(address)
        print(f'{address[0]}:{address[1]}', end=' ')
        print(data.decode('utf-8'))

        for client in clients:
            if address != client:
                s.sendto(data, client)
    except Exception as ex_:
        print('Server stopped')
        q = True
s.close()