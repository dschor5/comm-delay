import threading
import time
import queue
import socket
import select

MSG_SIZE    = 4096

BUFFER_SIZE = 10
q = queue.Queue(BUFFER_SIZE)

class ServerProducerThread(threading.Tread):
    def __init__(self, ip='127.0.0.1', port=1234, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(ServerProducerThread, self).__init__()
        self.target = target
        self.name   = name
        self.ip     = ip
        self.port   = port
      
   def run(self):
   
    # Create a socket
    # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
    # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # SO_ - socket option
    # SOL_ - socket option level
    # Sets REUSEADDR (as a socket option) to 1 on socket
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind, so server informs operating system that it's going to use given IP and port
    # For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to 127.0.0.1 and remotely to LAN interface IP
    serverSocket.bind((self.ip, self.port))

    # This makes server listen to new connections
    serverSocket.listen()

    # List of sockets for select.select()
    socketList = [serverSocket]

    # List of clients connected
    clients = {}

    while(True):
        # Calls Unix select() system call or Windows select() WinSock call with three parameters:
        #   - rlist - sockets to be monitored for incoming data
        #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
        #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
        # Returns lists:
        #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
        #   - writing - sockets ready for data to be send thru them
        #   - errors  - sockets with some exceptions
        # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
        readSockets, _, exceptionSockets = select.select(socketList, [], socketList)

        # Iterate over notified sockets
        for notifiedSocket in readSockets:
         
            # If notifiedSocket is a server socket --> new connection to accept
            if(notifiedSocket == serverSocket):
               
                # Accept new connection.
                clientSocket, clientAddress = serverSocket.accept()

                # Other handshake info?
                # e.g., client sends its username
                # If this fails, assume the client disconnected

                # Add accepted socket to select.select() list
                socketList.append(clientSocket)
            
            # Else, existing socket is sending a message
            else:
               
                try:
                    # Receive message
                    msg = clientSocket.recv(MSG_SIZE)
                    q.put(msg)
                except:
                    # Client connection lost. 
                    socketList.remove(notifiedSocket)
                    del clients[notifiedSocket]
                    continue
            
        for notifiedSocket in exceptionSockets:
            socketList.remove(notifiedSocket)
            del clients[notifiedSocket]
               
               
class ClientConsumerThread(threading.Tread): 
    def __init__(self, ip='127.0.0.1', port=1234, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(ClientConsumerThread, self).__init__()
        self.target = target
        self.name   = name
        self.ip     = ip
        self.port   = port
        return
      
    def run(self):
        # Create a socket
        # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
        # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to a given ip and port
        client_socket.connect((self.ip, self.port))

        # Set connection to non-blocking state, so .recv() call won't block, just return some exception we'll handle
        client_socket.setblocking(False)

        
   