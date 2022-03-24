import threading
import socket

HOST = '192.168.0.163'
PORT = 55555
FORMAT = 'utf-8'
USERNAME = input("Enter your user name: ")
END = False


def receive_msg():
    global END
    while not END:
        print(client_socket.recv(1024).decode(FORMAT))


def send_msg():
    global END
    while not END:
        message = input()
        if message == '!QUIT':
            close()
        else:
            client_socket.send(message.encode(FORMAT))


def close():
    global END
    END = True
    client_socket.send('!QUIT'.encode(FORMAT))
    print('[COMPUTER]: Connection to server terminated.')


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print('[COMPUTER]: Connecting to server')
client_socket.send(USERNAME.encode(FORMAT))
receive_msg_thread = threading.Thread(target=receive_msg,)
receive_msg_thread.start()
send_msg_thread = threading.Thread(target=send_msg,)
send_msg_thread.start()
