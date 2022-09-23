import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "localhost"  # '127.0.0.1'
port = 4500
address = (ip, port)
run = True
while run:
    # connect to driver
    client = socket.socket()
    client.connect(address)

    # ask for operation
    message = input("> ")

    # send operation
    client.sendall(message.encode("utf-8"))

    # stop loop if abort instruction sent
    if "abort" in message:
        run = False

    # receive data from driver
    data = client.recv(1024).decode("utf-8")
    print(data)
