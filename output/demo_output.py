from time import sleep
from logicapcontroller import LogiCapController


# Small demo of LogiCapController: Creates a short recording with different scenes
def logi_demo():
    lc = LogiCapController()

    sleep(3)
    lc.start_stop()
    sleep(4)
    lc.switch_scene(1)
    sleep(1)
    lc.switch_scene(2)
    sleep(1)
    lc.switch_scene(3)
    sleep(1)
    lc.switch_scene(4)
    sleep(1)
    lc.start_stop()
