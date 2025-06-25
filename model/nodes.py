from dataclasses import dataclass

import datetime


@dataclass
class Node:
    id: int
    datetime: datetime.date
    city: str
    state:str
    country:str
    shape:str
    duration: int
    duration_hm:str
    comments:str
    date_posted: datetime.date
    latitude: float
    longitude: float

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return str(self.id)