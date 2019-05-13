import struct
import sys
import pyaudio
import ibmstt
from porcupine import Porcupine
from communication import Publisher


# Number of seconds until recognition is aborted if nothing is recognized
TIMEOUT = 10


def scene(t):
    return any(w in t for w in ["camera", "camaro", "see", "scene"])


def listen_callback(t):
    # Do reeeaally simple "recognition"
    if "record" in t:
        speech.send("start_stop")
    elif scene(t) and ("one" in t):
        speech.send("scene_1")
    elif scene(t) and ("two" in t or "to" in t):
        speech.send("scene_2")
    elif scene(t) and ("three" in t):
        speech.send("scene_3")
    elif scene(t) and ("four" in t or "for" in t):
        speech.send("scene_4")
    elif "rage" in t or "rache" in t or "suck" in t:
        speech.send("rage")
    elif "cloud" in t:
        speech.send("cloud")
    elif "clear" in t:
        speech.send("clear_overlay")
    elif ("subscribe" in t or "follow" in t) and "youtube" in t:
        speech.send("social_youtube")
    elif ("subscribe" in t or "follow" in t) and "twitter" in t:
        speech.send("social_twitter")
    else:
        # Return False since we didn't find anything
        return False
    # Return True because we found something
    return True


class Recognizer():

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
                    ibmstt.recognize(listen_callback, TIMEOUT)

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
