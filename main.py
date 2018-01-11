import random
from enum import Enum
from species import SpeciesArea
from card import Deck

from action import *

class Player(object):
    def __init__(self, name):
        self._name = name
        self.species_area = None
        self.hand = []

    @property
    def name(self):
        return self._name

    def select_action(self, actions):
        for i, action in enumerate(actions):
            print(str(i) + ": " + str(action))
        choice = int(input(self.name + " choose your action\n>"))
        return actions[choice]


class State(object):
    def __init__(self):
        self.first_player = None
        self.phase = None
        self.players_left_to_go = None
        self.players = None
        self.oasis_staging = []

PhaseName = Enum('PhaseName','setup deal_cards select_food play_cards reveal_food feeding cleanup final_cleanup end')


class Phase(object):
    next_phase = PhaseName.end

    @classmethod
    def setup(cls, state):
        return state

    @classmethod
    def player_main(cls, player, state):
        chosen_action = None
        while(type(chosen_action) != EndAction):
            actions = cls.get_actions(player, state)
            chosen_action = player.select_action(actions)
            if not chosen_action:
                raise Exception("Invalide choice")
            state = chosen_action.apply(state)

        return state


    @classmethod
    def get_actions(cls, player, state):
        return [EndAction()]

    @classmethod
    def cleanup(cls, state):
        return state

    @classmethod
    def get_next_phase(cls):
        return cls.next_phase


class SetupPhase(Phase):
    next_phase = PhaseName.deal_cards

    @classmethod
    def setup(cls, state):
        state.deck = Deck()
        players = state.players
        for player in list(players.values()):
            player.species_area = SpeciesArea()
            # Every player starts with a single specie
            player.species_area.add_specie_left()
        return state


class DealCardsPhase(Phase):
    next_phase = PhaseName.select_food

    @classmethod
    def setup(cls, state):
        players = state.players
        for player in list(players.values()):
            player.hand += state.deck.draw(3 + player.species_area.count)

        return state


class SelectFoodPhase(Phase):
    next_phase = PhaseName.play_cards

    @classmethod
    def setup(cls, state):
        state.oasis_staging = []
        return state

    @classmethod
    def player_main(cls, player, state):
        actions = cls.get_actions(player, state)
        chosen_action = player.select_action(actions)
        state = chosen_action.apply(state)
        return state

    @classmethod
    def get_actions(cls, player, state):
        actions = []
        for i, card in enumerate(player.hand):
            actions.append(SelectFoodAction(player, i, card))

        return actions

class PlayCardsPhase(Phase):
    next_phase = PhaseName.end

    @classmethod
    def get_actions(cls, player, state):
        # All specie creation actions
        actions = []
        for i, card in enumerate(player.hand):
            actions.append(CreateSpecieAction(player, i, True))
            actions.append(CreateSpecieAction(player, i, False))

        # Increase specie body size or population
        for specie in player.species_area:
            for i, card in enumerate(player.hand):
                actions.append(IncreaseBodySizeAction(player, i, specie))
                actions.append(IncreasePopulationAction(player, i, specie))

        actions.append(EndAction())
        return actions



class FinalCleanupPhase(Phase):
    next_phase = PhaseName.end


class EndPhase(Phase):
    pass


phases = {
    PhaseName.setup: SetupPhase,
    PhaseName.deal_cards: DealCardsPhase,
    PhaseName.select_food: SelectFoodPhase,
    PhaseName.play_cards: PlayCardsPhase,
    PhaseName.final_cleanup: FinalCleanupPhase,
    PhaseName.end: EndPhase
}


class Game(object):
    class TurnOrder(object):
        def __init__(self, players, first_player):
            players = list(players.values())
            for i, player in enumerate(players):
               if player == first_player:
                   break
            self.order = players[i:] + players[:i]

        def next(self):
            player = self.order[0]
            self.order = self.order[1:]
            return player

        def players_left(self):
            return self.order

        def done(self):
            if len(self.order):
                return False
            return True

    def __init__(self):
        self.players = {}
        self.state = State()

    def add_player(self, player):
        name = player.name
        if name in self.players:
            raise Exception("Player with that name already exists")
        self.players[name] = player

    def start(self):
        print("Starting the game")
        self.state.first_player = random.choice(list(self.players.values()))
        print("First player is " + self.state.first_player.name)
        self.state.phase = SetupPhase

        self.state.players = self.players


    def turn(self, player):
        print("It is player " + player.name + "'s turn.")
        print(self.state)


    def run(self):
        print("Running the game")
        # Keep cycling through phases until we hit the end phase
        while(self.state.phase != EndPhase):
            phase = self.state.phase
            self.state = phase.setup(self.state)
            self.state.turn_order = Game.TurnOrder(self.players, self.state.first_player)

            # Cycle through the players
            while(not self.state.turn_order.done()):
                player = self.state.turn_order.next()
                self.state = phase.player_main(player, self.state)

            self.state = phase.cleanup(self.state)
            self.state.phase = phases[phase.get_next_phase()]

        print(self.state)

if __name__ == "__main__":
    game = Game()

    player = Player("Zach")
    game.add_player(player)
    player = Player("Kade")
    #game.add_player(player)
    player = Player("Charlie")
    #game.add_player(player)


    game.start()
    game.run()

