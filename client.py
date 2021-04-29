import socket

HEADER_SIZE = 10

class Client:


    def __init__(self): #peer address maybe a parameter def __init__(self, ip)
        #establish the socket to use
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #attempts to connect to server
        self.s.connect((socket.gethostname(), 9500))
    '''def connect(self, ip):
        self.s.connect((ip, 9500)) #TODO might add try exception'''
    #def sendFile(self, file):
    #def recieveFile(self, file):

    '''if socket is None:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.socket = socket'''
        # FIXME figure out actual host ip
        #self.s.connect((socket.gethostname(), 1234))
    '''while True:

        full_msg = ''
        new_msg = True  # a flag to track if the current message being sent is the start of a new message
        while True:
            msg = self.s.recv(16)

            # if the message is new, the program will get the header which contains information
            # about the number of characters the msg will have.
            if new_msg:
                print(f"New message length: {msg[:HEADER_SIZE]}")
                msglen = int(msg[:HEADER_SIZE])
                new_msg = False

            full_msg += msg.decode("utf-8")

            # checks if the message has been fully decoded and prints it.
            # sets the new_msg flag back to True to be ready for the next message
            if len(full_msg) - HEADER_SIZE == msglen:
                print("Full message received:")
                print(full_msg[HEADER_SIZE:])
                new_msg = True
                full_msg = '''''
temp = Client()