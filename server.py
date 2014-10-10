import socket
import time
import os

host = 'localhost'
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
conn, addr = s.accept()

def replyBack (data):
    print(data)
    if data  == "Fuck You":
        print("Fuck You")
        conn.sendall("No Fuck You")
        time.sleep(1)
        #s.sendall("work")
    else:
        print("Recieved: " + (data))

print ("Connection from", addr)

#if not data: break

while True:
    data = conn.recv(1024)
    replyBack(data)
    print("test")
    break
    #response = raw_input("Reply: ")

    #if response == "exit":
    #    break
    conn.sendall(data)
conn.close()