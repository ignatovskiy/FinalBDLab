import psycopg2

from sqlfunctions import sql_functions


class DataBase:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.is_created = False
        self.is_damaged = False

    def connect(self):
        self.connection = psycopg2.connect(database="tanksdatabase", user="postgres", password="postgres",
                                           host="127.0.0.1", port="5432")
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql_functions)

    def create_database(self):
        try:
            if not self.is_created:
                self.connection = psycopg2.connect(user="postgres", password="postgres",
                                                   host="127.0.0.1", port="5432")
                self.connection.autocommit = True
                self.cursor = self.connection.cursor()
                self.cursor.execute(sql_functions)
                self.cursor.execute(f"""SELECT create_database()""")
                self.connection.close()
                self.connect()
                self.cursor.execute(f"""SELECT create_accounts_info()""")
                self.cursor.execute(f"""SELECT create_event_info()""")
                self.is_created = True
                return True
        except:
            self.is_damaged = True
            return False


        else:
            return False

    def delete_database(self):
        self.connection = psycopg2.connect(user="postgres", password="postgres",
                                           host="127.0.0.1", port="5432")
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql_functions)
        self.cursor.execute(f"""SELECT delete_database()""")
        self.is_created = False
        if self.is_damaged is True:
            self.is_damaged = False
            self.delete_database()

    def get_accounts(self):
        self.cursor.execute(f"""SELECT * FROM get_accounts()""")

    def get_events(self):
        self.cursor.execute(f"""SELECT * FROM get_events()""")

    def clean_accounts(self):
        self.cursor.execute(f"""SELECT clear_accounts()""")

    def clean_events(self):
        self.cursor.execute(f"""SELECT clear_events()""")

    def add_account(self, id_=-1, nickname="", battles_amount=0, average_damage=0, clan="", tanks_amount=0, events_amount=0):
        self.cursor.execute(f"""SELECT add_account({id_}, '{nickname}', {battles_amount}, {average_damage}, '{clan}', {tanks_amount}, {events_amount})""")

    def add_event(self, id_=-1, event_name="", event_prize=0, account_id=-1):
        self.cursor.execute(f"""SELECT add_event({id_}, '{event_name}', {event_prize}, {account_id})""")

    def edit_account(self, id_=-1, nickname="", battles_amount=0, average_damage=0, clan="", tanks_amount=0, events_amount=0):
        self.cursor.execute(f"""SELECT edit_account({id_}, '{nickname}', {battles_amount}, {average_damage}, '{clan}', {tanks_amount}, {events_amount})""")

    def edit_event(self, id_=-1, event_name="", event_prize=0, account_id=-1):
        self.cursor.execute(f"""SELECT edit_event({id_}, '{event_name}', {event_prize}, {account_id})""")

    def find_account(self, nickname):
        self.cursor.execute(f"""SELECT * FROM find_account('{nickname}')""")

    def find_event(self, event_name):
        self.cursor.execute(f"""SELECT * FROM find_event('{event_name}')""")

    def delete_account_by_id(self, id_):
        self.cursor.execute(f"""SELECT delete_account_by_id({id_})""")

    def delete_account_by_nickname(self, nickname):
        self.cursor.execute(f"""SELECT delete_account_by_nickname('{nickname}')""")

    def delete_event_by_id(self, id_):
        self.cursor.execute(f"""SELECT delete_event_by_id({id_})""")

    def delete_event_by_name(self, event_name):
        self.cursor.execute(f"""SELECT delete_event_by_name('{event_name}')""")