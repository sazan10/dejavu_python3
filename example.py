import os
import shutil
from botocore.client import Config
import boto3
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer
from dejavu import Dejavu
import warnings
import json
import time
import csv
import pandas as pd
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
songs_arr = client.list_objects(Bucket='songs-1')['Contents']
# pop out the dir name
songs_arr.pop(0)
num_vcpu = 4

# delete previous os dir
dir_name = 'fopi_songs'
if os.path.isdir(dir_name):
    shutil.rmtree(dir_name)

# read from log
last_run_at = 0
if os.path.isfile('log.csv'):
    df = pd.read_csv('log.csv', header=None)
    last_run_at = int(df.tail(1)[0]) - 1

# update song_arr
start_from = last_run_at*num_vcpu + num_vcpu-1
song_arr = song_arr[start_from:]

# load config for dejavu db
with open("dejavu.cnf") as f:
    config = json.load(f)


if __name__ == '__main__':

        # create a Dejavu instance
    djv = Dejavu(config)
    os.mkdir(dir_name)
    
    # Fingerprint all the mp3's in the directory we give it
    songs_tag=[]
    starting_time=time.time()
    print ("start time: ",starting_time)
    for num, song in enumerate(songs_arr, 1):    
        client.download_file(Bucket='songs-1',
                            Key=song['Key'],
                            Filename=song['Key'])
        songs_tag.append(song['Key'])
        if ((num) == len(songs_arr)) or (((num) % num_vcpu) == 0):
            start=time.time()
            djv.fingerprint_directory(dir_name, [".mp3"])
            print("batch:",songs_tag,time.time()-start)
            with open('log.csv', 'a') as writeFile:
               writer= csv.writer(writeFile)
               writer.writerows([[num/4,songs_tag,time.time()-start]])
            songs_tag=[]
            shutil.rmtree(dir_name)
            os.mkdir(dir_name)
    final_end_time=time.time()
    print("end time: ", final_end_time)
    with open('total_time.csv', 'a') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows([["complete time",final_end_time-starting_time]])

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
