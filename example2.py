import warnings
import json
warnings.filterwarnings("ignore")

from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer
from dejavu.database import get_database, Database

# load config from a JSON file (or anything outputting a python dictionary)
with open("dejavu.cnf") as f:
    config = json.load(f)

if __name__ == '__main__':

	# create a Dejavu instance
	djv = Dejavu(config)

	# Fingerprint all the mp3's in the directory we give it
	djv.fingerprint_directory("22050mp3", [".mp3"])

	# Recognize audio from a file
	#song = djv.recognize(FileRecognizer, "ads/hyundai offer.mp3")
	#if song['confidence']>100:
#		db_cls = get_database(config.get("database_type", None))
#		db = db_cls(**config.get("database", {}))
#		db.setup()
#		count = db.get_song_count_by_name(song["song_name"])
#		db.update_song_count(song["song_name"],count['count']+1)
#		
#		print("From file we recognized: {}, count: {}\n".format(song["song_name"], count['count']+1))
#	else:
#		print("None")
#	print("From file we recognized: {}\n".format(song))

	#song = djv.recognize(FileRecognizer, "mp3/01 Aakhako Bato.mp3")
	#print("From file we recognized: {}\n".format(song))

	# Or recognize audio from your microphone for `secs` seconds
#	secs = 5
#	song = djv.recognize(MicrophoneRecognizer, seconds=secs)
#	if song is None:
#		print("Nothing recognized -- did you play the song out loud so your mic could hear it? :)")
#	else:
#		print("From mic with %d seconds we recognized: %s\n" % (secs, song))

	# Or use a recognizer without the shortcut, in anyway you would like
#	recognizer = FileRecognizer(djv)
#	song = recognizer.recognize_file("mp3/Josh-Woodward--I-Want-To-Destroy-Something-Beautiful.mp3")

#	print("No shortcut, we recognized: {}\n".format(song))

#	print("No shortcut, we recognized: {}\n".format(song))
