import configparser
import sqlite3
from enum import Enum

class DatabaseColumns(Enum):
    """
    An enum to represent the columns in the database.
    """
    ID = "id"
    NAME = "name"
    TEXT = "text"
    TIMESTAMP = "timestamp"

class DatabaseManager:
    """
    A class to manage the database.
    """

    def __init__(self):
        # Setting up the configurations.
        config = configparser.ConfigParser()
        config.read("settings/config.ini")

        # Reading the database settings.
        self.db_name = config.get("Database Settings", "database_name")
        self.table_name = config.get("Database Settings", "table_name")
        self.clear = config.getboolean("Database Settings", "clear_db")

        # Connecting to the database.
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Creating the table if it doesn't exist.
        if config.getboolean("Database Settings", "first_run"):
            self.create_table()
            config.set("Database Settings", "first_run", "False")

    def create_table(self, *args) -> None:
        """
        Creates a table in the database with the name specified in the config file.
        
        Parameters:
        args (string): different table name, if such is desired.
        """

        table = self.table_name
        if len(args) > 0:
            table = args[0]

        self.cursor.execute(f"""
        CREATE table IF NOT EXISTS {table}
        (id integer primary key autoincrement,
        name text not null,
        text text not null,
        timestamp datetime default current_timestamp)
        """)
        self.conn.commit()
        

    def insert_db(self, name: str, text: str, *args) -> None:
        """
        Inserts a new row into the database.

        Parameters:
        name (string): the name of the person who sent the message.
        text (string): the text of the message.
        args (string): different table name, if such is desired.
        """

        table = self.table_name
        if len(args) > 0:
            table = args[0]

        self.cursor.execute(f"""
        INSERT INTO {table} (name, text)
        VALUES ('{name}', '{text}')
        """)
        self.conn.commit()

    def query_db(self, **kwargs) -> any:
        """
        Queries the database.

        Parameters:
        kwargs table (string): different table name, if such is desired.
        kwargs columns (list of DatabaseColumns objects): the columns to return.
        kwargs limit (int): the number of rows to return.
        kwargs order_by (string): sort by column.
        kwargs order_asc (bool): sort ascending or descending. Ascending by default.
        """

        query = """select """

        # Add the limit to the query.
        if "limit" in kwargs:
            limit = kwargs["limit"]
            query += f"top {limit} "

        # Add the columns to the query.
        if "columns" in kwargs:
            columns = kwargs["columns"]
            for i in range(len(columns)):
                query += f"{columns[i].value}"
                if i != len(columns) - 1:
                    query += ", "
        else:
            query += "* "

        # Add the table to the query.
        if "table" in kwargs:
            table = kwargs["table"]
            query += f"from {table} "
        else:
            query += f"from {self.table_name} "

        # Add the order by to the query.
        if "order_by" in kwargs:
            order_by = kwargs["order_by"]
            query += f"order by {order_by} "
            if "order_asc" in kwargs:
                order_asc = kwargs["order_asc"]
                if not order_asc:
                    query += "desc "
                else:
                    query += "asc " 

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def clear_table(self, *args):
        """
        Clears the table.

        Parameters:
        table (string): different table name, if such is desired.
        """

        table = self.table_name
        if len(args) > 0:
            table = args[0]

        cursor = self.conn.cursor()
        cursor.execute(f"""
        DELETE FROM {table}
        """)
        # Reset the autoincrement.
        cursor.execute(f"""
        DELETE FROM sqlite_sequence WHERE name='{table}'
        """)
        self.conn.commit()