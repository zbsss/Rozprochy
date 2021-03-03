import socket;

serverIP = "127.0.0.1"
serverPort = 9008
msg = "żółta gęś" # new message

print('PYTHON UDP CLIENT')
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# changed encoding to utf-8
client.sendto(bytes(msg, "utf-8"), (serverIP, serverPort))




