import time
import os
from server import Server
from client import Client

class peer2peer:
    #peers = ['127.0.0.1']
    ips = []
    with os.popen('arp -a') as f: #calls the arp table to read
        data = f.readlines()
        pointer = 0
        while pointer < len(data): #look through the arp table so we can get each line seperated
            data[pointer] = data[pointer].strip()
            if len(data[pointer]) == 0:
                del data[pointer]
                pointer -= 1
            pointer += 1

        for line in data: #loop grabs the lan's specific IP
            x = line.split()
            ip = x[0]
            # if the first character is a number than its an ip and we'll add it to our list
            if ip[0].isdigit():
                ips.append(ip)
            #print(line.split())
def main():
    '''msg = "what?"
    while True:
        try:
            print("CONNECTING")
            time.sleep(randint)'''
    listips = []
    #print(peer2peer.ips)
    timer = 0
    if timer == 0:
        tempC = Client()
    tempC = Client()
    temp = Server()
    tempC.connect(temp.revealIP())
    for ip in peer2peer.ips:
        print(ip)
        #temp = Server(ip)
    #print(listips)
main()

