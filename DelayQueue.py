import queue
import time
import DelayPacket
import DelayFunction

# TODO - Cache last value found at teh top of the queue

class DelayQueue(object):

   def __init__(self):
      self.__queue = queue.PriorityQueue()
      self.__delay = DelayFunction.DelayFunction()
      self.__size  = 0
      
   def getMsg(self):
      if(self.__queue.empty()):
         return None
      msg = self.__queue.get()
      if(msg is None):
         print("Invalid message.")
         return None
      currTime = time.monotonic()
      delay    = self.__delay.getDelay(currTime)

      if((msg.getTimestamp() + delay) > currTime):
         self.__queue.put(msg)
         return None
      self.__size = self.__size - 1
      return msg.getData()
   
   def putMsg(self, msg):
      newMsg = DelayPacket.DelayPacket(msg)
      self.__queue.put(newMsg)
      self.__size = self.__size + 1
      
   def __str__(self):
      return "DelayQueue(size=" + str(self.__size) + ")"

   