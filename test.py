import threading
import time

def testFunc(num):
    print("start: " + str(num))
    time.sleep(5)
    print("end: " + str(num))

testThread1 = threading.Thread(name="ctrl", target=testFunc, args=(1,))
testThread2 = threading.Thread(name="ctrl", target=testFunc, args=(2,))
testThread1.start()
testThread2.start()
