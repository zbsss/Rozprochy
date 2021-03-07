import socket
import threading
import sys

HEADER = 64
ENCODING  = "utf-8"
DISCONNECT_MESSAGE = "!q"

SERVER = "127.0.0.1"
PORT = 9008
ADDR = (SERVER, PORT)


def receive():
    while True:
        # this line blocks, waits until it receives a msg from client
        # we need to know how many bites the message contains
        # for that we first send a constant length HEADER that tells us how long
        # the following message is going to be
        msg_length = client.recv(HEADER).decode(ENCODING)

        if msg_length:
            msg_length = int(msg_length)

            msg = client.recv(msg_length).decode(ENCODING)
            print(msg)
    

def send(msg):
    message = msg.encode(ENCODING)
    header = str(len(message)).encode(ENCODING)
    
    # make header length of HEADER
    header += b' ' * (HEADER - len(header)) 

    client.send(header)
    client.send(message) 


print(f"[CONNECTING] Connecting to server {SERVER}")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

nickname = input("Enter nickname: ")
prompt = nickname + ">  "
send(nickname)

receaver = threading.Thread(target=receive, daemon=True)
receaver.start()

print("Type !q to disconnect\n")
try:
    while True:
        msg = input()
        
        print(prompt + msg)
        send(prompt + msg)
        
        if msg == DISCONNECT_MESSAGE:
            break
except KeyboardInterrupt:
    send(DISCONNECT_MESSAGE)
    client.close()
except BrokenPipeError:
    print("[ERROR] Connection to server lost")