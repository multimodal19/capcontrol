import sys
from overlaywrapper import OverlayWrapper
from communication import MessageBroker, Publisher, Subscriber


# Global state
shared_state = {'hands': {}}


def speech_handler(msg):
    if msg == "start_stop":
        print("Starting/stopping recording")
        logi.send("start_stop")
    elif "scene_" in msg:
        scene = msg.replace("scene_", "")
        print(f"Changing to scene {scene}")
        logi.send(f"scene_{scene}")
    elif msg == "rage":
        print("Showing the rage overlay")
        overlay.rage_overlay()
    elif msg == "cloud":
        print("Showing the cloud overlay")
        overlay.cloud_overlay()
    elif msg == "next":
        # Skip if no hand data was collected yet
        if "right" not in shared_state["hands"]: return
        print("Showing the popup")
        # Show small image at index finger position
        w = 200
        x = shared_state["hands"]["right"][0] - int(w / 2)
        y = shared_state["hands"]["right"][1] - int(w / 2)
        # Replace with whatever image you like
        overlay.send("D:/Downloads/mindblown.gif", x=x, y=y, width=w, animate=True)
    else:
        print(f"Unknown speech command: {msg}")


def openpose_handler(msg):
    kind, *args = msg.split(" ")

    if kind == "face":
        direction = args[0]
        print(f"Looking {direction}")
        overlay.send(f"overlays/filter_{direction}.png")
    elif kind == "hand":
        # Store hand data in global state
        shared_state["hands"][args[0]] = list(map(int, args[1:]))
        #print(f"hand data: {', '.join(args)}")
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
