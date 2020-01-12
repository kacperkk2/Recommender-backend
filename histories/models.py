from datetime import datetime


class HistoryElement(object):
    def __init__(self, timestamp, name, crag, sector, country):
        self.date = datetime.fromtimestamp(timestamp).date()
        self.name = name
        self.crag = crag
        self.sector = sector
        self.country = country

    def __str__(self):
        return self.name