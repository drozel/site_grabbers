from sqlitedict import SqliteDict

FileName = "data/cars.sqlite"

def save(data):
    db = SqliteDict(FileName)
    for k,v in data.items():
        db[k] = v
    db.commit()

def load():
    db = SqliteDict(FileName)
    data = dict(db)
    db.close()
    return data