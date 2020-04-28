import threading
import time
import queue
import socket
import select

import DelayCtrlServer
import DelayQueue
import DelayPacket

class DelayServer(object):
   """
   Delay Server

   Acts as a proxy that adds a time delays to all messages.
   Messages --> rxThread --> [DELAY] --> txThread --> Message.
   Implemented as a multi-threaded producer/consumer design pattern.
   """

   # Constants
   __THREAD_DELAY = 0.01

   def __init__(self, rxPort, txPort, ctrlPort=0):
      """
      Initialize variables, start the server, and register it with
      the controller.
      """

      # Port to receive messages
      self.__rxPort     = rxPort
      self.__rxThread   = None

      # Port to transmit messages
      self.__txPort     = txPort
      self.__txThread   = None

      # Control server that allows operators to change the delays
      # or exit the program.
      self.__ctrlServer = DelayCtrlServer.DelayCtrlServer(ctrlPort)

      # Thread-safe sentinel to stop infinit loops.
      self.__stop       = threading.Event()

      # Thread-safe message queue used by the producer-consumer pair.
      self.__msgQueue   = DelayQueue.DelayQueue()

      # Start server and register it with the controller.
      if(self.__startServer() == True):
         self.__ctrlServer.register(self)


   def __startServer(self):
      """
      Start rxThread and txThread.
      """

      # Prevent starting the same server more than once.
      if(self.__rxThread is not None and self.__txThread is not None):
         return False

      # Set sentinel to start servers.
      try:
         self.__stop.clear()
      except:
         print("ERROR: Could not create sentinel for server.")
         return False

      # Start rxThread.
      try:
         self.__rxThread = threading.Thread(name="rx", target=self.__runRxServer, args=(self.__stop, self.__msgQueue))
         self.__rxThread.start()
      except:
         print("ERROR: Could not start rxThread on port ", str(self.__rxPort))
         self.__stop.set()
         return False

      # Start txThread.
      try:
         self.__txThread = threading.Thread(name="tx", target=self.__runTxServer, args=(self.__stop, self.__msgQueue))
         self.__txThread.start()
      except:
         print("ERROR: Could not start txThread on port ", str(self.__txPort))
         self.__stop.set()
         return False

      return True


   def stopServer(self):
      """
      Stop server and wait for all theads to finish.
      """

      # Ensure threads are running.
      if(self.__rxThread is None and self.__txThread is None):
         return False

      # Set flag to stop server threads.
      self.__stop.set()
      print("Stopping server.")

      # Join all threads.
      try:
         self.__rxThread.join()
         self.__txThread.join()
      except:
         return False
      return True

   def __runRxServer(self, stopEvent, msgQueue):
      rxSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      rxSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      rxSocket.bind(('', self.__rxPort))
      rxSocket.listen()
      rxSocketList = [rxSocket]
      rxClients = {}
      print("RxServer: Listening on port " + str(self.__rxPort))

      while(stopEvent.isSet() == False):
         rxSocketRead, _, rxSocketException = select.select(rxSocketList, [], rxSocketList, 0)
         for iSocket in rxSocketRead:
            if(iSocket == rxSocket):
               iClientSocket, iClientAddress = rxSocket.accept()
               rxSocketList.append(iClientSocket)
               print("RxServer: New connection from " + str(iClientAddress))
            else:
               try:
                  msg = iClientSocket.recv(1024)
                  if(msg):
                     #print("RxServer: putMsg() = " + str(msg))
                     msgQueue.putMsg(msg)
               except:
                  rxSocketList.remove(iSocket)
                  del rxClient[iSocket]
                  continue
         for iSocket in rxSocketException:
            rxSocketList.remove(iSocket)
            del rxClients[iSocket]
            continue
         time.sleep(DelayServer.__THREAD_DELAY)


   def __runTxServer(self, stopEvent, msgQueue):
      txSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      txSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      txSocket.bind(('', self.__txPort))
      txSocket.listen()
      txSocketList = [txSocket]
      txClients = {}
      print("TxServer: Listening on port " + str(self.__txPort))

      while(stopEvent.isSet() == False):
         txSocketRead, _, txSocketException = select.select(txSocketList, [], txSocketList, 0)
         for iSocket in txSocketRead:
            if(iSocket == txSocket):
               iClientSocket, iClientAddress = txSocket.accept()
               txSocketList.append(iClientSocket)
               print("TxServer: New connection from " + str(iClientAddress))
         msg = msgQueue.getMsg()
         while(msg is not None):
            #print("TxServer: getMsg() = " + str(msg))
            if(len(txSocketList) == 1):
               print("TxServer: discardig msg.")
            else:
               for iSocket in txSocketList:
                  if(iSocket != txSocket):
                     #print(iSocket)
                     try:
                        iSocket.send(msg)
                     except:
                        break
            msg = msgQueue.getMsg()
         for iSocket in txSocketException:
            txSocketList.remove(iSocket)
            del txClients[iSocket]
            continue

         time.sleep(DelayServer.__THREAD_DELAY)


time.sleep(10)
DelayCtrlServer.DelayCtrlServer(1003)
ds = DelayServer(1001, 1002)
#ds = DelayServer(2001, 2002)
