from typing import Optional

from telegram import User
from tinydb import Query
from tinydb.table import Table

query = Query()


class UserDB(User):
    table: Optional[Table]
    idea_flag: bool

    def __init__(self, user: User = None, id_in: int = 0, username: str = "", first_name: str = "",
                 last_name: str = "", table: Table = None, idea_flag: bool = False):
        if id_in == 0 and user is not None:
            id_in = user.id
            username = user.username
            first_name = user.first_name
            last_name = user.last_name

        super().__init__(id=id_in, first_name=first_name, is_bot=False, last_name=last_name, username=username)

        self.table = table
        self.idea_flag = idea_flag

    def insert_user(self):
        self.table.upsert(
            {'id': self.id, 'username': self.username, 'first_name': self.first_name, 'idea_flag': self.idea_flag},
            query.id == self.id)

    def is_idea_admin(self):
        if self.id == 72025606:
            return True
        return False

    def can_insert_idea(self):
        if self.idea_flag:
            return True
        return False

    def chang_idea_flag(self, value: bool):
        self.table.update({'idea_flag': value}, query.id == self.id)
