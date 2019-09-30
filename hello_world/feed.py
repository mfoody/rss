from dataclasses import dataclass


@dataclass
class Feed:
    id: str
    name: str
    url: str

    @staticmethod
    def from_record(record):
        return Feed(record["Id"]["S"], record["Name"]["S"], record["Url"]["S"])

    def to_record(self):
        return {
            "Id": {
                "S": self.id
            },
            "Name": {
                "S": self.name
            },
            "Url": {
                "S": self.url
            }
        }