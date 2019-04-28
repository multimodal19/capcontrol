# Copyright 2016 IBM
# Modifications copyright (c) 2019 Martin Disch
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import base64
import configparser
import json
import threading
import pyaudio
import websocket
from websocket._abnf import ABNF

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

RUNNING = None
CALLBACK = None
# The maximum number of seconds after which recognition is stopped
RECORD_SECONDS = 10

REGION_MAP = {
    'us-south': "stream.watsonplatform.net",
    'us-east': "gateway-wdc.watsonplatform.net",
    'eu-de': "stream-fra.watsonplatform.net",
    'eu-gb': "gateway-lon.watsonplatform.net",
    'au-syd': "gateway-syd.watsonplatform.net",
    'jp-tok': "gateway-tok.watsonplatform.net"
}


def read_audio(ws):
    """Read audio and send it to the websocket port.

    This uses pyaudio to read from a device in chunks and send these
    over the websocket wire.

    """
    # Open stream
    global RATE
    p = pyaudio.PyAudio()
    RATE = int(p.get_default_input_device_info()['defaultSampleRate'])
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    # Recognize until timeout or recognition
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        if not RUNNING:
            break
        data = stream.read(CHUNK)
        ws.send(data, ABNF.OPCODE_BINARY)

    print("Stopped listening")
    # Disconnect the audio stream
    stream.stop_stream()
    stream.close()
    # Close the WebSocket
    ws.close()
    # Kill the audio device
    p.terminate()


def on_message(ws, msg):
    """Print the recognized message and pass it to the callback."""
    data = json.loads(msg)
    if "results" in data:
        # This prints out the current fragment that we are working on
        text = data['results'][0]['alternatives'][0]['transcript'].lower()
        print(text)
        # Pass it to the callback
        if CALLBACK(text):
            # If it recognized something, stop listening
            global RUNNING
            RUNNING = False


def on_error(ws, error):
    """Print any errors."""
    print(f"WebSocket error: {error}")


def on_open(ws):
    """Triggered as soon a we have an active connection."""
    data = {
        "action": "start",
        # this means we get to send it straight raw sampling
        "content-type": "audio/l16;rate=%d" % RATE,
        "interim_results": True,
        "profanity_filter": False
    }

    # Send the initial control message which sets expectations for the
    # binary stream that follows:
    ws.send(json.dumps(data).encode('utf8'))
    # Spin off a dedicated thread where we are going to read and
    # stream out audio.
    threading.Thread(target=read_audio, args=[ws]).start()


def get_url():
    """Return the URL for the location from the config file.

    Returns
    -------
    str
        The URL with all parameters.

    """
    config = configparser.RawConfigParser()
    config.read("speech.cfg")
    region = config.get('auth', 'region')
    host = REGION_MAP[region]
    return (
        f"wss://{host}/speech-to-text/api/v1/recognize"
        "?model=en-US_BroadbandModel&x-watson-learning-opt-out=true"
    )


def get_auth():
    """Return the credentials from the config file.

    Returns
    -------
    tuple of str
        With two elements, key and value.

    """
    config = configparser.RawConfigParser()
    config.read("speech.cfg")
    apikey = config.get('auth', 'apikey')
    return ("apikey", apikey)


def recognize(callback, timeout):
    """Recognize speech, passing it to the callback to act upon.

    Recognition will run until the callback returns True on a result, or the
    timeout has been reached.

    Parameters
    ----------
    callback : fun
        Function taking a string (the recognized text) as an argument.
        Returns True when it was able to recognize something and this run of
        recognition should stop, or False if that wasn't the case and
        recognition should continue.
    timeout : int
        Number of seconds after which recognition should be stopped if nothing
        was recognized.

    """
    # Reset globals
    global CALLBACK, RUNNING, RECORD_SECONDS
    CALLBACK = callback
    RECORD_SECONDS = timeout
    RUNNING = True
    # Connect to websocket interfaces
    headers = {}
    userpass = ":".join(get_auth())
    headers["Authorization"] = "Basic " + base64.b64encode(
        userpass.encode()).decode()
    url = get_url()
    ws = websocket.WebSocketApp(url,
                                header=headers,
                                on_message=on_message,
                                on_error=on_error,
                                on_open=on_open)
    # This hands control to the WebSocketApp. It's a blocking call, so it won't
    # return until ws.close() gets called
    ws.run_forever()
