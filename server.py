import socket
import threading
import time
import json
from encryption import encrypt, decrypt

HOST = "0.0.0.0"
PORT = 6000

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

clients = {}
game_state = {}

print("Server started...")

def receive_messages():
    while True:
        try:
            data, addr = server.recvfrom(2048)
        except ConnectionResetError:
            # Ignore reset packets (common on Windows UDP)
            continue

        try:
            message = json.loads(decrypt(data))
        except Exception:
            # Ignore invalid or corrupted packets
            continue

        player = message.get("player")
        msg_type = message.get("type")

        # ---- Handle join request ----
        if msg_type == "join":

            if player in clients:
                print("Duplicate player attempt:", player)

                error_msg = {
                    "type": "error",
                    "message": "Player name already taken. Choose another name."
                }

                server.sendto(encrypt(json.dumps(error_msg)), addr)
                continue

            clients[player] = addr
            game_state[player] = {"x": 0, "y": 0}

            print(player, "joined")

        # ---- Handle movement ----
        elif msg_type == "move":

            if player in game_state:
                game_state[player]["x"] = message["x"]
                game_state[player]["y"] = message["y"]

                print("Updated:", game_state)

# Start receiver thread
threading.Thread(target=receive_messages, daemon=True).start()

# ---- Broadcast game state to all clients ----
while True:
    try:
        state = json.dumps(game_state)
        encrypted = encrypt(state)

        for client in clients.values():
            server.sendto(encrypted, client)

        time.sleep(0.05)  # 20 updates per second

    except Exception:
        # Prevent server crash if a client disconnects
        continue