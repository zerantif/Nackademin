import threading
import socket
import struct


HOST = '127.0.0.1'
PORT = 50007
ENCODING = 'utf-8'


class Server(threading.Thread):
    def __init__(self, host=HOST, port=PORT):
        super().__init__()
        self.connections = []                           # A list of ServerSocket objects representing the active connections.
        self.host = host                                # The IP address of the listening socket.
        self.port = port                                # The port number of the listening socket.
    
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen()
        print('Listening.', sock.getsockname())
        while True:
            sc, sockname = sock.accept()                                # Accept new connection
            print('Accepted a new connection from {} to {}'.format(sc.getpeername(), sc.getsockname()))
            server_socket = ServerSocket(sc, sockname, self)            # Create new thread
            self.add_connection(server_socket)                          # Add thread to active connections
            server_socket.start()                                       # Start new thread                           
            print('Server is ready to receive messages from', sc.getpeername())

    def broadcast(self, client_name, message, source):          # Sends a message to all connected clients except the source
        for connection in self.connections:
            if connection.sockname != source:
                connection.send(f"{client_name}: {message}")

    def close_all_connections(self):
        for connection in self.connections:                     # Server attempt to close all client connections
            try:
                connection.sc.close()
            except ConnectionResetError:
                pass

    def add_connection(self, connection):
        self.connections.append(connection)

    def remove_connection(self, connection):
        self.connections.remove(connection)

    def handle_client_command(self, server_socket, command):
        command = command.split()                               # Split command and arguments into list
        if command[0] == "users":                               # Send a list of user to the user
            s = "List of connected users:\n"
            for c in self.connections:
                s = s + f"  - {c.client_name}\n"
            server_socket.send(s)
            return
        if command[0] == "sendpm":                              # Send private message to a user
            print(f"User wants to send sendpm")
            for c in self.connections:
                if c.client_name == command[1]:
                    c.send(f"Private message from {server_socket.client_name}: {' '.join(command[2:])}")
                    return
            server_socket.send("No such user!")
            return
        if command[0] == "sendimg":                              # sender -> server:     !sendimg <filename> [<recipient>]
            print(f"User wants to send a img")                   # server -> recipient:  !imgstart <sender> <filename>
            file_name = command[1]
            recipient = command[2] if len(command) > 2 else None
            self._distribute_command(server_socket.client_name, recipient, '!imgstart', file_name)
            return
        
        # sender -> server:    !imgdata [<recipient>] <first nnn bytes>
        # server -> recipient  !imgdata <sender> <first nnn bytes>
        # sender -> server:    !imgdata [<recipient>] <next nnn bytes...>
        # server -> recipient  !imgdata <sender> <next nnn bytes...>
        if command[0] == "imgdata":
            if len(command) == 2:                                       # Send to everyone / !imgdata <data bytes>
                recipient = None
                file_data = command[1]
            else:
                if len(command) == 3:                                   # Send to specific user / !imgdata <recipient> <data bytes>
                    recipient = command[1]
                    file_data = command[2]
                else:
                    print("Protocol error - incorrect number of arguments.")
            self._distribute_command(server_socket.client_name, recipient, '!imgdata', file_data)   # !imgdata <sender> <next nnn bytes>
            return

        if command[0] == "imgend":                                      # sender -> server       !imgend [<recipient>]
            recipient = command[1] if len(command) > 1 else None        # server -> recipient    !imgend <sender>
            self._distribute_command(server_socket.client_name, recipient, '!imgend', '')
            return
        server_socket.send("No such command!")

    def _distribute_command(self, sender, recipient, command, data):
        for c in self.connections:
            if recipient:
                if c.client_name == recipient:                              # Named recipient
                    c.send(f'{command} {sender} {data}')
                    return
            else:                                                           # Send to everyone
                c.send(f'{command} {sender} {data}')


class ServerSocket(threading.Thread):
    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc = sc                                                        # sc (socket.socket): The connected socket.
        self.sockname = sockname                                            # sockname (tuple): The client socket address.
        self.server = server                                                # server (Server): The parent thread.
        self.client_name = None

    def run(self):
        try:
            while True:
                message_length = struct.unpack('H', self.sc.recv(2))[0]     # Read message length
                message = b''
                while message_length > 0:                                   # Read entire message into the "message" variable
                    data_read = self.sc.recv(message_length)
                    message = message + data_read
                    message_length = message_length - len(data_read)
                message = message.decode()
                if self.client_name == None:
                    self.client_name = message                              # Store client name
                else:
                    if message:
                        if message[0:1] == "!":                             # Handle commando
                            self.server.handle_client_command(self, message[1:])
                        
                        else:
                            print('{} says [{}]'.format(self.sockname, message))    # Say to all connected
                            self.server.broadcast(self.client_name, message, self.sockname)
                    else:
                        raise ConnectionResetError()
        except ConnectionResetError:
                print('{} has disconnected'.format(self.sockname))
                self.server.remove_connection(self)
                self.sc.close()
                return

    def send(self, message):                                  # Sends a message to the connected server
        message = f'{message}'.encode()
        self.sc.sendall(struct.pack("H",len(message)))
        self.sc.sendall(message)

def exit(server):                                             # Allows the admin to shut down server
    while True:
        ipt = input('')
        if ipt == 'q':
            print('Disconnecting.')
            server.close_all_connections()
            print('Server shutdown.')
            return


if __name__ == '__main__':
    main_server = Server()       # Create and start server thread
    main_server.start()

    exit = threading.Thread(target = exit, args = (main_server,))
    exit.start()
    exit.join()
