import socket
import select
import errno
import sys

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = int(sys.argv[1])

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
   # Connect to a given ip and port
   client_socket.connect((IP, PORT))

   # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
   client_socket.setblocking(False)

   client_socket.send(b"Hello World!")
except:
   print("ERROR: Could not send message.")
