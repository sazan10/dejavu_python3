import os
import shutil
from botocore.client import Config
import boto3
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer
from dejavu import Dejavu
import warnings
import json
warnings.filterwarnings("ignore")


# boto3 library to manipulate s3 bucket

# start and config session for s3
session = boto3.session.Session()
client = session.client('s3',
                        region_name='sgp1',
                        endpoint_url='https://sgp1.digitaloceanspaces.com',
                        aws_access_key_id='T73DNHQ2DPI4PB35JCDT',
                        aws_secret_access_key='eSsUdEHEqwaS7ph6VBnn8qnwtVhBf09hCXL0GdWzfzc')
# get the names of all the songs
songs_arr = client.list_objects(Bucket='songs-1')['contents']
# pop out the dir name
songs_arr.pop(0)
num_vcpu = '4'
dir_name = 'fopi_songs'

with open("dejavu.cnf") as f:
        config = json.load(f)

if __name__ == '__main__':

        # create a Dejavu instance
    djv = Dejavu(config)

    # Fingerprint all the mp3's in the directory we give it
   
    for num, song in enumerate(songs_arr, 1):
        print(num, song)
        os.mkdir(dir_name)
        client.download_file(Bucket='songs-1',
                            Key=song['Key'],
                            Filename=os.path.join(dir_name, song['Key']))
        if ((num) == len(songs_arr)) or (((num) % num_vcpu) == 0):
            djv.fingerprint_directory(dir_name, [".mp3"])
            shutil.rmtree(dir_name)
            print('\n\n************')
            print('finger printed ', num, ' songs')
            # load config from a JSON file (or anything outputting a python dictionary)
    
    # Recognize audio from a file
    # song = djv.recognize(
    #    FileRecognizer, "mp3/Sean-Fournier--Falling-For-You.mp3")
    #print("From file we recognized: {}\n".format(song))
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
