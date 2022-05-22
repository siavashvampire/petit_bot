from tinydb import TinyDB

dev = True

db = TinyDB('../database/config.json')
db.drop_tables()
table = db.table('config')

table.insert({'density': 5})
table.update({'telegram_token': "5377461148:AAFekpap_Fs-C-_3CVPi50nexYOsAQK-IuQ"})

if dev:
    table.update({'channel_id': -1001757304606})  # test
else:
    table.update({'channel_id': -1001567906020})  # main
