import multiprocessing
import time
import urllib.request
import json
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
data2=['1','2','3','4','5','6','7']#,'11']#,'12','13','14','15','16','17','18','19','20','21','22','23','24','25','26']

config =None
with open("dejavu.cnf") as f:
    config = json.load(f)


def mp_worker(urldata):
    url=None
    number=None
    song=None
    name =None
    try:
        url, number=urldata
        name= 'recording' +number+'.mp3'
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
    try:
        djv = Dejavu(config)
        song = djv.recognize(FileRecognizer, name)
        # print("From Stream we recognized: {}\n".format(song))
        print(song)
        if type(song)=="NoneType":
            print("NONE")
        elif song is None:
            print("NONE")
        elif song['confidence']>100:
            db_cls = get_database(config.get("database_type", None))
            db = db_cls(**config.get("database", {}))
            db.setup()
            count = db.get_song_count_by_name(song["song_name"])
            db.update_song_count(song["song_name"],count['count']+1)
            print("From file we recognized: {} {}\n".format(song["song_name"], count))
        else:
            print("Identified with very low confidence")#,song['confidence'])
    except Exception as e:
        print(e)

t=time.time()
def proc():
    nProcessor=multiprocessing.cpu_count()
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
        if (now-current) >=20:
            proc()
            current=time.time()


