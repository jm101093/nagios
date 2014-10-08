import socket

host = '10.0.1.38'
port = 8080

response1 = "Closing"

def AlwaysTrue():
    data = s.recv(1024)
    print(data)
    sendReply(data)
    response = raw_input("Reply: ")
    if response == "exit":
        s.sendall(response1)
        s.close()
        break

def sendReply(data):
    if data == "work":
        s.sendall("work")
        print "sending data"
        AlwaysTrue()
    else:
        AlwaysTrue()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print("Connected to " + (host) + " on port " + str(port))
initialMessage = raw_input("Send: ")
s.sendall(initialMessage)
AlwaysTrue()
s.close()