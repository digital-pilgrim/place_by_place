import sqlite3


history_model = sqlite3.connect('history.db', check_same_thread=False)

cursor = history_model.cursor()

cursor.close()
