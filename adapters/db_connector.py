from sqlmodel import create_engine


class DBConnector:
    def __init__(self):

        sqlite_file_name = "database.db"
        sqlite_url = f"sqlite:///{sqlite_file_name}"

        connect_args = {"check_same_thread": False}
        self.engine = create_engine(sqlite_url, connect_args=connect_args)

    def get_engine(self):
        return self.engine


db_connector = DBConnector()
engine = db_connector.get_engine()
