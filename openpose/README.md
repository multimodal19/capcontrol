# openpose

A C++ implementation of a camera preview window with a parallel thread running
OpenPose and processing as many of the frames as it can.

## Build Requirements
- Visual Studio 2017 (Tested with version 15.9.10, but other versions should
  be fine too)
    - C++ Desktop development component
- [OpenPose C++ API](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
- The ZeroMQ library [libzmq](https://github.com/zeromq/libzmq) as well as its
  C++ bindings [cppzmq](https://github.com/zeromq/cppzmq).


## Installation
1. Build OpenPose. Please refer to the [installation guide](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation.md#openpose---installation).
2. Build the ZeroMQ library
   - Place the built ZeroMQ `*.lib` in the openpose directory at
     `3rdparty\zeromq\lib\*.lib`.
   - Place the ZeroMQ header files in the openpose directory at
     `3rdparty\zeromq\include\`.
   - Place the built ZeroMQ `*.dll` in the openpose output directory.
3. In the files `camera_pose.vcxproj` & `camera_pose.vcxproj.user` from the
  `OpenPose` subfolder, replace all occurrences of
  `D:\Documents\GitHub\openpose` with your own OpenPose installation path.
4. Open and build solution with Visual Studio.

## Usage
Either just run the application directly from Visual Studio or from the build
directory.

For the Publisher & Subscriber, host address and port can be changed via
command line arguments, default is: `camera_pose.exe localhost 4000 4001`.

The following interaction is possible:
| Key              | Action                       |
|------------------|------------------------------|
| <kbd>Esc</kbd>   | Quit the application         |
| <kbd>Space</kbd> | Toggle show processed frames |
| <kbd>f</kbd>     | Toggle FPS indicator         |
| <kbd>m</kbd>     | Toggle mirroring             |
| <kbd>w</kbd>     | Increase turn threshold      |
| <kbd>s</kbd>     | Decrease turn threshold      |
| <kbd>c</kbd>     | Switch between cameras       |
