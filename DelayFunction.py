import time
import math

#TODO Make singleton

class DelayFunction(object):
   
   # DelayFunction singleton instance
   __instance = None
   
   def __new__(cls):
      if(DelayFunction.__instance is None):
         DelayFunction.__instance = object.__new__(cls)
         DelayFunction.__metZero = time.monotonic()
         DelayFunction.__delay = 5
         print(DelayFunction.__metZero)
         print(DelayFunction.__delay)
      return DelayFunction.__instance

   def getDelay(self, currTime):
      met = currTime - self.__metZero
      #if(met < 10):
      #   self.__delay = 5
      #else:
      #   self.__delay = 5 - math.floor(met) * 0.1
      #   if(self.__delay < 0):
      #      self.__delay = 0
      return self.__delay
      
   def __str__(self):
      return "DelayFunction(delay=" + str(self.__delay) + ")"
      