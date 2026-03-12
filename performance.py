import socket
import time

SERVER = ("127.0.0.1",5000)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

start = time.time()

client.sendto(b"ping",SERVER)

data,_ = client.recvfrom(1024)

end = time.time()

latency = (end-start)*1000

print("Latency:",latency,"ms")