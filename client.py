import threading
import socket

HOST = '**********'    # Add the ip address of the server you would like to connect to.
PORT = 55555
FORMAT = 'utf-8'
USERNAME = input("Enter your user name: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print('[COMPUTER]: Connecting to server')
client_socket.send(USERNAME.encode(FORMAT))

def receive_msg():
    while True:
        print(client_socket.recv(1024).decode(FORMAT))


def send_msg():
    while True:
        message = input()
        if message == '!QUIT':
            close()


receive_msg_thread = threading.Thread(target=receive_msg)
receive_msg_thread.start()

send_msg_thread = threading.Thread(target=send_msg)
send_msg_thread.start()


def close():
    receive_msg_thread.join()
    send_msg_thread.join()
    client_socket.send('!QUIT'.encode(FORMAT))
    print('[COMPUTER]: Connection to server terminated.')
