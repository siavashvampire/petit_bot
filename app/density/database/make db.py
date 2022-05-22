from tinydb import TinyDB

dev = True

db = TinyDB('density.json')
db.drop_tables()
table = db.table('density')

table.insert({'density': 5})
