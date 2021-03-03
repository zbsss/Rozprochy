import socket;

serverIP = "127.0.0.1"
serverPort = 9008
msg = "Ping Python Udp!"

print('PYTHON UDP CLIENT')
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto((300).to_bytes(4, byteorder='little'), (serverIP, serverPort))



buff, _ = client.recvfrom(1024)
print("received msg:", int.from_bytes(buff, byteorder='little'))