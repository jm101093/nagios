import socket
import time
import os

#kinda does nothing at the moment
def formatData(data):
    while True:
        #print(data)
        #conn.sendall(data)
        replyBack(data)
#replys
def replyBack (data):
    #print(data)
    if data  == "Fuck You":
        print("Fuck You")
        client.send("No Fuck You")
        time.sleep(1)
        #s.sendall("work")
    else:
        print("Recieved: " + (data))
#attempt at making this thing retry connection
def connect(host, port):
    s.bind((host, port))
    s.listen(1)
    (client,(ip,port)) = s.accept()
    data = client.recv(1024)
    formatData(data)

host = 'localhost'
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
(client,(ip,port)) = s.accept()

print ("Connection from", client,ip,port)
data = client.recv(1024)
formatData(data)

if not data:
    connect(host,port)
#conn.sendall(data)
client.close()


    #response = raw_input("Reply: ")

    #if response == "exit":
    #    break