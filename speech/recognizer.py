import struct
import sys
import pyaudio
import speech_recognition as sr
from threading import Thread
from porcupine import Porcupine
from communication import Publisher


def listen_google():
    with sr.Microphone() as source:
        audio = r.listen(source)
    # recognize speech using Google Speech Recognition
    try:
        text = r.recognize_google(audio).lower()
        print("Recognized: {}".format(text))
        # Do reeeaally simple "recognition"
        if "record" in text:
            speech.send("start_stop")
        elif "camera" in text or "scene" in text:
            if "1" in text or "one" in text:
                speech.send("scene_1")
            elif "2" in text or "two" in text:
                speech.send("scene_2")
            elif "3" in text or "three" in text:
                speech.send("scene_3")
            elif "4" in text or "four" in text:
                speech.send("scene_4")
        elif "rage" in text or "radar" in text or "suck" in text:
            speech.send("rage")
        elif "cloud" in text:
            speech.send("cloud")
        elif "clear" in text:
            speech.send("clear_overlay")

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {}"
            .format(e))


class Recognizer(Thread):

    def __init__(
            self,
            library_path,
            model_file_path,
            keyword_file_paths,
            sensitivities):
        super(Recognizer, self).__init__()
        self._library_path = library_path
        self._model_file_path = model_file_path
        self._keyword_file_paths = keyword_file_paths
        self._sensitivities = sensitivities


    def run(self):
        porcupine = None
        pa = None
        audio_stream = None
        try:
            porcupine = Porcupine(
                library_path=self._library_path,
                model_file_path=self._model_file_path,
                keyword_file_paths=self._keyword_file_paths,
                sensitivities=self._sensitivities)

            pa = pyaudio.PyAudio()
            audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length)

            while True:
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                result = porcupine.process(pcm)
                if result:
                    print("Detected hotword, listening...")
                    listen_google()

        except KeyboardInterrupt:
            print('stopping ...')
        finally:
            if porcupine is not None:
                porcupine.delete()
            if audio_stream is not None:
                audio_stream.close()
            if pa is not None:
                pa.terminate()


if __name__ == "__main__":
    # Abort on missing arguments
    if len(sys.argv) < 3:
        print("Expected arguments <address> <port>")
        sys.exit(1)
    # Initialize Publisher
    speech = Publisher(sys.argv[1], sys.argv[2], "speech")

    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        print("Be quiet, we're calibrating")
        # we only need to calibrate once, before we start listening
        r.adjust_for_ambient_noise(source, 5)

    # start listening in the background
    print("Now listening in the background for hotword 'Christina'")

    keyword_file_paths = ["porcupine/keywords/christina_windows.ppn"]
    library_path = "porcupine/libpv_porcupine.dll"
    model_file_path = "porcupine/porcupine_params.pv"
    sensitivities = [0.5]

    Recognizer(
        library_path,
        model_file_path,
        keyword_file_paths,
        sensitivities).run()
