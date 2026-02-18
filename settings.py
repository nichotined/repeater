from lib.database import Database


# init db
database = Database()
database.connect()
database.init_tables()
