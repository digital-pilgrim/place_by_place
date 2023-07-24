from database.peewee.common.models import db, location_model
from database.peewee.utils.crud import CRUDInterface


db.connect()

db.create_tables([location_model])

crud = CRUDInterface

if __name__ == '__main__':
    crud()
