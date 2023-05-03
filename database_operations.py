import sqlite3

class database_operations:

    def __init__(self, name):
        self.__db = sqlite3.connect(name)

    def make_table(self, name, args: list):
        c = self.__db.cursor()
        params = ''

        try:
            for arg in args:
                params = params + arg + ',\n'
            c.execute('''
                            CREATE TABLE records(
                                id INTEGER PRIMARY KEY,
                                name varchar(30),
                                duration INTEGER,
                                blocksize INTEGER,
                                date DATE
                            );
                    ''')
            self.__db.commit()

        except Exception as e:
            print(e)

    def statement(self, statement: str):
        c = self.__db.cursor()
        c.execute(statement)
        return c.fetchall()
    #das ist ein Kommentar