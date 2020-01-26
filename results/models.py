
class RecommendationElement(object):
    def __init__(self, rank, name, crag, sector, country, grade):
        self.rank = rank
        self.name = name
        self.crag = crag
        self.sector = sector
        self.country = country
        self.grade = grade

    def __str__(self):
        return self.name