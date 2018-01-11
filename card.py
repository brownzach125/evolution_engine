
class Card(object):
    def __init__(self, type, food_value):
        self.type = type
        self.food_value = food_value


class Deck(object):
    def __init__(self):
        self.cards = [Card("A", i) for i in range(0, 52)]

    @property
    def cards_left(self):
        return len(self.cards)

    def draw(self, number):
        cards = self.cards[:number]
        self.cards = self.cards[number:]
        return cards