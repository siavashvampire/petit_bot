from telegram import User
from tinydb import Query
from tinydb.table import Table
from app.user.database import table

query = Query()
# idea_admin_id = 72025606
idea_admin_id = 21221221
accounting_admin_id = 99981475


class UserDB(User):
    table: Table
    idea_flag: bool

    def __init__(self, id_in: int = 0, username: str = "", first_name: str = "",
                 last_name: str = "", idea_flag: bool = False, accounting_flag: bool = False):
        self.table = table

        if id_in != 0 and username == "":
            self.id = id_in
            search = self.table.get(query.id == self.id)
            username = search['username']
            first_name = search['first_name']
            self.idea_flag = search['idea_flag']
            self.accounting_flag = search['accounting_flag']
        else:
            self.idea_flag = idea_flag
            self.accounting_flag = accounting_flag

        super().__init__(id=id_in, first_name=first_name, is_bot=False, last_name=last_name, username=username)

    def insert_user(self):
        self.table.upsert(
            {'id': self.id, 'username': self.username, 'first_name': self.first_name,
             'idea_flag': self.idea_flag, 'accounting_flag': self.accounting_flag},
            query.id == self.id)

    def is_idea_admin(self):
        if self.id == idea_admin_id:
            return True
        return False

    def is_accounting_admin(self):
        if self.id == accounting_admin_id:
            return True
        return False

    def can_insert_idea(self):
        if self.idea_flag:
            return True
        return False

    def can_insert_accounting(self):
        if self.accounting_flag:
            return True
        return False

    def change_idea_flag(self, value: bool):
        self.table.update({'idea_flag': value}, query.id == self.id)

    def change_accounting_flag(self, value: bool):
        self.table.update({'accounting_flag': value}, query.id == self.id)
