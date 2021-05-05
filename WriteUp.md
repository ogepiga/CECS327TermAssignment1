# Lab Writeup

### When we started the lab, our goals were:
* Create a program that establishes the connection between a server and client
* Convert that program to a Peer 2 Peer network
* Send files in the network
* Sync the files with all the nodes in the network

### How we tackled these goals:
* Create a program that establishes the connection between a server and client
    * Learned about the sockets library in Python3
    * Created simple server.py and client.py where the server would 'echo' back whatever it receives from the client
* Convert that program to a Peer 2 Peer network
    * Learned about the Peer 2 Peer network and how its nodes can act as server and client.
    * We decided to combine the files into one file and have the main() method decide when and where the nodes would acts as server or client.
        * If server disconnects from the network, make a random client become the server, then have all the active clients connect to the new server
* Send files in the network
    * Learned about the Pickle library in Python which allows most Python objects to be encoded into bytes and decoded back to their original forms
    * Used Pickle to convert our files into bytes to be sent across the network
* Sync the files with all the nodes in the network
    * Created a syncFolder which is a folder that the program detects where all files found in it will be synced with the network
    * Created a tempFolder that the server would create to hold all the files received from the clients
    * Compare and contrast tempFolder with the Server's own syncFolder and then apply the missing/changed files from the temp folder into the syncFolder
    * Send the updated syncFolder back to the clients for them to copy and paste to their tempFolders.


## Issues/Roadblocks/Errors
One issue we ran into was scanning the network. Our implementation involved opening an arp table and looking through each ip. If port 9000 was open on that ip, we open that port to go into. The problem we had was the time it took to scan the network. There were also timing issues because to check if a port is open a connection needs to be implemented.

Another issue was synchronizing the files because we technically let the server do all the work. The server takes whatever the client sends and puts it in a temporary folder. Then the server compares the syncFolder and the tempFolder. Our implementation does not check if files had the same name. Meaning that we only take in the server's versions of the file even if the client had a newer version of it. The reasoning behind this is that the server downloads the files as bytes and we did not send over meta data so in our opinion there is no point to compare.

An error that may occur depending on the system(s) used includes file corruption when the server writes new temp files to the sync file. For some reason it is only the last file of the temporary folder if its a new file.

We wrote the logic of making the client a server when the initial server logs off, however in our current version, this doesn't work because we wanted to focus on the file sharing so we never wait to see if the socket is closed and furthermore never close sockets. If given more time it is possible we just have to uncomment some lines or rewrite lines and also mess with the timing of the sockets.
