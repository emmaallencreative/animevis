import sqlite3


class DOA:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        sql_create_pagination_table = """ CREATE TABLE IF NOT EXISTS pagination (
                                                last_scraped_page integer,
                                                last_scraped_anime_id integer
                                            ); """
        sql_create_animelist_table = '''CREATE TABLE IF NOT EXISTS animelist (
                 id text, 
                 idanilist integer, 
                 idmal integer, 
                 title text, 
                 startdate text, 
                 enddate text, 
                 season text)'''
        sql_create_datasource_table = """ CREATE TABLE IF NOT EXISTS datasource (
                                                    datasource_name text,
                                                    datasource_id INTEGER PRIMARY KEY AUTOINCREMENT
                                                ); """
        sql_create_details_table = '''CREATE TABLE IF NOT EXISTS details (
                     id text, 
                     description text, 
                     status text, 
                     format text, 
                     animesource text,
                     episodes integer, 
                     datasource integer)'''
        # self.cursor.execute(sql_create_animelist_table)
        # self.cursor.execute(sql_create_pagination_table)
        # self.cursor.execute(sql_create_datasource_table)
        # self.cursor.execute(sql_create_details_table)

    def database_qc(self, action):
        if action == 'select':
            self.cursor.execute('''SELECT * FROM animelist''')
            data = self.cursor.fetchall()
            print(data)
        elif action == 'delete':
            self.cursor.execute('''DELETE FROM animelist where id > 0''')

    def enter_data(self):
        self.cursor.execute("""INSERT INTO datasource (datasource_name) 
            VALUES ('Anilist')""")
        self.conn.commit()

    def add_column(self):
        anilist_column = """ALTER TABLE animelist
                            ADD idanilist integer"""
        self.cursor.execute(anilist_column)

    def update_column(self):
        move_idanilist = """UPDATE animelist SET
                            idanilist=id
                            id=unique_id
                            WHERE product_id = 102"""
        self.cursor.execute(move_idanilist)
