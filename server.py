import os
import socket
import threading

host = '127.0.0.1'
port = 5345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
words = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('koi8-r')
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            break


def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        client.send('WORD'.encode('koi8-r'))

        word = client.recv(1024).decode('koi8-r')
        words.append(word)
        clients.append(client)


        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


os.system('clear')
receive()