import logging
import threading
import time
from uuid import uuid4

import requests
import schedule
from bs4 import BeautifulSoup

import feed_repository
import item_repository
from item import Item


def start_polling():
    schedule.every(30).seconds.do(poll_feeds)
    continuous_thread = ScheduleThread()
    continuous_thread.start()


def poll_feeds():
    feeds = feed_repository.get_all_feeds()
    for feed in feeds:
        try:
            response = requests.get(feed.url)
            rss = response.text
            document = BeautifulSoup(rss, "xml")
            items = document.find_all("item")
            for item in items:
                item_id = str(uuid4())
                item_pub_date = None if item.pubDate is None else item.pubDate.text
                item_comments = None if item.comments is None else item.comments.text
                item_repository.create_item(Item(id=item_id, title=item.title.text, link=item.link.text,
                                                 read=False, pubDate=item_pub_date, comments=item_comments,
                                                 description=item.description.text))
        except Exception as ex:
            logging.exception(ex)


cease_continuous_run = threading.Event()


class ScheduleThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.setDaemon(True)

    @classmethod
    def run(cls):
        while not cease_continuous_run.is_set():
            schedule.run_pending()
            time.sleep(10)
