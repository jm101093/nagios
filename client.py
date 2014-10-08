import socket
import time

def AlwaysTrue(data):
    print(data)
    time.sleep(1)
    sendReply(data)
    response = raw_input("Reply: ")
    if response == "exit":
        s.sendall(response1)
        s.close()

def sendReply(data):
    if data == "No Fuck You":
        s.sendall("Fuck You")
        print(data)
        time.sleep(1)
        AlwaysTrue(data)
    else:
        AlwaysTrue(data)

host = 'localhost'
port = 8080

response1 = "Closing"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print("Connected to " + (host) + " on port " + str(port))

initialMessage = "Fuck You"
s.sendall(initialMessage)
data = s.recv(1024)

while True:
    data = s.recv(1024)
    AlwaysTrue(data)

s.close()