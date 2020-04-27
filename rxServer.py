import socket
import select
import errno
import time
import sys

IP = "127.0.0.1"
PORT = int(sys.argv[1])

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
   # Connect to a given ip and port
   client_socket.connect((IP, PORT))

   client_socket.setblocking(True)
except:
   print("ERROR: Could not connect.")
   exit()
numMsgs = 0
while(True):
   try:
      msg = client_socket.recv(1024)
      numMsgs = numMsgs + 1
   except:
      print("ERROR: Could not receive message.")
      continue

   if(msg == b''):
      break
   try:
      msgTime  = float.fromhex(msg.decode("utf-8"))
   except:
      msgTime  = 0.0
   currTime = time.monotonic()
   print("Received message at " + str(currTime) + " with time " + str(msgTime) + " --> " + str(currTime-msgTime))
   #time.sleep(0.01)
print(numMsgs)