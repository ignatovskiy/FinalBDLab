import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from db_functions import DataBase

accswin, eventswin = None, None


def create_database():
    status = db.create_database()

    if not status:
        messagebox.showinfo("Information", "DB is already created! Opening DB.")
    global accswin, eventswin
    if accswin is None and eventswin is None:
        accswin = AccountsWindow()
        eventswin = EventsWindow()


def delete_database():
    db.delete_database()

    if accswin is not None:
        accswin.destroy()
        eventswin.destroy()
    else:
        messagebox.showerror("Error!", "DB is not found!")


class MainWindow(tk.Frame):
    def __init__(self):
        super().__init__(main_window)
        self.create_db = tk.PhotoImage(file="create_db.png")
        self.delete_db = tk.PhotoImage(file="delete_db.png")

        buttons_bar = tk.Frame(bg='#FFFFFF', bd=2)
        buttons_bar.pack(side=tk.TOP, fill=tk.X)
        btn_create_db = tk.Button(buttons_bar,
                                  text='Create/Open DB',
                                  command=create_database,
                                  bg='#FFFFFF',
                                  compound=tk.TOP,
                                  image=self.create_db)
        btn_delete_db = tk.Button(buttons_bar,
                                  text='Delete DB',
                                  command=delete_database,
                                  bg='#FFFFFF',
                                  compound=tk.TOP,
                                  image=self.delete_db)

        btn_create_db.pack(side=tk.LEFT)
        btn_delete_db.pack(side=tk.LEFT)


class AccountsWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.columns_accounts = (
        "id", "nickname", "battles_amount", "average_damage", "clan", "tanks_amount", "events_amount")

        self.add_record = tk.PhotoImage(file="add_record.png")
        self.edit_record = tk.PhotoImage(file="edit_record.png")
        self.delete_record = tk.PhotoImage(file="delete_record.png")
        self.find_record = tk.PhotoImage(file="find_record.png")

        self.accounts_list = ttk.Treeview(self, columns=self.columns_accounts, height=100, show="headings")
        for heading in self.columns_accounts:
            self.accounts_list.heading(heading, text=heading.replace("_", " ").title())
            self.accounts_list.column(heading, width=50)

        self.accounts_list.bind('<Button>', self.handle_click_accounts)

        self.title("Accounts Info")
        self.geometry("900x350")

        self.init_buttons()
        self.accounts_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.show_accounts()


    def init_buttons(self):
        accs_buttons_bar = tk.Frame(master=self, bg='#FFFFFF', bd=2)
        accs_buttons_bar.pack(side=tk.TOP, fill=tk.X)

        accs_btn_add_record = tk.Button(accs_buttons_bar,
                                   text='Add',
                                   command=self.add_record_to_DB,
                                   bg='#FFFFFF',
                                   compound=tk.TOP,
                                   image=self.add_record)
        accs_btn_edit_record = tk.Button(accs_buttons_bar,
                                    text='Edit',
                                    command=self.edit_record_in_DB,
                                    bg='#FFFFFF',
                                    compound=tk.TOP,
                                    image=self.edit_record)
        accs_btn_delete_record = tk.Button(accs_buttons_bar,
                                      text='Delete',
                                      command=self.delete_records_from_db,
                                      bg='#FFFFFF',
                                      compound=tk.TOP,
                                      image=self.delete_record)
        accs_btn_find_record = tk.Button(accs_buttons_bar,
                                    text='Find',
                                    command=self.search_file_in_DB,
                                    bg='#FFFFFF',
                                    compound=tk.TOP,
                                    image=self.find_record)

        accs_btn_add_record.pack(side=tk.LEFT)
        accs_btn_edit_record.pack(side=tk.LEFT)
        accs_btn_delete_record.pack(side=tk.LEFT)
        accs_btn_find_record.pack(side=tk.LEFT)

    def handle_click_accounts(self, event):
        if self.accounts_list.identify_region(event.x, event.y) == "separator":
            return "break"

    def show_accounts(self):
        db.get_accounts()
        [self.accounts_list.delete(i) for i in self.accounts_list.get_children()]
        for row in db.cursor.fetchall():
            self.accounts_list.insert('', "end", values=row)

    def add_record_to_DB(self):
        AddRecordWindowAccs(window=self)

    def edit_record_in_DB(self):
        if self.accounts_list.selection():
            EditRecordWindowAccs(window=self, selection=self.accounts_list.set(self.accounts_list.selection()[0]))

    def delete_records_from_db(self):
        if self.accounts_list.selection():
            db.delete_account_by_id(self.accounts_list.set(self.accounts_list.selection()[0])["id"])
            self.show_accounts()
        else:
            DeleteAccsWindow(window=self)

    def search_file_in_DB(self):
        SearchRecordAccsWindow()


class EventsWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.columns_events = ("id", "event_name", "event_prize", "account_id")
        self.add_record = tk.PhotoImage(file="add_record.png")
        self.edit_record = tk.PhotoImage(file="edit_record.png")
        self.delete_record = tk.PhotoImage(file="delete_record.png")
        self.find_record = tk.PhotoImage(file="find_record.png")

        self.title("Event info")
        self.geometry("600x350")

        self.events_list = ttk.Treeview(self, columns=self.columns_events, height=100, show="headings")
        for heading in self.columns_events:
            self.events_list.heading(heading, text=heading.replace("_", " ").title())
            self.events_list.column(heading, width=50)

        self.events_list.bind('<Button>', self.handle_click_events)

        self.init_buttons()
        self.events_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.show_events()

    def init_buttons(self):
        buttons_bar = tk.Frame(master=self, bg='#FFFFFF', bd=2)
        buttons_bar.pack(side=tk.TOP, fill=tk.X)

        btn_add_record = tk.Button(buttons_bar,
                                   text='Add',
                                   command=self.add_record_to_DB,
                                   bg='#FFFFFF',
                                   compound=tk.TOP,
                                   image=self.add_record)
        btn_edit_record = tk.Button(buttons_bar,
                                    text='Edit',
                                    command=self.edit_record_in_DB,
                                    bg='#FFFFFF',
                                    compound=tk.TOP,
                                    image=self.edit_record)
        btn_delete_record = tk.Button(buttons_bar,
                                      text='Delete',
                                      command=self.delete_records_from_db,
                                      bg='#FFFFFF',
                                      compound=tk.TOP,
                                      image=self.delete_record)
        btn_find_record = tk.Button(buttons_bar,
                                    text='Find',
                                    command=self.search_file_in_DB,
                                    bg='#FFFFFF',
                                    compound=tk.TOP,
                                    image=self.find_record)

        btn_add_record.pack(side=tk.LEFT)
        btn_edit_record.pack(side=tk.LEFT)
        btn_delete_record.pack(side=tk.LEFT)
        btn_find_record.pack(side=tk.LEFT)


    def handle_click_events(self, event):
        if self.events_list.identify_region(event.x, event.y) == "separator":
            return "break"

    def show_events(self):
        db.get_events()
        [self.events_list.delete(i) for i in self.events_list.get_children()]
        [self.events_list.insert('', 'end', values=row) for row in db.cursor.fetchall()]

    def add_record_to_DB(self):
        AddRecordWindowEvents(window=self)

    def edit_record_in_DB(self):
        if self.events_list.selection():
            EditRecordWindowEvents(window=self, selection=self.events_list.set(self.events_list.selection()[0]))

    def delete_records_from_db(self):
        if self.events_list.selection():
            db.delete_account_by_id(self.events_list.set(self.events_list.selection()[0])["id"])
            self.show_events()
        else:
            DeleteEventsWindow(window=self)

    def search_file_in_DB(self):
        SearchRecordEventsWindow()


class AddRecordWindowAccs(tk.Toplevel):
    def __init__(self, window):
        super().__init__()
        self.columns_accounts = (
            "id", "nickname", "battles_amount", "average_damage", "clan", "tanks_amount", "events_amount")

        self.window = window

        self.entry_id = ttk.Entry(self)
        self.entry_nickname = ttk.Entry(self)
        self.entry_battles = ttk.Entry(self)
        self.entry_damage = ttk.Entry(self)
        self.entry_tanks = ttk.Entry(self)
        self.entry_clan = ttk.Entry(self)
        self.entry_events = ttk.Entry(self)

        self.button_add = ttk.Button(self, text="Add")
        self.button_cancel = ttk.Button(self, text="Close", command=self.destroy)

        self.init_window_entities()

    def init_window_entities(self):
        self.title("Adding account record to DB")
        self.geometry('360x300+400+300')
        self.resizable(False, False)

        label_id = tk.Label(self, text="ID")
        label_id.place(x=10, y=20)
        label_nickname = tk.Label(self, text="Nickname")
        label_nickname.place(x=10, y=50)
        label_battles = tk.Label(self, text="Battles")
        label_battles.place(x=10, y=80)
        label_damage = tk.Label(self, text="Damage")
        label_damage.place(x=10, y=110)
        label_tanks = tk.Label(self, text="Tanks")
        label_tanks.place(x=10, y=140)
        label_clan = tk.Label(self, text="Clan")
        label_clan.place(x=10, y=170)

        self.entry_id.place(x=150, y=20)
        self.entry_nickname.place(x=150, y=50)
        self.entry_battles.place(x=150, y=80)
        self.entry_damage.place(x=150, y=110)
        self.entry_tanks.place(x=150, y=140)
        self.entry_clan.place(x=150, y=170)

        self.button_add.place(x=65, y=270)
        self.button_add.bind('<Button-1>',
                             lambda event: self.adding_record([int(self.entry_id.get()),
                                                              self.entry_nickname.get(),
                                                              int(self.entry_battles.get()),
                                                              int(self.entry_damage.get()),
                                                              self.entry_clan.get(),
                                                              int(self.entry_tanks.get())]))

        self.button_cancel.place(x=200, y=270)

    def adding_record(self, fields_list):
        db.add_account(id_=fields_list[0], nickname=fields_list[1], battles_amount=fields_list[2],
                       average_damage=fields_list[3], clan=fields_list[4], tanks_amount=fields_list[5])
        self.window.show_accounts()
        eventswin.show_events()
        self.destroy()


class AddRecordWindowEvents(tk.Toplevel):
    def __init__(self, window):
        super().__init__()
        self.columns_events = ("id", "event_name", "event_prize", "account_id")

        self.entry_id = ttk.Entry(self)
        self.entry_event_name = ttk.Entry(self)
        self.entry_event_prize = ttk.Entry(self)
        self.entry_account_id = ttk.Entry(self)

        self.button_add = ttk.Button(self, text="Add")
        self.button_cancel = ttk.Button(self, text="Close", command=self.destroy)

        self.window = window

        self.init_window_entities()

    def init_window_entities(self):
        self.title("Adding events record to DB")
        self.geometry('360x300+400+300')
        self.resizable(False, False)

        label_id = tk.Label(self, text="ID")
        label_id.place(x=10, y=20)
        label_event_name = tk.Label(self, text="Event Name")
        label_event_name.place(x=10, y=50)
        label_event_prize = tk.Label(self, text="Event Prize")
        label_event_prize.place(x=10, y=80)
        label_account_id = tk.Label(self, text="Account ID")
        label_account_id.place(x=10, y=110)

        self.entry_id.place(x=150, y=20)
        self.entry_event_name.place(x=150, y=50)
        self.entry_event_prize.place(x=150, y=80)
        self.entry_account_id.place(x=150, y=110)

        self.button_add.place(x=65, y=270)
        self.button_add.bind('<Button-1>',
                             lambda event: self.adding_record([int(self.entry_id.get()),
                                                              self.entry_event_name.get(),
                                                              int(self.entry_event_prize.get()),
                                                              int(self.entry_account_id.get())]))

        self.button_cancel.place(x=200, y=270)

    def adding_record(self, fields_list):
        db.add_event(id_=fields_list[0], event_name=fields_list[1], event_prize=fields_list[2],
                       account_id=fields_list[3])
        self.window.show_events()
        accswin.show_accounts()
        self.destroy()


class EditRecordWindowAccs(tk.Toplevel):
    def __init__(self, window, selection):
        super().__init__()
        self.columns_accounts = (
            "id", "nickname", "battles_amount", "average_damage", "clan", "tanks_amount", "events_amount")
        self.selection = selection
        self.window = window

        self.entry_id = ttk.Entry(self)
        self.entry_nickname = ttk.Entry(self)
        self.entry_battles = ttk.Entry(self)
        self.entry_damage = ttk.Entry(self)
        self.entry_tanks = ttk.Entry(self)
        self.entry_clan = ttk.Entry(self)
        self.entry_events = ttk.Entry(self)

        self.button_add = ttk.Button(self, text="Edit")
        self.button_cancel = ttk.Button(self, text="Close", command=self.destroy)

        self.init_window_entities()

    def init_window_entities(self):
        self.title("Editing account record to DB")
        self.geometry('360x300+400+300')
        self.resizable(False, False)

        label_id = tk.Label(self, text="ID")
        label_id.place(x=10, y=20)
        label_nickname = tk.Label(self, text="Nickname")
        label_nickname.place(x=10, y=50)
        label_battles = tk.Label(self, text="Battles")
        label_battles.place(x=10, y=80)
        label_damage = tk.Label(self, text="Damage")
        label_damage.place(x=10, y=110)
        label_tanks = tk.Label(self, text="Tanks")
        label_tanks.place(x=10, y=140)
        label_clan = tk.Label(self, text="Clan")
        label_clan.place(x=10, y=170)
        label_events = tk.Label(self, text="Events")
        label_events.place(x=10, y=200)

        self.entry_id.place(x=150, y=20)
        self.entry_nickname.place(x=150, y=50)
        self.entry_battles.place(x=150, y=80)
        self.entry_damage.place(x=150, y=110)
        self.entry_tanks.place(x=150, y=140)
        self.entry_clan.place(x=150, y=170)
        self.entry_events.place(x=150, y=200)

        self.entry_id.insert(0, self.selection['id'])
        self.entry_nickname.insert(0, self.selection['nickname'])
        self.entry_battles.insert(0, self.selection['battles_amount'])
        self.entry_damage.insert(0, self.selection['average_damage'])
        self.entry_tanks.insert(0, self.selection['tanks_amount'])
        self.entry_clan.insert(0, self.selection['clan'])
        self.entry_events.insert(0, self.selection['events_amount'])

        self.button_add.place(x=65, y=270)
        self.button_add.bind('<Button-1>',
                             lambda event: self.editing_record([int(self.entry_id.get()),
                                                               self.entry_nickname.get(),
                                                               int(self.entry_battles.get()),
                                                               int(self.entry_damage.get()),
                                                               self.entry_clan.get(),
                                                               int(self.entry_tanks.get()),
                                                               int(self.entry_events.get())]))

        self.button_cancel.place(x=200, y=270)

    def editing_record(self, fields_list):
        db.edit_account(id_=fields_list[0], nickname=fields_list[1], battles_amount=fields_list[2],
                       average_damage=fields_list[3], clan=fields_list[4], tanks_amount=fields_list[5],
                       events_amount=fields_list[6])
        self.window.show_accounts()
        eventswin.show_events()
        self.destroy()


class EditRecordWindowEvents(tk.Toplevel):
    def __init__(self, window, selection):
        super().__init__()
        self.columns_events = ("id", "event_name", "event_prize", "account_id")

        self.entry_id = ttk.Entry(self)
        self.entry_event_name = ttk.Entry(self)
        self.entry_event_prize = ttk.Entry(self)
        self.entry_account_id = ttk.Entry(self)

        self.button_add = ttk.Button(self, text="Edit")
        self.button_cancel = ttk.Button(self, text="Close", command=self.destroy)

        self.window = window
        self.selection = selection

        self.init_window_entities()

    def init_window_entities(self):
        self.title("Editing events record to DB")
        self.geometry('360x300+400+300')
        self.resizable(False, False)

        label_id = tk.Label(self, text="ID")
        label_id.place(x=10, y=20)
        label_event_name = tk.Label(self, text="Event Name")
        label_event_name.place(x=10, y=50)
        label_event_prize = tk.Label(self, text="Event Prize")
        label_event_prize.place(x=10, y=80)
        label_account_id = tk.Label(self, text="Account ID")
        label_account_id.place(x=10, y=110)

        self.entry_id.place(x=150, y=20)
        self.entry_event_name.place(x=150, y=50)
        self.entry_event_prize.place(x=150, y=80)
        self.entry_account_id.place(x=150, y=110)

        self.entry_id.insert(0, self.selection['id'])
        self.entry_event_name.insert(0, self.selection['event_name'])
        self.entry_event_prize.insert(0, self.selection['event_prize'])
        self.entry_account_id.insert(0, self.selection['account_id'])

        self.button_add.place(x=65, y=270)
        self.button_add.bind('<Button-1>',
                             lambda event: self.editing_record([int(self.entry_id.get()),
                                                              self.entry_event_name.get(),
                                                              int(self.entry_event_prize.get()),
                                                              int(self.entry_account_id.get())]))

        self.button_cancel.place(x=200, y=270)

    def editing_record(self, fields_list):
        db.edit_event(id_=fields_list[0], event_name=fields_list[1], event_prize=fields_list[2],
                       account_id=fields_list[3])
        self.window.show_events()
        accswin.show_accounts()
        self.destroy()


class DeleteAccsWindow(tk.Toplevel):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.resizable(False, False)
        self.title("Deleting")
        self.geometry('360x100+400+300')

        self.button_delete_all = ttk.Button(self, text="Delete all tables", command=self.delete_all)
        self.button_delete_accs = ttk.Button(self, text="Delete this table", command=self.delete_accs)
        self.button_cancel = ttk.Button(self, text="Close", command=self.destroy)

        self.button_delete_all.place(x=10, y=10)
        self.button_delete_accs.place(x=140, y=10)
        self.button_cancel.place(x=270, y=10)

        self.button_search = ttk.Button(self, text="Delete")

        label_nickname = tk.Label(self, text="Nickname")
        label_nickname.place(x=10, y=50)
        self.entry_nickname = ttk.Entry(self)
        self.entry_nickname.place(x=80, y=50)

        self.button_search.place(x=280, y=50)
        self.button_search.bind('<Button-1>',
                                lambda event: self.delete_record(str(self.entry_nickname.get())))

    def delete_accs(self):
        db.clean_accounts()
        self.window.show_accounts()

    def delete_all(self):
        db.clean_accounts()
        db.clean_events()
        self.window.show_accounts()
        eventswin.show_events()

    def delete_record(self, nickname):
        db.delete_account_by_nickname(nickname)
        self.window.show_accounts()


class DeleteEventsWindow(tk.Toplevel):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.resizable(False, False)
        self.title("Deleting")
        self.geometry('360x100+400+300')

        self.button_delete_all = ttk.Button(self, text="Delete all tables", command=self.delete_all)
        self.button_delete_events = ttk.Button(self, text="Delete this table", command=self.delete_accs)
        self.button_cancel = ttk.Button(self, text="Close", command=self.destroy)

        self.button_delete_all.place(x=10, y=10)
        self.button_delete_events.place(x=140, y=10)
        self.button_cancel.place(x=270, y=10)

        self.button_search = ttk.Button(self, text="Delete")

        label_nickname = tk.Label(self, text="Event Name")
        label_nickname.place(x=10, y=50)
        self.entry_nickname = ttk.Entry(self)
        self.entry_nickname.place(x=90, y=50)

        self.button_search.place(x=280, y=50)
        self.button_search.bind('<Button-1>',
                                lambda event: self.delete_record(str(self.entry_nickname.get())))

    def delete_accs(self):
        db.clean_events()
        self.window.show_events()

    def delete_all(self):
        db.clean_accounts()
        db.clean_events()
        self.window.show_events()
        accswin.show_accounts()

    def delete_record(self, event_name):
        db.delete_event_by_name(event_name)
        self.window.show_events()


class SearchRecordAccsWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.geometry("300x100")
        self.button_search = ttk.Button(self, text="Search")
        self.title("Finding accounts")

        label_nickname = tk.Label(self, text="Nickname")
        label_nickname.place(x=10, y=20)
        self.entry_nickname = ttk.Entry(self)
        self.entry_nickname.place(x=90, y=20)

        self.button_search.place(x=110, y=70)
        self.button_search.bind('<Button-1>',
                                lambda event: self.search_record(self.entry_nickname.get()))

    def search_record(self, nickname):
        SearchResultsAccsWindow(nickname=nickname)


class SearchResultsAccsWindow(tk.Toplevel):
    def __init__(self, nickname):
        super().__init__()
        self.columns_accounts = (
        "id", "nickname", "battles_amount", "average_damage", "clan", "tanks_amount", "events_amount")

        self.nickname = nickname

        self.resizable(False, False)
        self.accounts_list = ttk.Treeview(self, columns=self.columns_accounts, height=100, show="headings")
        for heading in self.columns_accounts:
            self.accounts_list.heading(heading, text=heading.replace("_", " ").title())
            self.accounts_list.column(heading, width=50)

        self.accounts_list.bind('<Button>', self.handle_click_accounts)

        self.title("Accounts Info")
        self.geometry("900x350")

        self.accounts_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        db.find_account(nickname=self.nickname)
        [self.accounts_list.delete(i) for i in self.accounts_list.get_children()]
        [self.accounts_list.insert('', 'end', values=row) for row in db.cursor.fetchall()]

    def handle_click_accounts(self, event):
        if self.accounts_list.identify_region(event.x, event.y) == "separator":
            return "break"


class SearchRecordEventsWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.geometry("300x100")
        self.button_search = ttk.Button(self, text="Search")
        self.title("Finding events")

        label_nickname = tk.Label(self, text="Event Name")
        label_nickname.place(x=10, y=20)
        self.entry_nickname = ttk.Entry(self)
        self.entry_nickname.place(x=90, y=20)

        self.button_search.place(x=110, y=70)
        self.button_search.bind('<Button-1>',
                                lambda event: self.search_record(self.entry_nickname.get()))

    def search_record(self, event_name):
        SearchResultsEventsWindow(event_name=event_name)


class SearchResultsEventsWindow(tk.Toplevel):
    def __init__(self, event_name):
        super().__init__()
        self.columns_events = ("id", "event_name", "event_prize", "account_id")

        self.event_name = event_name

        self.resizable(False, False)
        self.events_list = ttk.Treeview(self, columns=self.columns_events, height=100, show="headings")
        for heading in self.columns_events:
            self.events_list.heading(heading, text=heading.replace("_", " ").title())
            self.events_list.column(heading, width=50)

        self.events_list.bind('<Button>', self.handle_click_events)

        self.title("Events Info")
        self.geometry("900x350")

        self.events_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        db.find_event(event_name=self.event_name)
        [self.events_list.delete(i) for i in self.events_list.get_children()]
        [self.events_list.insert('', 'end', values=row) for row in db.cursor.fetchall()]

    def handle_click_events(self, event):
        if self.events_list.identify_region(event.x, event.y) == "separator":
            return "break"


if __name__ == "__main__":
    db = DataBase()
    main_window = tk.Tk()
    application = MainWindow()
    application.pack()
    main_window.title("DB")
    main_window.geometry("170x90+300+200")
    main_window.resizable(False, False)
    main_window.mainloop()
