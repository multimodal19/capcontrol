import sys
import speech_recognition as sr
from communication import Publisher


# this is called from the background thread
def callback(recognizer, audio):
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use
        # `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        text = recognizer.recognize_google(audio).lower()
        print("Recognized: {}".format(text))
        # Do reeeaally simple "recognition"
        if "record" in text:
            speech.send("start_stop")
        elif "camera" in text or "scene" in text:
            if "1" in text or "one" in text:
                speech.send("scene_1")
            elif "2" in text or "two" in text:
                speech.send("scene_2")
        elif "rage" in text:
            speech.send("rage")
        elif "cloud" in text:
            speech.send("cloud")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition "
              "service; {}".format(e))


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
print("Now listening in the background")
stop_listening = r.listen_in_background(m, callback)

# Don't terminate immediately
print("Press enter to quit.")
input()

# calling this function requests that the background listener stop listening
stop_listening(wait_for_stop=False)
