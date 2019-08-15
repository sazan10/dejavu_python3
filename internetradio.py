import requests
import time
import urllib.request

stream_url = 'http://kantipur-stream.softnep.com:7248'

# r = requests.get(stream_url, stream=True)
conn = urllib.request.urlopen(stream_url)
t = time.time()
i = 0
with open('stream.mp3', 'wb') as f:
    try:
        while True:
            f.write(conn.read(100000))
            # ti = time.time() - t
            # if(ti > 1):
            break
        
        
    except KeyboardInterrupt:
        pass

with open('stream1.mp3', 'wb') as fi:
    try:
        while True:
            fi.write(conn.read(500000))
            # ti = time.time() - t
            # if(ti > 1):
            break
        
        
    except KeyboardInterrupt:
        pass

# print(i)
# print(ti)