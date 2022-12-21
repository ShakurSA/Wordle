import os
import socket
import threading

host = '127.0.0.1'
port = 2455

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
words = []


def broadcast(message, client):
    client.send(message.encode('koi8-r'))


def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('koi8-r')
            if message == 'конецигры':
                index = clients.index(client)
                clients.remove(clients[index])
            elif message != '':
                broadcast(message, client)
        except:
            index = clients.index(client)
            clients.remove(clients[index])
            client.close()
            break


def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        client.send('СЛОВО'.encode('koi8-r'))

        word = client.recv(1024).decode('koi8-r')
        print(word)
        words.append(word)
        clients.append(client)

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


os.system('clear')
receive()