import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '127.0.0.1'
port = 4500
address = (ip, port)
run = True
while run:
    client = socket.socket()
    client.connect(address)
    message = input("> ")
    client.sendall(message.encode('utf-8'))
    data = client.recv(1024).decode('utf-8')
    print(data)
    if message == "abort":
        run = False
