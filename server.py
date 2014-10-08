import socket

host = '10.0.1.38'
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
conn, addr = s.accept()

print ("Connection from", addr)

while True:
    data = conn.recv(1024)
    if data == "work":
        print("work")
        conn.sendall("work")
        s.sendall("work")
    else:
        print("Recieved: " + (data))

    if not data: break

    response = raw_input("Reply: ")
    if response == "exit":
        break

    conn.sendall(response)
conn.close()