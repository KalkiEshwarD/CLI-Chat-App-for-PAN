import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 55555
FORMAT = 'utf-8'
CLIENTS = []
USER_NAMES = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print('Server is listening...')


def receive_msg(client, username):
    while True:
        try:
            message = client.recv(1024).decode()
            if message == '!QUIT':
                client.close()
                print(f'[SERVER]: {username} has left the chat room.')
                CLIENTS.remove(client)
                USER_NAMES.remove(username)
                broadcast(f'{username} has left the chat room.', '[SERVER]')
                break
            else:
                broadcast(message, username)
        except:
            try:
                client.close()
                broadcast(f'{username} has left the chat room.', '[SERVER]')
                print(f'[SERVER]: {username} has left the server.')
            except:
                break


def broadcast(message, username):
    for client in CLIENTS:
        client.send(f'{username}: {message}'.encode(FORMAT))


def on_boarding():
    while True:
        connection, address = server_socket.accept()
        CLIENTS.append(connection)
        connection.send('[SERVER]: Connected to server.\n'.encode(FORMAT))
        user_name = connection.recv(1024).decode()
        print(f'{user_name} with address {address} has connected to the server.')
        USER_NAMES.append(user_name)
        broadcast(f'{user_name} has joined the server.', '[SERVER]')
        receive_msg_thread = threading.Thread(target=receive_msg, args=(connection, user_name,))
        receive_msg_thread.start()


on_boarding()
