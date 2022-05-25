from telegram import User
from app.user.model.user_model import UserDB
from app.user.database import table
from tinydb import Query

query = Query()


def get_user(id: int = 0, username: str = "", user: User = None) -> UserDB:
    query_text = ""
    if id != 0:
        query_text = query.id == id
    elif username != "":
        query_text = query.username == username
    elif user is not None:
        return UserDB(id_in=user.id, username=user.username, first_name=user.first_name, last_name=user.last_name)

    search = table.search(query_text)

    if len(search):
        search = search[0]
        return UserDB(id_in=search['id'])
    else:
        return UserDB()


def add_user(user_in: User):
    get_user(user=user_in).insert_user()


def get_all_user() -> list[UserDB]:
    users_row = table.all()
    users = []
    for i in users_row:
        users.append(UserDB(id_in=i['id'], username=i['username'], first_name=i['first_name'],
                            idea_flag=i["idea_flag"]))
    return users
