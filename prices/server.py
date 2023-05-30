import socket
hostname = socket.gethostname()
ipAddr = socket.gethostbyname(hostname)

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((ipAddr,9999))
server.listen()

client,addr = server.accept()

done = False

while True:
    msg = (client.recv(1024).decode('utf-8'))
    print(msg)
    #client.send(input("Message: ").encode('utf-8'))
    if msg == 'stop':
        break
        client.close()
        server.close()

