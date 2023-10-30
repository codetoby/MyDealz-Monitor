import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers.webhook import sendWebhook
from helpers.crawler import getDeals

def testSendWebhook():

    deals = getDeals()
    deal = deals[0]
    sendWebhook(deal)

testSendWebhook()
    