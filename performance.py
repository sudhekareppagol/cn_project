import socket
import time
import json
from encryption import encrypt

SERVER = ("127.0.0.1", 6000)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(5)

player_id = "perf_test"

# ---- Step 1: Join the game ----
join_msg = {
    "type": "join",
    "player": player_id
}

client.sendto(encrypt(json.dumps(join_msg)), SERVER)

# give server time to register player
time.sleep(0.2)

# ---- Step 2: Send move and measure latency ----
move_msg = {
    "type": "move",
    "player": player_id,
    "x": 0,
    "y": 0
}

start = time.time()

client.sendto(encrypt(json.dumps(move_msg)), SERVER)

try:
    data, _ = client.recvfrom(2048)

    end = time.time()

    latency = (end - start) * 1000

    print("Latency:", round(latency, 2), "ms")

except socket.timeout:
    print("Server did not respond.")

client.close()