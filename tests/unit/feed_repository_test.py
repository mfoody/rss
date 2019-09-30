from uuid import uuid4

import feed_repository
from feed import Feed


def test_create_and_get():
    feed = Feed(id=str(uuid4()), name="High Scalability", url="http://www.google.com")
    response = feed_repository.create_feed(feed)
    assert feed == response

