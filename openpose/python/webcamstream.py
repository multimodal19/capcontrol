from threading import Thread
import cv2


class WebcamVideoStream:
    def __init__(self, width, height, src=0, mirror=False):

        # Set up video capture using the window dimensions to get nice scaling
        self.stream = cv2.VideoCapture(cv2.CAP_DSHOW + src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        # Check video capture by getting first frame
        if self.stream.isOpened():
            self.grabbed, self.frame = self.stream.read()
        else:
            raise Exception("Cannot access camera")

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False
        self.mirror = mirror

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                self.stream.release()
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return cv2.flip(self.frame, 1) if self.mirror else self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
