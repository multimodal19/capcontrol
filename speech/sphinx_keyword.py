from pocketsphinx import LiveSpeech


speech = LiveSpeech(lm=False, keyphrase='record', kws_threshold=1e-35)
for phrase in speech:
    print(phrase.segments(detailed=True))
