import time
from communication import MessageBroker, Publisher, Subscriber

# WIP
# This will soon be replaced with a mock implementation of the real
# coordinator which will manage interaction between the input and output
# modules of the application.

def speech_handler(msg):
    print("Speech handler received {}".format(msg))

def openpose_handler(msg):
    print("OpenPose handler received {}".format(msg))

# Start broker listening on 4000 for messages and redistributing on 4001
broker = MessageBroker("4000", "4001")
broker.start()

# Prepare publishers and subscribers
in1 = Publisher("localhost", "4000", "speech")
in2 = Publisher("localhost", "4000", "openpose")
out1 = Subscriber("localhost", "4001", "speech", speech_handler)
out2 = Subscriber("localhost", "4001", "openpose", openpose_handler)
# Start subscribers
out1.start()
out2.start()
time.sleep(1)

# User said to start recording
in1.send("Record")
time.sleep(1)
# User looked in other camera
in2.send("Switch to cam2")
time.sleep(2)
# User said to stop recording
in1.send("Stop")
time.sleep(1)
