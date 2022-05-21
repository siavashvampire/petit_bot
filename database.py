from typing import Union

from tinydb import TinyDB, Query

db = TinyDB('database/config.json')
query = Query()
table = db.table('config')
# table.insert({'density':5})
data_all = table.all()[0]

density: float = data_all['density']


def update_database(key: str, value: Union[int, float]) -> None:
    table.update({key: value})


def get_database(key: str):
    return data_all[key]


def insert_database(id: int, step: int, value: int):
    return db.insert({'id': id, 'step': step, 'value': value})


def get_database_step_by_id(id: int):
    return db.get(query.id == id)
