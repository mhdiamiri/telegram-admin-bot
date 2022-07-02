import sqlite3
import random

def random_fal():
    db = sqlite3.connect('hafez.db')
    r = random.randrange(1, 100)
    aa = db.execute("SELECT * FROM hafez WHERE id =%i"%(r))
    for rr in aa:
        return rr