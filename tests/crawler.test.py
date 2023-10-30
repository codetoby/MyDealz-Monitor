import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

from helpers.crawler import filterNewDeals
import mysql.connector as database

def testFilterNewDeals():

    password = os.getenv("password")
    username = os.getenv("username")
    localhost = os.getenv("localhost")
    port = os.getenv("port")

    connection = database.connect(
        user=username[:-1],
        password=password,
        host=localhost,
        port=port,
        database="mydealz"
    )

    cursor = connection.cursor()

    statement = """
        DELETE FROM ids
    """
    cursor.execute(statement)
    connection.commit()

    deals = filterNewDeals()


    assert len(deals) > 0

    statement = """
        DELETE FROM ids
    """
    cursor.execute(statement)
    connection.commit()

    connection.close()

testFilterNewDeals()