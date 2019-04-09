# overlay

## Build Requirements
- Visual Studio 2017 (Tested with version 15.9.9, but other versions should be
  fine too)
    - .NET Desktop development component

## Installation
Open and build solution with Visual Studio.

## Usage
Either just run the application directly from Visual Studio or from the bin
directory.

Commands are read from `stdin` and via ZeroMQ subscriber under topic `overlay`.
For the subscriber, host address and port can be changed via command line
arguments, default is: `CameraOverlay.exe localhost 4001`.

```
command structure: [OPTIONS] IMG_SOURCE

-x               Horizontal offset (Default: 0).
-y               Vertical offset (Default: 0).
-w               Width (Default: screen size).
-h               Width (Default: screen size).
-i, --fadein     Fade in duration in ms (Default: 200).
-o, --fadeout    Fade out duration of previous image in ms (Default: 200).
--center         Align image centered on the screen (Default: false).
--stretch        Stretch image to fit (Default: only scale).
--animate        Animate gif (Default: false).
--help           Display this help screen.
--version        Display version information.
IMG_SOURCE       Required. file path or URL pointing to image.
```

Use <kbd>Esc</kbd> to quit and <kbd>Space</kbd> to switch between the two
default overlays.
