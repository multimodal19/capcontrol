import time


class FPSCounter:
    # average_interval=1 => displays the new frame rate every 1 second
    def __init__(self, average_interval=1):
        self.start_time = time.time()
        self.average_interval = average_interval
        self.counter = 0
        self.fps = 0

    def tick(self):
        self.counter += 1
        if (time.time() - self.start_time) > self.average_interval:
            self.fps = self.counter / (time.time() - self.start_time)
            self.counter = 0
            self.start_time = time.time()

    def get_fps(self):
        return self.fps
