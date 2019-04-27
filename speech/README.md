# speech

## Installation
1. Installation of PyAudio with PortAudio.
    1. `git clone https://github.com/intxcc/pyaudio_portaudio.git`
    2. Open the portaudio project located in
       `pyaudio\portaudio-v19\build\msvc\portaudio.sln` with Visual Studio.
    3. Open the project properties and make sure that the configuration type
       is set to static library.
    4. Select the build type _Release_ and _x64_. Then build the solution.
       Might need to do _Project -> Retarget Solution_ on build failure
       (Windows SDK). Make sure configuration type is still static library.
    5. ```
       cd <Location of the repository>\pyaudio_portaudio\pyaudio
       python setup.py install --static-link
       ```
3. Install other dependencies with `pip install -r requirements.txt`.
4. Since this uses the IBM Watson speech-to-text (STT) service, you need
   to create a free trial plan, copy `speech.cfg.EXAMPLE` to `speech.cfg` and
   enter your API key there.

## Usage

To run the recognizer connecting to the MessageBroker, use
`python recognizer.py localhost 4000`.

For the Porcupine demo, run
`python .\porcupine\porcupine_demo.py --keyword_file_paths
.\porcupine\keywords\christina_windows.ppn`.

For the IBM Watson STT demo, run
`python .\demo_ibm.py -t 20`.
