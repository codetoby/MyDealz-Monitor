import requests
import json

with open("./config.json", "r") as f:
    CONFIG = json.load(f)

def sendWebhook(article):
    data = {
        "username": "MyDealz Checker",
        "embeds": [
            {
                "title": article.title,
                "url": article.link,
                "image": {
                    "url": article.image
                },
                "fields": [
                    {
                        "name": "New Price",
                        "value": article.price,
                        "inline": True
                    },
                    {
                        "name": "Shipping Cost",
                        "value": article.shipping,
                        "inline": True
                    },
                    {
                        "name": "Description",
                        "value": article.description,
                        "inline": False
                    },

                ]
            }


        ]
    }
    requests.post(CONFIG["webhook"]["url"], json=data)


