import multiprocessing
import time
import urllib.request
import json
import datetime
import pytz
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer
from dejavu.database import get_database, Database

'''data1 = (["http://kantipur-stream.softnep.com:7248",'1'],
        ["http://ujyaalo-stream.softnep.com:7710",'2'],
        ["http://kalika-stream.softnep.com:7740",'3'],
        ["http://streaming.softnep.net:8085",'4'],
        ["http://streaming.softnep.net:8039",'5'],
        ["http://streaming.softnep.net:8067",'6'],
        ["http://streaming.softnep.net:9001",'7'],
        ["http://streaming.softnep.net:8029",'8'],
        ["http://streaming.softnep.net:800",'9'],
        ["http://streaming.softnep.net:8037",'10'],
        ["http://streaming.softnep.net:8091",'11'],
        ["http://streaming.softnep.net:8003",'12'],
        ["http://108.166.161.210:9022",'13'],
        ["http://192.99.8.192:3552",'14'],
        ["http://202.166.217.123:89",'15'],
        ["http://streaming.softnep.net:8049",'16'],
        ["http://streaming.softnep.net:8014",'17'],
        ["http://streaming.softnep.net:9001",'18'],
        ["http://streaming.softnep.net:8081",'19'],
        ["http://streaming.softnep.net:8089",'20'],
        ["http://streaming.softnep.net:8101",'21'],
        ["http://streaming.softnep.net:8099",'22'],
        ["http://streaming.softnep.net:8093",'23'],
        ["http://streaming.softnep.net:8031",'24'],
        ["http://streaming.softnep.net:8057",'25'],
        ["http://streaming.softnep.net:8035",'26'],
        ["http://streaming.softnep.net:8097",'27'],
        ["http://streaming.softnep.net:8077",'28'],
        ["http://streaming.softnep.net:8047",'29'],
        ["http://streaming.softnep.net:8061",'30']
)'''
data1 = ["http://kantipur-stream.softnep.com:7248"
        # ,"http://kalika-stream.softnep.com:7740"#
        # ,"http://streaming.softnep.net:8085"
        # ,"http://streaming.softnep.net:8037"#
        #,"http://streaming.softnep.net:8091"
        ,"http://streaming.softnep.net:8003"
        # ,"http://streaming.softnep.net:8049"#
        ,"http://streaming.softnep.net:8093"
        #,"http://192.168.10.82:8000"
        ,"http://streaming.softnep.net:8031"
        ,"http://streaming.softnep.net:8057"]
        #,"http://streaming.softnep.net:8061"]
data2=['kantipur','butwal','kalaiya','softnep','makwanpur']#,'11']#,'12','13','14','15','16','17','18','19','20','21','22','23','24','25','26']

config =None
db = None
with open("dejavu.cnf") as f:
    config = json.load(f)
    db_cls = get_database(config.get("database_type", None))
    db = db_cls(**config.get("database", {}))
    db.setup()


def mp_worker(urldata):
    url=None
    station_name=None
    song=None
    name =None
    try:
        url, station_name=urldata
        name= station_name+'.mp3'
    except ValueError:
        pass
    try:
        u=urllib.request.urlopen(url)
        data=u.read(150000)
        with open(name,'wb') as file:
            file.write(data)
            time.sleep(1)
    except Exception as e:
        print (e)
    #try:
    djv = Dejavu(config)
    song = djv.recognize(FileRecognizer, name)
    # print("From Stream we recognized: {}\n".format(song))
    if song is None:
        print("NONE")
    elif song['confidence'] >= 40:
        file_data=None
        try:        
            with open(station_name+".txt",'r') as file:
                file_data=file.read()
        except Exception as e: 
            with open(station_name+".txt",'w') as file:
                pass
        if file_data==song["song_name"]:
            print('ad already recorded')
            with open('log_date.txt','a') as writeFile:
                writeFile.write("\n Duplicate recognition with confidence %d %s " %(song["confidence"],song["song_name"]))    
        else:
            with open(station_name+".txt",'w') as file:
                file.write(song["song_name"])  
            db_cls = get_database(config.get("database_type", None))
            db = db_cls(**config.get("database", {}))
            db.setup()
            # count = db.get_song_count_by_name(song["song_name"])
            # db.update_song_count(song["song_name"],count['count']+1)
            d_local = datetime.datetime.now(pytz.timezone("Asia/Kathmandu"))  
            db.insert_radio_song(station_name, song["song_name"], 'Begari Guys', int(song['confidence']), d_local)
            print("From file we recognized: {}\n".format(song["song_name"]))
            with open('log_date.txt','a') as writeFile:
                writeFile.write("\n Identified with high confidence %d %s" %(song['confidence'],song['song_name']))
    else:
        with open('log_date.txt','a') as writeFile:
            writeFile.write("\n Identified with very less confidence %d %s" %(song['confidence'],song["song_name"]))
        print("From file we recognized: {} {} \n".format(song["song_name"],song['confidence']))
        #except Exception as e:
        #    print(e)

t=time.time()
def proc():
    nProcessor=multiprocessing.cpu_count()
    # radio = db.get_all_radio()
    p = multiprocessing.Pool(nProcessor)
    data=zip(data1,data2)
    iterator=p.imap_unordered(mp_worker, data)
    while True:
        try:
            iterator.next()
        except StopIteration:
            break
    # iterator=p.map(mp_worker, data1)
    p.close()
    t2=time.time()-t
    print("time taken",t2)

if __name__ == '__main__':
    current=time.time()
    proc()
    while True: 
        now =time.time()
        if (now-current) >=15:
            proc()
            current=time.time()


