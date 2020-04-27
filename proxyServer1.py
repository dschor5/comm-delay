import threading
import time
import queue
import socket
import select

class DelayServer(object):
   """
   Delay Server
   
   Acts as a proxy that adds delays to all communicaitons.
   """
   
   # DelayServer Singleton instance
   __instance = None
   
   # Constants
   