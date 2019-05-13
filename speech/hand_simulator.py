import sys
import random
import time
from communication import Publisher

# Abort on missing arguments
if len(sys.argv) < 3:
    print("Expected arguments <address> <port>")
    sys.exit(1)
# Initialize Publisher
pub = Publisher(sys.argv[1], sys.argv[2], "openpose")

while True:
    pub.send(
        f"hand right {random.randint(200, 1300)} {random.randint(200, 800)}")
    time.sleep(1)
