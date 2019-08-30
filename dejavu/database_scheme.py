from mongoengine import *
import json

# CREATE_SONGS_TABLE
class Songs(Document):
    """
    A class used to store songs details.

    ...

    Attributes
    ----------
    song_id : int
        a unique vaule to represent the each song
    song_name : str
        the name of the songs
    fingerprinted : int
        a value 1 or 0 to define weather the song is fingerprinted
    file_sha1 : binary
        a binary of the hash of the song.
    """
    #auto increment is required
    # song_id= IntField(min_value=0, max_value=16777215, unique=True)
    song_name = StringField(max_length=250)
    fingerprinted = IntField(min_value=0,max_value=1,default=0)
    file_sha1 = StringField(max_bytes=10, null=False, unique=True)

    meta = {
        'indexes': [
            'song_name',
            'file_sha1'
        ]
    }

    def __str__(self):
        return str(self.id)

# CREATE_FINGERPRINTS_TABLE
class Fingerprints(Document):
    """
    A class used to store Fingerprints details.

    ...

    Attributes
    ----------
    hash : binary
        a binary of the hash of the song.
    song_id : reference
        relation to the song collections
    offset : int
        to enter the offset present in the song.
    """
    hash= StringField(max_bytes=10, null=False)
    song_id = ReferenceField(Songs,reverse_delete_rule=CASCADE)
    offset= IntField()

    meta = {
        'indexes': [
            'hash',
            'song_id'
        ],
        'ordering': ['-song_id']
    }