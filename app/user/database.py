from tinydb import TinyDB, Query


db = TinyDB('app/user/database/users.json')
query = Query()
table = db.table('users')