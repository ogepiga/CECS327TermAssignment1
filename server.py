import socket


# creating socket s
# family = AF_INET = IPV4
# type = SOCK_STREAM = TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# FIXME: figure out how to get ip address and port of the other computer in the LAN
s.bind((socket.gethostname(), 1234))
# prepare a space for possible connections with a queue of 5
s.listen(5)

# listen forever for connections
while True:
    clientsocket, address = s.accept()  # when a connection is found, store info to variables
    print(f"Connection from {address} has been established!")

    # data has to be converted into bytes to be sent over the network
    # bytes() converts anything inside of it into a specific byte, here type is utf-8
    clientsocket.send(bytes("Welcome to the server!", "utf-8"))
