import socket
import time
import os

host = 'localhost'
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
(client,(ip,port)) = s.accept()

def formatData(data):
    while True:
        #print(data)
        #conn.sendall(data)
        replyBack(data)

def replyBack (data):
    #print(data)
    if data  == "Fuck You":
        print("Fuck You")
        client.send("No Fuck You")
        time.sleep(1)
        #s.sendall("work")
    else:
        print("Recieved: " + (data))

print ("Connection from", client,ip,port)
data = client.recv(1024)
formatData(data)

#if not data: break
#conn.sendall(data)
client.close()


    #response = raw_input("Reply: ")

    #if response == "exit":
    #    break