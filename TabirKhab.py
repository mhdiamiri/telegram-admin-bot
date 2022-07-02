import sqlite3

def search(title):
    db = sqlite3.connect('tabir.db')
    result = db.execute("SELECT * FROM tabir WHERE title LIKE '%"+title+"%'")
    keys = []
    for (fav, i, title, content) in result:
        keys.append([i, title])
    return keys

def re_content(i):
    db = sqlite3.connect('tabir.db')
    result = db.execute('SELECT * FROM tabir WHERE id = %i'%(int(i)))
    for m in result:
        return m[3]
