from time import sleep

from logicapcontroller import LogiCapController
from overlaycontroller import OverlayController


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


# Small demo of OverlayController: switches between default overlays
def overlay_demo():
    oc = OverlayController()

    sleep(3)
    oc.cloud_overlay()
    sleep(1)
    oc.rage_overlay()
    sleep(1)
    oc.cloud_overlay()
    sleep(1)
    oc.rage_overlay()
    sleep(1)

