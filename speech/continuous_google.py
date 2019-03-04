import time
import speech_recognition as sr


# this is called from the background thread
def callback(recognizer, audio):
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use
        # `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print(recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition "
              "service; {}".format(e))


r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    print("Be quiet, we're calibrating")
    # we only need to calibrate once, before we start listening
    r.adjust_for_ambient_noise(source, 5)

# start listening in the background
print("Now listening in the background")
stop_listening = r.listen_in_background(m, callback)

# do some unrelated computations for 60 seconds
# we're still listening even though the main thread is doing other things
for _ in range(600): time.sleep(0.1)

# calling this function requests that the background listener stop listening
stop_listening(wait_for_stop=False)
