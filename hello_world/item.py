from dataclasses import dataclass
from typing import Dict


@dataclass
class Item:
    id: str
    title: str
    link: str
    read: bool
    pubDate: str
    comments: str
    description: str

    @staticmethod
    def from_record(record: Dict):
        return Item(record["Id"]["S"], record["Title"]["S"], record["Link"]["S"],
                    read=record["Read"]["N"] is 1 if "Read" in record else False,
                    pubDate=record["PubDate"]["S"] if "PubDate" in record else None,
                    comments=record["Comments"]["S"] if "Comments" in record else None,
                    description=record["Description"]["S"] if "Description" in record else None,)

    def to_record(self):
        record = {
            "Id": {
                "S": self.id
            },
            "Title": {
                "S": self.title
            },
            "Link": {
                "S": self.title
            },
            "Read": {
                "N": 1 if self.read else 0
            }
        }
        if self.pubDate is not None:
            record["PubDate"] = {
                "S": self.pubDate
            }

        if self.comments is not None:
            record["Comments"] = {
                "S": self.comments
            }

        if self.description is not None:
            record["Description"] = {
                "S": self.description
            }

        return record
