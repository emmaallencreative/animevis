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
        sql_create_mal_jikan_scores_table = '''CREATE TABLE IF NOT EXISTS mal_jikan_scores (
                     id text, 
                     watching integer,
                     completed integer,
                     on_hold integer,
                     dropped integer,
                     plan_to_watch integer,
                     status_total integer,
                     scores_1_votes integer,
                     scores_1_percentage real,
                     scores_2_votes integer,
                     scores_2_percentage real,
                     scores_3_votes integer,
                     scores_3_percentage real,
                     scores_4_votes integer,
                     scores_4_percentage real,
                     scores_5_votes integer,
                     scores_5_percentage real,
                     scores_6_votes integer,
                     scores_6_percentage real,
                     scores_7_votes integer,
                     scores_7_percentage real,
                     scores_8_votes integer,
                     scores_8_percentage real,
                     scores_9_votes integer,
                     scores_9_percentage real,
                     scores_10_votes integer,
                     scores_10_percentage real,
                     averagescore real,
                     scoredby integer,
                     alltimerank integer,
                     popularityrank integer,
                     popularityvolume integer,
                     favorites integer)'''
        sql_create_mal_jikan_descriptions_table = '''CREATE TABLE IF NOT EXISTS mal_jikan_descriptions (
                             id text, 
                             description text, 
                             background text);'''
        sql_create_mal_jikan_genres_table = '''CREATE TABLE IF NOT EXISTS mal_jikan_genres (
                                     id text, 
                                     genre text)'''
        sql_create_mal_jikan_recommendations_table = '''CREATE TABLE IF NOT EXISTS mal_jikan_recommendations (
                                             id text, 
                                             recommendation_mal_id integer,
                                             recommendation_title text,
                                             recommendation_count integer
                                             )'''
        sql_create_mal_jikan_review_text_table = '''CREATE TABLE IF NOT EXISTS mal_jikan_review_text (
                                             id text, 
                                             review_mal_id integer,
                                             review_text text
                                             )'''

        sql_create_mal_jikan_review_stats_table = '''CREATE TABLE IF NOT EXISTS mal_jikan_review_stats (
                                             id text, 
                                             review_mal_id integer,
                                             helpful_count integer,
                                             review_date text,
                                             episodes_seen integer,
                                             overall_score integer,
                                             story_score integer,
                                             animation_score integer,
                                             sound_score integer,
                                             character_score integer,
                                             enjoyment_score integer
                                             )'''

        # self.cursor.execute(sql_create_animelist_table)
        # self.cursor.execute(sql_create_pagination_table)
        # self.cursor.execute(sql_create_datasource_table)
        # self.cursor.execute(sql_create_details_table)

        self.cursor.execute(sql_create_mal_jikan_scores_table)
        #self.cursor.execute(sql_create_mal_jikan_descriptions_table)
        self.cursor.execute(sql_create_mal_jikan_genres_table)
        self.cursor.execute(sql_create_mal_jikan_recommendations_table)
        self.cursor.execute(sql_create_mal_jikan_review_text_table)
        self.cursor.execute(sql_create_mal_jikan_review_stats_table)


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

d = DOA('../animevis.db')
d.create_tables()