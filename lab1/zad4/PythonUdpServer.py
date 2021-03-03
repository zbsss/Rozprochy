import socket;

serverPort = 9008
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(('', serverPort))
buff = []

print('PYTHON UDP SERVER')

while True:

    buff, address = serverSocket.recvfrom(1024)
    msg = str(buff, 'utf-8')
    print("python udp server received msg: " + msg)

    if 'python' in msg.lower():
        response = "Pong Python UDP!"
    elif 'java' in msg.lower():
        response = "Pong Java UDP!"
    else:
        response = "Pong UDP!"
    
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(bytes(response, 'utf-8'), address)