import socket
import random
import time
import sys
#HEADER_SIZE = 10

class Server:
    def __init__(self):
        #try:
            # creating socket s
            # family = AF_INET = IPV4
            # type = SOCK_STREAM = TCP
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #location = (ip, 9000)
        '''if self.s.connect_ex(location) == 0: # if this ip has port x open
        print(ip, "port OPEN")
        else:
        print(ip, "port CLOSED")'''
        self.s.bind(('', 9500))#self.s.bind((socket.gethostname(), 9500)) #first parameter either socket.gethostname() or ''
        #'' would be used for other computers that are trying to request access


        #Create lists of server's connections and peers
        self.connections = []
        self.peers = []

        # prepare a space for possible connections with a queue of 5
        self.s.listen(5)
        while True:
            clientsocket, address = self.s.accept()  # when a connection is found, store info to variables
            self.peers.append(address)
            print("Connected with ", address[0])
            '''print(socket.gethostname())
            print(clientsocket)
            print(address)'''

            clientsocket.close()

            exit()
        #self.activate()
        #except Exception as e: #if the activation fails we will exit#
            #sys.exit()

    '''def activate(self):
    # activate the server to listen forever for connections
        while True:
            clientsocket, address = self.s.accept()  # when a connection is found, store info to variables
            self.peers.append(address)
            #updates peers on which peers are conected
            self.contactPeers()
            #TODO implement threads if needed
            print("SUCCESS")
            self.connections.append(clientsocket)
            print("HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
            #print(f"Connection from {address} has been established")

            # creates a header that will tell the client how many characters of the msg they are receiving.
            # the header is the first 10 characters of the message with its contents being the len of the message
            #msg = "Welcome to the server" + f" {address}!"
            #msg = f'{len(msg):<{HEADER_SIZE}}' + msg

            # will ask the user what message to send to the client
            # to show the stream of data to the client'''
            '''while True:
                msg = input("Please type in something to send to the client: ")
                msg = f"{len(msg):<{HEADER_SIZE}}" + msg

                print(f"Message sent! length of message: {len(msg)}")

                # data has to be converted into bytes to be sent over the network
                # bytes() converts anything inside of it into a specific byte, here type is utf-8
                clientsocket.send(bytes(msg, "utf-8"))'''
    def contactPeers(self): #may not need if we are just sending a list of the peers
        #creates the list of peers in a string in order to send the data
        peerList = ""
        for i in self.peers:
            peerList = peerList + str(i[0] + ",")

        for i in self.connections:
            data = b'\x11' + bytes(peerList, 'utf-8')
            i.send(data)
    '''def disconnect(self, connection, a):
        #self.connections.remove(connection)
        #self.peers.remove(a)
        connection.close()
        #self.contactPeers()'''

temp = Server()
#create and synchronize a folder
#have folder to syncrhonize
