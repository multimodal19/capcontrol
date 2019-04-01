import os
import cv2
import sys
from sys import platform
from threading import Thread


build_path = "D:/Documents/GitHub/openpose/build"


# Import Openpose (Windows/Ubuntu/OSX)
try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(build_path + '/python/openpose/Release')
        os.environ['PATH'] += ';' + build_path + '/x64/Release;' + build_path + '/bin;'
        import pyopenpose as op
    else:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(build_path + '/python')
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the
        # OpenPose/python module from there. This will install OpenPose and the python library at your desired
        # installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found.')
    print('Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e


class OpenPose:
    def __init__(self, camwindow, size):
        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        params = dict()
        params["model_folder"] = build_path + "/../models/"
        params["face"] = True
        params["hand"] = True

        # Starting OpenPose
        self.opWrapper = op.WrapperPython()
        self.opWrapper.configure(params)
        self.opWrapper.start()

        self.cw = camwindow
        self.size = size
        self.stopped = False

    def process_img(self, img):
        img = cv2.resize(img, self.size)

        # Create new datum
        datum = op.Datum()
        datum.cvInputData = img

        # Process and display image
        self.opWrapper.emplaceAndPop([datum])
        # do something datum.faceKeypoints

        return datum.cvOutputData

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            self.cw.set_frame(self.process_img(self.cw.get_frame()))
            self.cw.o_fps.tick()

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
