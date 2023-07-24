from database.sqlite.common.models import history_model
from database.sqlite.utils.crud import CRUDInterface


with history_model:
    cursor = history_model.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT,
    user_id INT,
    command_type TEXT,
    place_category TEXT,
    search_result TEXT);
    """)

    history_model.commit()

crud = CRUDInterface

if __name__ == '__main__':
    crud()
