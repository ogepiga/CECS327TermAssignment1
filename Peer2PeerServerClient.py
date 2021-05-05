import socket
import threading
import sys
import time
from random import randint
import os
import pickle
import filecmp
import shutil
SEPARATOR = "SEPARATOR"
HEADER_SIZE = 10


class Server:
    connections = []
    peers = []

    '''
    Initializer for the Server class
    '''
    def __init__(self, folderPath):
        # create tempFolder for storage of all client's files to be synced
        folderName = "TempFolder" # the folder name where the files will be stored
        currentDirectory = os.getcwd()  # gets the path of where the program is in.
        tempPath = currentDirectory + "\\" + folderName
        try:
            os.makedirs(tempPath)  # attempt to create a folder
        except FileExistsError:  # if the folder exists
            # clear the folder if there are contents in it
            for f in os.listdir(tempPath):
                os.remove(os.path.join(tempPath, f))
            pass
        except OSError:  # if any OS errors occurs
            pass
        # create a listening server socket to accept client connections
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # allows the socket to be reusable
        sock.bind(('0.0.0.0', 9000))
        sock.listen(1)  # listen for incoming connections and have a queue of 1
        print("Server running...")

        while True:
            c, a = sock.accept()  # accept the connection and store connection info on c and address info on a
            # creating a new thread for handler(c, a) method.

            # cThread = threading.Thread(target=self.handler, args=(c, a))
            cThread = threading.Thread(target=self.receiveClientFolder, args=(c, tempPath, folderPath))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)  # add the new connection to the connection list
            self.peers.append(a[0])  # add the address of the new connection to the peers list
            print(str(a[0]) + ':' + str(a[1]), "connected.")
            #self.send_peers()

    '''
    Handles sending information from the server to the clients
    '''
    def handler(self, c, a):
        while True:
            data = c.recv(1024)
            # send information received to all clients
            for connection in self.connections:
                connection.send(data)
            # send the information of the client that just disconnected to all the clients
            # and update and send the peers list to all the clients
            if not data:
                print(str(a[0]) + ':' + str(a[1]), "disconnected.")
                # remove information from client/peers list
                self.connections.remove(c)
                self.peers.remove(a[0])
                c.close()  # close connection
                self.send_peers()  # send the peer list to the clients
                break

    def receiveClientFolder(self, c, tempPath, syncPath):
        data = c.recv(1024)
        dataLength = int(data[:HEADER_SIZE])
        # if the data is less than the expected size, that means more data is still needed to be received
        while (len(data) - HEADER_SIZE) < dataLength:
            msg = c.recv(1024)
            data += msg

        dataList = pickle.loads(data[HEADER_SIZE:])
        # this should be the number that the client sends before sending any file
        # this number denotes the number of files the client is about to send
        # if we are prompted that a client has an empty folder
        # send that client the server's folder
        if len(dataList) == 0:
            # self.sendFolder(folderPath)
            print("folder empty bruh")
        else:
            for tempList in dataList:
                # receivedFile = c.recv(1024).decode('utf-8')
                # filename, filesize = receivedFile.split(SEPARATOR)
                filename = tempList[0]  # receive the file name
                filesize = tempList[1]  # receive the file size
                tempName = os.path.join(tempPath, filename)
                f = open(tempName, 'wb')  # create a temp file to write the bytes that the client is sending
                f.write(tempList[2])  # write the file contents onto the temp file
        self.compareFolderFiles(c, tempPath, syncPath)
        
    '''
    This function will compare its files to what was sent
    If we have a copy of a file name we always assume the server
    is right. We just take in file names that is not in the syncFolder
    and add it to the syncFolder so we can send it back
    '''
    def compareFolderFiles(self, c, tempPath, syncPath):
        #create a comparison object to have lists of both paths
        comparison = filecmp.dircmp(tempPath, syncPath)
        tempFileNames = comparison.left_list
        syncFileNames = comparison.right_list
        '''print(tempFileNames)
        print(syncFileNames)'''
        #for each file in the tempFolder
        for i in tempFileNames:
            #if a file is not in the syncFolder
            if i not in syncFileNames:
                #we are going to open the file and rewrite in the syncFolder
                with open(tempPath + "\\" + i, 'rb') as f:
                    data = f.read()
                    with open(syncPath + "\\" + i, 'wb') as f1:
                        f1.write(data)

        self.sendSyncFolder(c, syncPath)

                #os.system("copy "+tempPath+"\\"+i+" "+syncPath+"\\")
                #os.rename((tempPath+"\\"+i), (syncPath+"\\"+i))

                #or we use shutil to copy
                #shutil.copy2((tempPath+"\\"+i), (syncPath+"\\"), follow_symlinks=False)
                #add that file to the syncFolder

    '''
    This function will now send back the syncFolder to the client
    '''
    def sendSyncFolder(self, c, syncPath):
        syncFolder = os.listdir(syncPath)
        dataList = [] #list containing lists of file info
        for file in syncFolder:
            tempList = []
            tempList.append(file) #tempList[0] = file name
            fileSize = os.path.getsize(syncPath+"\\"+file)
            tempList.append(fileSize) #tempList[1] = file size
            with open(syncPath+"\\"+file, "rb") as f:
                tempList.append(f.read(tempList[1])) #tempList[2] = file contents
            dataList.append(tempList)
        pickledList = pickle.dumps(dataList)
        msg = bytes(f'{len(pickledList):<{HEADER_SIZE}}', "utf-8") + pickledList
        print("SERVER SENDING NEW FOLDER")
        c.send(msg)
        #c.close()
    
    '''
    Sends the peer list to other clients by sending a list of the currently connected clients'
    ip addresses.
    '''
    def send_peers(self):
        p = ""
        # create the string of information
        for peer in self.peers:
            p = p + peer + ","
        # send the information to the clients in the connection list
        # append byte '\x11' to the beginning of the message so that clients will know that
        # the information being received is peer list info
        for connection in self.connections:
            connection.send(b'\x11' + bytes(p, 'utf-8'))

class Client:
    '''
    Initializer for the Client class
    '''
    def __init__(self, address, folderPath, folderContents):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create Socket
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # flag for socket to be reused
        sock.connect((address, 9000))  # connect socket
        print("Connected to", address)
        # Create a new thread so the client can send messages while receiving data
        iThread = threading.Thread(target=self.giveFolder, args=(sock, folderPath, folderContents))
        iThread.daemon = True
        iThread.start()
        '''while True:
            data = sock.recv(1024)
            if not data:
                break
            if data[0:1] == b'\x11':  # checks if the data holds peer list information
                self.updatePeers(data[1:])
            else:
                print(str(data, 'utf-8'))'''

    # FIXME file sending will probably happen here
    def giveFolder(self, sock, folderPath, folderContents):
        dataList = []
        for file in folderContents:
            tempList = []
            tempList.append(file)  # tempList[0] = file name
            fileSize = os.path.getsize(folderPath+"\\"+file)
            tempList.append(fileSize)  # tempList[1] =  file size
            with open(folderPath+"\\"+file, "rb") as f:
                tempList.append(f.read(tempList[1]))  # tempList[2] = file contents in bytes
            dataList.append(tempList)
        # FIXME self.getFolder(folderPath)
        pickledList = pickle.dumps(dataList)  # pickle dataList
        msg = bytes(f'{len(pickledList):<{HEADER_SIZE}}', "utf-8") + pickledList
        sock.send(msg)  # send the list
        self.getServerFolder(sock, folderPath)

    def getServerFolder(self,sock, path):
        # first loop to remove all files in folder that was sent
        # to receieve the servers sync file
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))
        data = sock.recv(1024)
        dataLength = int(data[:HEADER_SIZE])
        while (len(data) - HEADER_SIZE) < dataLength:
            msg = sock.recv(1024)
            data += msg

        dataList = pickle.loads(data[HEADER_SIZE:])
        print("DATA RECEIVED,")
        print(dataList)
        if len(dataList) == 0:
            print("Folder empty")
        else:
            for tempList in dataList:
                filename = tempList[0]
                filesize = tempList[1]
                tempName = os.path.join(path, filename)
                f = open(tempName, 'wb')
                f.write(tempList[2])
        #close the connection
        # TODO write logic to take in each file

    '''
    Sends a message to the server
    '''
    '''def sendMsg(self, sock):
        # sends a user input message and is converted to utf-8
        while True:
            sock.send(bytes(input("Message: "), 'utf-8'))'''

    '''
    updates the peers list in the p2p class
    '''

    def updatePeers(self, peerData):
        # updates the list of peers cno
        p2p.peers = str(peerData, "utf-8").split(",")[:-1]


class p2p:
    peers = []  # peer list is its own class so that both client and server can have access to it


'''
Creates a folder named "SyncFolder", which is a folder that contains the files that will be synced
amongst the peers in the network. If the folder already exists, it won't make another.
'''
def findFolder(name):
    folderName = name  # the folder name where the files will be stored
    currentDirectory = os.getcwd()  # gets the path of where the program is in.
    path = currentDirectory + "\\" + folderName
    print("Checking for folder \"%s\"" % folderName)
    try:
        os.makedirs(path)  # attempt to create a folder
    except FileExistsError:  # if the folder exists
        print("Directory \"%s\" detected" % path)
    except OSError:  # if any error occurs
        print("Creation of the directory \"%s\" failed" % path)
    else:
        print("Successfully created the directory \"%s\"" % path)

    contents = os.listdir(path)  # get the contents in syncFolder
    print("Contents of %s: " % folderName)
    if len(contents) == 0:  # check if folder has nothing in it
        print("(No files detected)")
    else:
        for content in contents:  # prints the contents within sync folder
            print(content)
    return path, contents


def main():
    while True:
        syncPath, syncContents = findFolder("SyncFolder")
        print("\n# System Info #\nSystem Name: %s\nIP Address: %s"
              % (socket.gethostname(), socket.gethostbyname(socket.gethostname())))
        attemptToConnect = input("\nIP to attempt to connect to: ")
        p2p.peers.append(attemptToConnect)
        # time.sleep(randint(1, 10))
        for peer in p2p.peers:
            try:
                client = Client(peer, syncPath, syncContents)
            except KeyboardInterrupt:
                sys.exit(0)
            except ConnectionRefusedError:
                print("Connection was refused.")
            except TimeoutError:
                print("Connection timed out.")
            except OSError:
                print("Requested address is not valid in its context.")

            # become server if disconnected from client or unable to become client
            try:
                server = Server(syncPath)
            except KeyboardInterrupt:
                sys.exit(0)

main()
