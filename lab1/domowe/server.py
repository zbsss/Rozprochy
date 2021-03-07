import socket
import threading


HEADER = 64
FORMAT  = "utf-8"
DISCONNECT_MESSAGE = "!q"

PORT = 9009
SERVER = "127.0.0.1" 
ADDR = (SERVER, PORT)

# UDP
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(ADDR)

# TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = {}


def send(sender, header, msg, udp=False):
    for nick, client in clients.items():
        socket, addr = client
        if nick != sender:
            try:
                socket.send(header.encode(FORMAT))
                socket.send(msg.encode(FORMAT))
            except BrokenPipeError:
                print(f"[ERROR] {nick} disconnected unexpectedly")
                socket.close()
                socket.pop(nick)
                continue


def handle_client(conn, addr):
    def recv():
        header = conn.recv(HEADER).decode(FORMAT)

        if header:
            msg_length = int(header)

            msg = conn.recv(msg_length).decode(FORMAT)
            return msg, header

    # get nickname, add client
    nickname, _ = recv()
    clients[nickname] = conn, addr
    print(f"[NEW CONNECTION] {nickname} connected from {addr}")

    while True:
        # this line blocks, waits until it receives a msg from client
        # we need to know how many bites the message contains
        # for that we first send a constant length HEADER that tells us how long
        # the following message is going to be
        msg, header = recv()
        if msg == DISCONNECT_MESSAGE:
            """
            IMPORTANT NOTE!!!!!1
            
            In general Python is thread safe because of GIL, 
            as long as you use ATOMIC operations, such as append, remove etc.
            """
            clients.pop(nickname)
            break

        print(f"[{addr}] {msg}")
        send(nickname, header, msg)
        
    print(f"[DISCONNECTED] {nickname} disconnected")
    conn.close()


def handle_udp():
    while True:
        msg, addr = udp_server.recvfrom(2048)
        print(f"[UDP][{addr}] {msg.decode(FORMAT)}")
        
        for nick, client in clients.items():
            _, client_addr = client
            
            if addr != client_addr:
                udp_server.sendto(msg, client_addr)
         

def start():
    # start UDP
    threading.Thread(target=handle_udp, daemon=True).start()
    
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # this line blocks, meaning it waits for a connection
        conn, addr = server.accept()
        
        # when new connection appears execute handle_client in new thread
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")


print("[STARTING] server is starting")
try:
    start()
except:
    for _, client in clients.items():
        client[0].close()
    server.close()
    udp_server.close()
    print("[SHUTDOWN] Server shutdown")
        