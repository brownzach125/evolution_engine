class Action(object):
    def __init__(self):
        pass

    def apply(self, state):
        return state

    def __str__(self):
        return "end"


class EndAction(Action):
    def __str__(self):
        return "end"


class SelectFoodAction(Action):
    def __init__(self, player, card_index, card):
        self.player = player
        self.card_index = card_index
        self.card = card

    def apply(self, state):
        state.oasis_staging.append(self.card)
        self.player.hand.pop(self.card_index)
        return state

    def __str__(self):
        return "SelectFood card {0} {1} food value {2}".format(self.card_index, self.card.type, self.card.food_value)


class CreateSpecieAction(Action):
    def __init__(self, player, card_index, left):
        self.player = player
        self.card_index = card_index
        self.left = left

    def apply(self, state):
        self.player.hand.pop(self.card_index)
        if self.left:
            self.player.species_area.add_specie_left()
        else:
            self.player.species_area.add_specie_right()

    def __str__(self):
        return "CreateSpecie card {0} Left: {1}".format(self.card_index, self.left)


class IncreaseBodySizeAction(Action):
    pass


class IncreasePopulationAction(Action):
    pass
