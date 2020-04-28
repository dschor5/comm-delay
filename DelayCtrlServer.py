import threading
import time
import queue
import socket
import select


class DelayCtrlServer(object):
   # DelayCtrlServer singleton instance
   __instance = None
   __THREAD_DELAY = 0.01

   def __new__(cls, ctrlPort):
      """
      Create a singleton instance of DelayCtrlServer class.
      """
      if(DelayCtrlServer.__instance is None):
         DelayCtrlServer.__instance = object.__new__(cls)
         DelayCtrlServer.__ctrlPort = ctrlPort
         DelayCtrlServer.__ctrlThread = None

         # Safe-thread sentinel to stop infinit loops.
         DelayCtrlServer.__stop       = threading.Event()

         # Start servers
         DelayCtrlServer.__proxyServers = []
         DelayCtrlServer.__instance.__startServer()

      return DelayCtrlServer.__instance


   def register(self, server):
      if(server not in self.__proxyServers):
         self.__proxyServers.append(server)

   def __startServer(self):
      if(self.__ctrlThread is not None):
         return False

      try:
         self.__stop.clear()
         self.__ctrlThread = threading.Thread(name="ctrl", target=self.__runCtrlServer, args=(self.__stop, ))
         self.__ctrlThread.start()
      except:
         print("ERROR: Could not start threads.")
         return False
      return True

   def __runCtrlServer(self, stopEvent):
      ctrlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      ctrlSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      ctrlSocket.bind(('', self.__ctrlPort))
      ctrlSocket.listen()
      ctrlSocketList = [ctrlSocket]
      ctrlClients = {}
      print("CtrlServer: Listening on port " + str(self.__ctrlPort))

      while(stopEvent.isSet() == False):
         ctrlSocketRead, _, ctrlSocketException = select.select(ctrlSocketList, [], ctrlSocketList)
         for iSocket in ctrlSocketRead:
            if(iSocket == ctrlSocket):
               iClientSocket, iClientAddress = ctrlSocket.accept()
               ctrlSocketList.append(iClientSocket)
            else:
               try:
                  msg = iClientSocket.recv(1024)
                  msgData = msg.decode("utf-8")
                  print(msgData)
                  stopEvent.set()
               except:
                  ctrlSocketList.remove(iSocket)
                  del ctrlClients[iSocket]
                  continue
         for iSocket in ctrlSocketException:
            ctrlSocketList.remove(iSocket)
            del ctrlClients[iSocket]
            continue
         time.sleep(DelayCtrlServer.__THREAD_DELAY)
      for proxy in self.__proxyServers:
         proxy.stopServer()
