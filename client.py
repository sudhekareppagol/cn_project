import socket
import json
from encryption import encrypt, decrypt

SERVER_IP = "10.30.202.91"
PORT = 6000

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

    # wait until server sends updated position
    while True:
        data, _ = client.recvfrom(2048)

        decrypted = decrypt(data)
        state = json.loads(decrypted)

        # check if our player state updated
        if player_id in state:
            if state[player_id]["x"] == x and state[player_id]["y"] == y:
                break

    print("Game state:", state)
