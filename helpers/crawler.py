import requests
from bs4 import BeautifulSoup as bs
from dataclasses import dataclass
import os
import mysql.connector as database
from dotenv import load_dotenv
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

username = os.getenv("username")
password = os.getenv("password")
localhost = os.getenv("localhost")
port = os.getenv("port")

URL = "https://mydealz.de"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

@dataclass
class Deal:
    id: str
    title: str
    image: str
    price: str
    shipping: str
    link: str
    description: str


def getPage():
    response = requests.get(URL, headers=HEADERS)
    soup = bs(response.content, "html.parser")
    return soup


def getDeals():

    foundDeals = []

    soup = getPage()
    deals = soup.find_all("article", class_="thread cept-thread-item thread--type-list imgFrame-container--scale thread--deal")

    for deal in deals:
        try:
            id = deal.get("id")
            title = deal.find("a", class_="cept-tt thread-link linkPlain thread-title--list js-thread-title").get("title")
            link = deal.find("a", class_="cept-tt thread-link linkPlain thread-title--list js-thread-title").get("href")
            image = deal.find("img", class_="thread-image width--all-auto height--all-auto imgFrame-img").get("src")
            price = deal.find("span", class_="thread-price text--b cept-tp size--all-l size--fromW3-xl").text
            description = 'deal.find("div", class_="overflow--wrap-break width--all-12  size--all-s").text'
            shipping = deal.find("span", class_="space--ml-2 size--all-s overflow--wrap-off").text

            foundDeals.append(Deal(id, title, image, price, shipping, link, description))
        except Exception:
            pass

    return foundDeals



def filterNewDeals():
    connection = database.connect(
        user=username,
        password=password,
        host=localhost,
        port=port,
        database="mydealz"
    )
    cursor = connection.cursor()
    deals = getDeals()
    newDeals = []
    newIds = []
    try:
        statement = "SELECT id FROM ids"
        cursor.execute(statement)
        ids = [id[0] for id in cursor]
        for deal in deals:
            if deal.id not in ids:
                newDeals.append(deal)
                newIds.append(deal.id)
        if newIds:
            try:
                statement = "INSERT INTO ids (id) VALUES (%s)"
                cursor.executemany(statement, [(id,) for id in newIds])
                connection.commit()
            except Exception as e:
                connection.rollback()
                logging.error(f"Error inserting entries into database: {e}")
    except Exception as e:
        logging.error(f"Error retrieving entry from database: {e}")
    finally:
        cursor.close()
        connection.close()
    return newDeals

