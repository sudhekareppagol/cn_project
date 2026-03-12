import socket
import threading
import time
import json
from encryption import encrypt, decrypt

HOST = "0.0.0.0"
PORT = 5050


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

clients = {}
game_state = {}

print("Server started...")

def receive_messages():
    while True:
        data, addr = server.recvfrom(2048)

        message = json.loads(decrypt(data))
        player = message["player"]

        if message["type"] == "join":
            clients[player] = addr
            game_state[player] = {"x":0,"y":0}
            print(player,"joined")

        elif message["type"] == "move":
            game_state[player]["x"] = message["x"]
            game_state[player]["y"] = message["y"]

            print("Updated:",game_state)

threading.Thread(target=receive_messages, daemon=True).start()

while True:
    state = json.dumps(game_state)
    encrypted = encrypt(state)

    for client in clients.values():
        server.sendto(encrypted, client)

    time.sleep(0.05)