import socket
import json
from encryption import encrypt, decrypt

SERVER_IP = "127.0.0.1"
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

player_id = input("Enter player id: ")

# send join message
join_msg = {
    "type": "join",
    "player": player_id
}

client.sendto(encrypt(json.dumps(join_msg)), (SERVER_IP, PORT))

while True:
    # get movement input
    x = int(input("Move X: "))
    y = int(input("Move Y: "))

    move_msg = {
        "type": "move",
        "player": player_id,
        "x": x,
        "y": y
    }

    # send move to server
    client.sendto(encrypt(json.dumps(move_msg)), (SERVER_IP, PORT))

    # receive updated game state
    data, _ = client.recvfrom(2048)

    # decrypt and convert JSON
    decrypted = decrypt(data)
    state = json.loads(decrypted)

    print("Game state:", state)