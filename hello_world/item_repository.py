import logging
from typing import List

import boto3

from item import Item

db = boto3.client("dynamodb")

try:
    db.create_table(
        TableName="items",
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


TABLE = "items"


def create_item(item: Item) -> Item:
    db.put_item(TableName=TABLE, Item=item.to_record())
    return item


def get_all_items() -> List[Item]:
    items = db.scan(TableName=TABLE)["Items"]
    return list(map(Item.from_record, items))


def get_one_item(item_id: str) -> Item:
    response = db.query(TableName=TABLE,
                    KeyConditionExpression="Id = :item_id",
                    ExpressionAttributeValues={
                        ":item_id": {
                            "S": item_id
                        }
                    })
    if response.count is 1:
        return Item.from_record(response.items[0])
    else:
        return None
