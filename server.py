import socket
import random
import time

HEADER_SIZE = 10

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
    print(f"Connection from {address} has been established")

    # creates a header that will tell the client how many characters of the msg they are receiving.
    # the header is the first 10 characters of the message with its contents being the len of the message
    msg = "Welcome to the server" + f" {address}!"
    msg = f'{len(msg):<{HEADER_SIZE}}' + msg

    # will ask the user what message to send to the client
    # to show the stream of data to the client
    while True:
        msg = input("Please type in something to send to the client: ")
        msg = f"{len(msg):<{HEADER_SIZE}}" + msg

        print(f"Message sent! length of message: {len(msg)}")

        # data has to be converted into bytes to be sent over the network
        # bytes() converts anything inside of it into a specific byte, here type is utf-8
        clientsocket.send(bytes(msg, "utf-8"))
