from typing import Union

from tinydb import TinyDB, Query

db = TinyDB('app/density/database/density.json')
query = Query()
table = db.table('density')

# data_all = table.all()[0]
#
# density: float = data_all['density']


def update_density_db(value: Union[int, float]) -> None:
    table.update({'density': value})


def get_density():
    return table.all()[0]['density']
