import mysql.connector


class Idea:
    stl_file_link: str

    def __init__(self, id: int = 0, inserter: str = '', innovator: str = '', admin: str = '', description: str = '',
                 overview: str = '', stl_file_link: str = ''):
        self.id = id
        self.inserter = inserter
        self.innovator = innovator
        self.admin = admin
        self.description = description
        self.overview = overview
        self.stl_file_link = stl_file_link

    def insert_idea(self):
        config = {
            'user': 'root',
            'password': '',
            'host': '127.0.0.1',
            'database': 'petit_popillon',
            'raise_on_warnings': True
        }

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = ("INSERT INTO idea "
                 "( `inserter`, `innovator`, `description`, `overview`,'stl_file') "
                 "VALUES (%s, %s, %s, %s,%s)")

        data = (self.inserter, self.innovator, self.description, self.overview, self.stl_file_link)

        cursor.execute(query, data)
        id = cursor.lastrowid

        # Make sure data is committed to the database
        cnx.commit()

        cursor.close()
        cnx.close()
        return id
