# speech

## Installation
This is based on a default installation of Python 3.7 (32-bit) on Windows, with
the Python distribution added to the PATH variable.
The installation on Windows is pretty tedious, since PyAudio with PortAudio and
PocketSphinx require binaries that are not available on PyPI for Python 3.7 and
need to be built locally or downloaded from elsewhere.

1. Make sure all necessary tools are up to date. From administrator PowerShell
   run `pip install --upgrade pip setuptools wheel`.
2. Allow scripts for virtualenv activation. From administrator PowerShell run
   `Set-ExecutionPolicy -ExecutionPolicy Unrestricted`.
3. Create and activate a virtualenv.
   ```
   virtualenv env
   .\env\Scripts\activate
   ```
4. Installation of PyAudio with PortAudio.
    1. `git clone https://github.com/intxcc/pyaudio_portaudio.git`
    2. Open the portaudio project located in
       `pyaudio\portaudio-v19\build\msvc\portaudio.sln` with Visual Studio.
    3. Open the project properties and make sure that the configuration type
       is set to static library.
    4. Select the build type _Release_ and _Win32_. Then build the project.
       Might need to do _Project -> Retarget Solution_ on build failure
       (Windows SDK). Make sure configuration type is still static library.
    5. ```
       cd <Location of the repository>\pyaudio_portaudio\pyaudio
       python setup.py install --static-link
       ```
5. Download appropriate wheel file (32-bit, Python 3.7) from
   https://www.lfd.uci.edu/~gohlke/pythonlibs/#pocketsphinx and install with
   `pip install .\pocketsphinx-0.1.15-cp37-cp37m-win32.whl`.
6. `pip install SpeechRecognition`

## Usage
With the activated virtualenv, run any of the Python files like
`python demo_google.py`.
