from mongoengine import connect
from dejavu.database_scheme import Fingerprints, Songs
import json
# from itertools import izip_longest
from itertools import zip_longest # renamed to zip_longest in python 3

class MongoDatabase(object):

    def __init__(self):
        self.database_host = 'localhost'
        self.database_name = 'dejavu'

    def setup(self):
        connect(host='mongodb://%s/%s'%(self.database_host,self.database_name))

    #Done
    def empty(self):
        """
        Drops collection created by dejavu

        .. warning:
            This will result in a loss of data
        """
        print("inside empty")
        Fingerprints.drop_collection()
        Songs.drop_collection()

    #Done
    def delete_unfingerprinted_songs(self):
        """
        Removes all songs that have no fingerprints associated with them.
        """
        print("inside delete unfinderprinted songs")
        Songs.objects(fingerprinted=0).delete()

    #Done
    def get_num_songs(self):
        """
        Returns number of songs the database has fingerprinted.
        """
        print("inside get num songs")
        songs_number = Songs.objects(fingerprinted=1).count()
        print("number of fingerprinted songs : %s"%(songs_number))
        return songs_number
    
    #Done
    def get_num_fingerprints(self):
        """
        Returns number of fingerprints the database has fingerprinted.
        """
        print("inside get num fingerprints")
        fingerprint_number = Fingerprints.objects().count()
        return fingerprint_number

    #Done
    def set_song_fingerprinted(self, sid):
        """
        Set the fingerprinted flag to TRUE (1) once a song has been completely
        fingerprinted in the database.
        """
        print("inside set song fingerpritned")
        Songs.objects(id=sid).update_one(fingerprinted=1)
    
    #Done
    def get_songs(self):
        """
        Return songs that have the fingerprinted flag set TRUE (1).
        """
        # all_songs = Songs.objects()
        print("inside get songs")
        all_songs = Songs.objects.exclude('id')
        for row in all_songs:
            yield row
        # return all_songs.to_json()

    #Done
    def get_song_by_id(self, sid):
        """
        Returns song by its ID.
        """
        print("inside get songs by id")
        one_song = Songs.objects(id=sid)
        one_song_str = one_song.to_json()
        dicts = json.loads(one_song_str)
        return dicts[0]

    #Done
    # INSERT FINGERPRINT
    def insert(self, hash, sid, offset):
        """
        Insert a (sha1, song_id, offset) row into database.
        """
        print("inside insert")
        insert_fingerprints = Fingerprints(hash=hash.upper(),song_id=sid,offset=offset)
        insert_fingerprints.save()

    #Done
    # INSERT SONGS
    def insert_song(self, songname, file_hash):
        """
        Inserts song in the database and returns the ID of the inserted record.
        """
        print("inside insert songs")
        insert_songs = Songs(song_name=songname, file_sha1=file_hash)
        insert_songs.save()
        return insert_songs.id

    #Not Done
    def query(self,hash):
        """
        Return all tuples associated with hash.
        If hash is None, returns all entries in the
        database (be careful with that one!).
        """
        print("inside query")
        fingerprints=None
        if hash is None:
            fingerprints = Fingerprints.objects().only('offset','song_id').exclude('id')
        else:
            fingerprints = Fingerprints.objects(hash=hash).only('song_id', 'offset').exclude('id')
        print("here")
        print(fingerprints.to_json())
        for sid, offset in fingerprints[0]:
            print(sid)
        return fingerprints

    #Done
    def get_iterable_kv_pairs(self):
        """
        Returns all tuples in database.
        """
        print("inside get iterable kv pairs")
        return self.query(None)

    #Done
    def insert_hashes(self, sid, hashes):
        """
        Insert series of hash => song_id, offset
        values into the database.
        """
        print("inside insert hashes")
        values = []
        for hashit, offset in hashes:
            values.append((hashit, sid, offset))

        for split_values in grouper(values, 1000):
            insert_fingerprints = []
            for hashit, sid, offset in split_values:
                insert_fingerprints.append(Fingerprints(hash=hashit.upper(),song_id=sid,offset=offset))
            Fingerprints.objects.insert(insert_fingerprints)

    #Done
    def return_matches(self, hashes):
        """
        Return the (song_id, offset_diff) tuples associated with
        a list of (sha1, sample_offset) values.
        """
        print("inside return matches")
        # Create a dictionary of hash => offset pairs for later lookups
        mapper = {}
        for hashit, offset in hashes:
            mapper[hashit.upper()] = offset

        # Get an iteratable of all the hashes we need
        values = mapper.keys()
        for split_values in grouper(values, 1000):
            query = Fingerprints.objects(hash__in=split_values).values_list('hash','song_id','offset')
            for hash, song_id, offset in query:
                yield (song_id, offset - mapper[hash])

def grouper(iterable, n, fillvalue=None):
	args = [iter(iterable)] * n
	return (list(filter(None, values)) for values in zip_longest(*args, fillvalue=fillvalue))