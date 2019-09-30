import logging
from typing import List

import boto3
from feed import Feed

db = boto3.client("dynamodb")

try:
    db.create_table(
        TableName="feeds",
        AttributeDefinitions=[
            {
                "AttributeName": "Id",
                "AttributeType": "S"
            }
        ],
        KeySchema=[
            {
                "AttributeName": "Id",
                "KeyType": "HASH"
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        }
    )
except Exception as ex:
    logging.error(ex)


TABLE = "feeds"


def create_feed(feed: Feed) -> Feed:
    db.put_item(TableName=TABLE, Item=feed.to_record())
    return feed


def get_all_feeds() -> List[Feed]:
    feeds = db.scan(TableName=TABLE)["Items"]
    return list(map(Feed.from_record, feeds))

