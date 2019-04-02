from pynput.keyboard import Key, Controller
import sys
from communication import Subscriber


class LogiCapController:
    """Can produce all shortcuts supported by Logitech Capture."""

    def __init__(self):
        self.kb = Controller()

    def start_stop(self):
        """Start / stop recording."""
        self.send_alt_key_combo('r')

    def mic_mute_unmute(self):
        """Mute / unmute microphone."""
        self.send_alt_key_combo('n')

    def sys_mute_unmute(self):
        """Mute / unmute system sounds."""
        self.send_alt_key_combo('m')

    def screenshot(self):
        """Take a screenshot."""
        self.send_alt_key_combo('s')

    def switch_scene(self, n):
        """Go to scene n (1-4)."""
        self.send_alt_key_combo(n)

    def next_scene(self):
        """Go to next scene."""
        self.send_alt_key_combo('c')

    def send_alt_key_combo(self, key):
        print(f"LogiCapture: alt-{key}")
        self.kb.press(Key.alt)
        self.kb.press(str(key))
        self.kb.release(str(key))
        self.kb.release(Key.alt)


def handler(msg, controller):
    """The message handler receiving commands from the coordinator.

    :param str msg: the message
    :param LogiCapController controller: the LogiCapController instance to use
    """
    if msg == "start_stop":
        controller.start_stop()
    elif msg == "scene_1":
        controller.switch_scene(1)
    elif msg == "scene_2":
        controller.switch_scene(2)
    else:
        print("Unknown message: {}".format(msg))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Expected arguments <address> <port>")
        sys.exit(1)
    # Instantiate new LogiCapController
    lc = LogiCapController()
    # Subscribe to and handle logicap messages
    sub = Subscriber(
        sys.argv[1], sys.argv[2], "logicap", handler, {'controller': lc})
    sub.start()
    # Don't terminate immediately
    print("Press enter to quit.")
    input()
