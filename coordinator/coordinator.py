import sys
from overlaywrapper import OverlayWrapper
from communication import MessageBroker, Publisher, Subscriber


def speech_handler(msg):
    if msg == "start_stop":
        print("Starting/stopping recording")
        logi.send("start_stop")
    elif msg == "scene_1":
        print("Changing to scene 1")
        logi.send("scene_1")
    elif msg == "scene_2":
        print("Changing to scene 2")
        logi.send("scene_2")
    elif msg == "rage":
        print("Showing the rage overlay")
        overlay.rage_overlay()
    elif msg == "cloud":
        print("Showing the cloud overlay")
        overlay.cloud_overlay()
    else:
        print(f"Unknown speech command: {msg}")


def openpose_handler(msg):
    if msg in ["left", "right", "straight"]:
        print(f"Looking {msg}")
        overlay.send(f"overlays/filter_{msg}.png")
    else:
        print(f"Unknown openpose command: {msg}")


# Abort on missing arguments
if len(sys.argv) < 3:
    print("Expected arguments <port_in> <port_out>")
    sys.exit(1)
port_in = sys.argv[1]
port_out = sys.argv[2]

# Start message broker
broker = MessageBroker(port_in, port_out)
broker.start()

# Prepare publishers and subscribers
overlay = OverlayWrapper(Publisher("127.0.0.1", port_in, "overlay"))
logi = Publisher("127.0.0.1", port_in, "logicap")
speech = Subscriber("127.0.0.1", port_out, "speech", speech_handler)
openpose = Subscriber("127.0.0.1", port_out, "openpose", openpose_handler)
# Start subscribers
speech.start()
openpose.start()

# Don't terminate immediately
print("Press enter to quit.")
input()
