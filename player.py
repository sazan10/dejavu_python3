
# import urllib.request as urllib2
# import pyaudio
# pyaudio = pyaudio.PyAudio()
# srate=44100
# p = pyaudio.PyAudio()
# stream = p.open(format=p.get_format_from_width(1),
#                 channels = 1,
#                 rate = srate,
#                 output = True)
# url = "http://kantipur-stream.softnep.com:7248"
# u = urllib2.urlopen(url)

# data = u.read(8192)

# while data:
#     stream.write(data)
#     data = u.read(8192)

# stream.stop_stream()
# stream.close()

# # close PyAudio (5)
# p.terminate()


import pyaudio
import sys
import urllib.request as urllib2
import pymedia.audio.acodec as acodec
import pymedia.muxer as muxer
dm= muxer.Demuxer( 'mp3' )
CHUNK = 1024

srate=44100
# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=p.get_format_from_width(2),
                channels=2,
                rate=srate,
                output=True)

# read data
# data = wf.readframes(CHUNK)
url = "http://kantipur-stream.softnep.com:7248"
u = urllib2.urlopen(url)

data = u.read(8192)
# play stream (3)
while len(data) > 0:

    #Start Decode using pymedia
    dec= None
    s= " "
    sinal=[]
    while len( s ):
        s= data
        if len( s ):
            frames= dm.parse( s )
            for fr in frames:
                if dec== None:
                    # Open decoder
                    dec= acodec.Decoder( dm.streams[ 0 ] )
                r= dec.decode( fr[ 1 ] )
                if r and r.data:
                    din = r.data
            s=""
    #decode ended
    stream.write(din)
    data = u.read(8192)


# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()