from typing import Union

from tinydb import TinyDB, Query

db = TinyDB('core/database/config.json')
query = Query()
table = db.table('config')

data_all = table.all()[0]

density: float = data_all['density']
telegram_token: str = data_all['telegram_token']
channel_id: int = data_all['channel_id']


def update_database(key: str, value: Union[int, float]) -> None:
    table.update({key: value})


def get_database(key: str):
    return data_all[key]