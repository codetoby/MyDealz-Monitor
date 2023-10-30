import logging
import time
from helpers.createTable import createTable
from helpers.crawler import filterNewDeals
from helpers.webhook import sendWebhook

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Started MyDealz Monitor")
    try:
        createTable()
    except Exception as e:
        logging.error(f"Failed to create table: {e}")
        return

    try:
        filterNewDeals()
    except Exception as e:
        logging.error(f"Failed to filter new deals: {e}")
        return
    
    while True:
        logging.info("Still searching...")       
        try:
            deals = filterNewDeals()
            for deal in deals:
                try:
                    sendWebhook(deal)
                    logging.info(f"New Deal {deal.title} {deal.link}")
                except Exception as e:
                    logging.error(f"Failed to send webhook for deal {deal.title}: {e}")
        except Exception as e:
            logging.error(f"Failed to filter new deals: {e}")
        time.sleep(30)

if __name__ == "__main__":
    main()

