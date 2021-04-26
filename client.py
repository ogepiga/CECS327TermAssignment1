import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

# s.recv(x) receives information with a buffer size of x bytes
msg = s.recv(1024)
# .decode(s) converts the x type bytes into what they were before being sent through bytes()
print(msg.decode("utf-8"))