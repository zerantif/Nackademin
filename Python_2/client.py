import socket
import threading
import os
import struct
import base64
import io
from PIL import Image

HOST = '127.0.0.1'
PORT = 50007
ENCODING = 'utf-8'

class Send(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock                                  # sock (socket.socket): The connected socket object
        self.name = name                                  # name (str): The username provided by the user
        self.is_running = True
    
    def send_to_server(self, message):
        if message == '!quit':                                            # Type !quit to leave the chatroom
            self.send('Server: {} has left the chat.'.format(self.name))
            return False
        if message[0:8] == "!sendimg":                                    # sender -> server:     !sendimg <filename> [<recipient>]
            message = message.split()
            file_name = message[1]
            if os.path.exists(file_name):                                 # Check if file exists, otherwise abort
                if len(message) > 2:
                    self.send(f"!sendimg {file_name} {message[2]}")
                else:
                    self.send(f"!sendimg {file_name}")
            else:
                print(f"ERROR: File [{file_name}] doesn't exist.")
                return True

            with open(file_name, 'rb') as f:                              # Enter into loop sending parts of file (!imgdata) to server.
                while True:                                               # sender -> server:    !imgdata [<recipient>] <first nnn bytes>
                    data_read = f.read(16384)
                    if not data_read:
                        break

                    data_read_b64 = base64.b64encode(data_read).decode()
                    if len(message) > 2:
                        self.send(f"!imgdata {message[2]} {data_read_b64}")
                    else:
                        self.send(f"!imgdata {data_read_b64}")

            if len(message) > 2:                                        # Send EOF condition (!imgend) to server.
                self.send(f"!imgend {message[2]}")                      # sender -> server       !imgend [<recipient>]
            else:
                self.send(f"!imgend")

        else:                                                           # Send message to server for broadcasting
            self.send(message)
        return True

    def run(self):
        self.send(self.name)                                            # Tell server our username
        while self.is_running:
            message = input('{}: '.format(self.name))
            if message:
                if not self.send_to_server(message):
                    break
        print('\nBye bye.')
        self.sock.close()
        os._exit(0)

    def send(self, message):
        message = f'{message}'.encode()
        self.sock.sendall(struct.pack("H",len(message)))
        self.sock.sendall(message)


class Receive(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.images_in_flight = {}
    
    def recv_from_server(self, message):
        if message[0] == '!':                                            # This is a command from the server
            message = message[1:].split()
            if message[0] == 'imgstart':                                 # server -> recipient  !imgstart <sender> <filename>
                sender = message[1]                                      # Create data structure
                file_name = message[2]
                self.images_in_flight[sender] = {}
                self.images_in_flight[sender]['filename'] = file_name
                self.images_in_flight[sender]['data'] = b''
            if message[0] == 'imgdata':                                  # Append data to "in-flight" data structure
                sender = message[1]                                      # server -> recipient  !imgdata <sender> <base64 encoded data...>
                data_b64 = message[2]
                data = base64.b64decode(data_b64)
                self.images_in_flight[sender]['data'] = self.images_in_flight[sender]['data'] + data
            if message[0] == 'imgend':                                   # server -> recipient  !imgend <sender>
                sender = message[1]
                file_name = self.images_in_flight[sender]['filename']
                print(f"Recieved image from {sender}, filename: {file_name}.") # Print image details                          
                image = Image.open(io.BytesIO(self.images_in_flight[sender]['data'])) # Show image to user 
                image.show()
                del self.images_in_flight[sender]
        else:
            print(f'\r{message}\n{self.name}: ', end = '')


    def run(self):
        while True:
            try:
                message_length = struct.unpack('H', self.sock.recv(2))[0]   # Read message length
                message = b''
                while message_length > 0:                                   # Read entire message into the "message" variable
                    data_read = self.sock.recv(message_length)
                    message = message + data_read
                    message_length = message_length - len(data_read)
                message = message.decode()

                if message:
                    self.recv_from_server(message)
                else:
                    break
            except ConnectionResetError:
                break

        print('\nServer connection lost.')                                  # Server has closed the socket, exit the program
        print('\nQuit.')


class Client:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def start(self):
        self.sock.connect((self.host, self.port))
        print(f'Connected to {self.host}:{self.port}')
        name = input('Enter your nickname: ')
        print(f'\nWelcome, {name}!\n')
        print("""Commandos:
    !users                              List users
    !sendpm <mottagare> <meddelande>    Send PM to a client
    !sendimg <filnamn> [<mottagare>]    Send a img to all or <mottagare>
    !quit                               Exit client
    """)
        send = Send(self.sock, name)                                       # Create send and receive threads
        receive = Receive(self.sock, name)
        send.start()                                                       # Start send and receive threads
        receive.start()
        send.send(f'{name} joined the chat!')
        receive.join()
        send.is_running = False

if __name__ == '__main__':
    client = Client()
    client.start()
