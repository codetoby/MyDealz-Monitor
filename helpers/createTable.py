import mysql.connector as database
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("username")
password = os.getenv("password")
localhost = os.getenv("localhost")
port = os.getenv("port")

connection = database.connect(
    user=username,
    password=password,
    host=localhost,
    port=port,
    database="mydealz"
)

def createTable():

    statementCreateTable = """
    CREATE TABLE IF NOT EXISTS
         `ids` (
            `id` varchar(50) NOT NULL,
            PRIMARY KEY (`id`)
        )
    """
    cursor = connection.cursor()
    cursor.execute(statementCreateTable)
    connection.commit()

    connection.close()
