import warnings
import json
warnings.filterwarnings("ignore")
import firFilter as fi
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer
from dejavu.database import get_database, Database
import os
from scipy.io import wavfile


# load config from a JSON file (or anything outputting a python dictionary)
with open("dejavu.cnf") as f:
    config = json.load(f)

if __name__ == '__main__':

	# create a Dejavu instance
    djv = Dejavu(config)

	# Fingerprint all the mp3's in the directory we give it
	# djv.fingerprint_directory("mp3", [".mp3"])
    fs,p = wavfile.read("mp3/coke.wav")
    data = p[:,1]
    new = fi.firFilter(data,fs)
    wavfile.write("new.wav",fs,new)