import cv2
from fps import FPSCounter
from openpose import OpenPose
from webcamstream import WebcamVideoStream


font = cv2.FONT_HERSHEY_SIMPLEX
scale_factor = 8


class CamWindow:
    def __init__(self):
        cv2.namedWindow("preview", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(
            "preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        # Get window dimensions
        x, y, width, height = cv2.getWindowImageRect("preview")

        ws = WebcamVideoStream(int(width/2), int(height/2), mirror=True)
        op = OpenPose(self, (int(width/scale_factor), int(height/scale_factor)))
        self.o_fps = o_fps = FPSCounter()
        ws.start()
        self.frame = frame = ws.read()
        self.oframe = frame

        fps = FPSCounter()
        op.start()

        show_full = True

        while True:

            fps.tick()
            window_fps = round(fps.fps, 1)
            openpose_fps = round(o_fps.fps, 1)

            frame = self.frame if show_full else self.oframe
            if show_full:
                cv2.putText(frame, f"{window_fps} - {openpose_fps}", (0, 100), font, 4, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow("preview", frame)

            self.frame = ws.read()
            key = cv2.waitKey(10)
            if key == 27:  # exit on ESC
                break
            if key == 32:  # space toggle
                show_full = not show_full

        ws.stop()
        cv2.destroyWindow("preview")
        op.stop()

    def get_frame(self):
        return self.frame

    def set_frame(self, frame):
        self.oframe = frame


CamWindow()
