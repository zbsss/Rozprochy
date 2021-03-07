import socket
import threading
from select import select
import sys

HEADER = 64
ENCODING  = "utf-8"
DISCONNECT_MESSAGE = "!q"

SERVER = "127.0.0.1"
PORT = 9009
ADDR = (SERVER, PORT)


def send(msg, udp=False):
    message = msg.encode(ENCODING)
    header = str(len(message)).encode(ENCODING)
    
    # make header length of HEADER
    header += b' ' * (HEADER - len(header)) 

    tcp_client.send(header)
    tcp_client.send(message) 


print(f"[CONNECTING] Connecting to server {SERVER}")

tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect(ADDR)

udp_client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_client.bind(tcp_client.getsockname())

nickname = input("Enter nickname: ")
prompt = nickname + ">  "
send(nickname)

print(
    """
    !q or Ctrl + C to disconnect
    To start a UDP message type !u and from new line type your UDP message. 
    To end your UDP message and send it press Ctrl + D.
    """
)

try:
    while True:
        read_sockets, _ , _ = select([sys.stdin, tcp_client, udp_client], [], [])
        
        for sock in read_sockets:
            if sock == tcp_client:
                msg_length = tcp_client.recv(HEADER).decode(ENCODING)

                if msg_length:
                    msg_length = int(msg_length)

                    msg = tcp_client.recv(msg_length).decode(ENCODING)
                    print(msg)
                    
            elif sock == udp_client:
                msg, addr = udp_client.recvfrom(2048)
                print(msg.decode(ENCODING))
                
            else:
                msg = sys.stdin.readline().strip()
                if msg.startswith("!u"):
                    msg = sys.stdin.read()
                    msg = prompt + "\n" + msg
                    udp_client.sendto(msg.encode(ENCODING), ADDR)
                    print()
                else:
                    msg = prompt + msg
                    send(msg)
                    if msg == DISCONNECT_MESSAGE:
                        break
                print(msg)
                
except KeyboardInterrupt:
    send(DISCONNECT_MESSAGE)
    tcp_client.close()
    udp_client.close()
except BrokenPipeError:
    print("[ERROR] Connection to server lost")