import sys
from communication import Publisher
from pocketsphinx import LiveSpeech


# Abort on missing arguments
if len(sys.argv) < 3:
    print("Expected arguments <address> <port>")
    sys.exit(1)
# Initialize Publisher
pub = Publisher(sys.argv[1], sys.argv[2], "speech")

speech = LiveSpeech(lm=False, keyphrase='next', kws_threshold=1e-35)
for phrase in speech:
    print(phrase.segments(detailed=True))
    pub.send("next")
