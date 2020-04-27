import time

class DelayPacket(object):
   def __init__(self, data):
      self.__data = data
      self.__time = time.monotonic()
      
   def getData(self):
      return self.__data
      
   def getTimestamp(self):
      return self.__time
      
   def __eq__(self, other):
      return self.__time == other.__time
      
   def __ne__(self, other):
      return self.__time != other.__time
      
   def __lt__(self, other):
      return self.__time < other.__time
      
   def __le__(self, other):
      return self.__time <= other.__time
      
   def __gt__(self, other):
      return self.__time > other.__time
      
   def __ge__(self, other):
      return self.__time >= other.__time
      
   def __str__(self):
      return "DelayPacket(time=", + str(self.__time) + ")"
      

