import sys
from communication import Publisher

# Abort on missing arguments
if len(sys.argv) < 3:
    print("Expected arguments <address> <port>")
    sys.exit(1)
# Initialize Publisher
speech = Publisher(sys.argv[1], sys.argv[2], "speech")

from time import sleep

sleep(3)
print("cloud")
speech.send("cloud")
sleep(2)
print("rage")
speech.send("rage")
sleep(1)
