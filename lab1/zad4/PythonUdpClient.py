import socket;

serverIP = "127.0.0.1"
serverPort = 9008
msg = "Ping Python Udp!"

print('PYTHON UDP CLIENT')
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# changed encoding to utf-8
client.sendto(bytes(msg, "utf-8"), (serverIP, serverPort))

buff, address = client.recvfrom(1024)
print("received msg: " + str(buff, 'utf-8'))


