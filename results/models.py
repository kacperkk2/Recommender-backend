
class RecommendationElement(object):
    def __init__(self, rank, name, crag, sector, country):
        self.rank = rank
        self.name = name
        self.crag = crag
        self.sector = sector
        self.country = country

    def __str__(self):
        return self.name