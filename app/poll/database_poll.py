from typing import Union

from tinydb import TinyDB, Query, where

db = TinyDB('database/poll.json')
query = Query()
table = db.table('config')


# data_all = table.all()[0]

def update_database(key: str, value: Union[int, float]) -> None:
    table.update({key: value})


def insert_database(id: int, step: int, value: int):
    return db.insert({'id': id, 'step': step, 'value': value})


def get_database_step_by_id(id: int):
    result = db.search(query.id == id)
    if result:
        return result[-1]['step']
    else:
        return None


def get_database_by_step(step: int):
    result = db.search(query.step == step)
    if result:
        return result
    else:
        return None


def get_database_mean_by_step(step: int):
    result = get_database_by_step(step)
    value = 0
    for i in result:
        value += i['value']

    value /= len(result)
    return value

def delete_database_by_id(id):
    db.remove(where('id') == id)
