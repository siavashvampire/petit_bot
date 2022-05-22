from typing import Optional

from telegram import User
from tinydb import TinyDB, Query

from app.user.model.user import UserDB

db = TinyDB('app/user/database/users.json')
query = Query()
table = db.table('users')


def add_user(user_in: User):
    UserDB(user=user_in, table=table).insert_user()


def get_all_user() -> list[UserDB]:
    users_row = table.all()
    users = []
    for i in users_row:
        users.append(UserDB(id_in=i['id'], username=i['username'], first_name=i['first_name'],
                            idea_flag=i["idea_flag"], table=table))
    return users


def get_user_by_username(username: str) -> Optional[UserDB]:
    search = table.search(query.username == username)
    if len(search):
        search = search[0]
        return UserDB(id_in=search['id'], username=search['username'], first_name=search['first_name'],
                      idea_flag=search["idea_flag"], table=table)
    else:
        return None
