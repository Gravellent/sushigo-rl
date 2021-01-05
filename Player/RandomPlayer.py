from utils import *
from Player.BasePlayer import BasePlayer


class RandomPlayer(BasePlayer):

    def __init__(self, name, playstyle='random'):
        super().__init__(name)
        self.playstyle = playstyle
        self.prepare_for_next_round()

    def draw(self, card):
        self.hand.append(card)

    def pick_a_card(self, all_player_boards):
        action = None

        if self.playstyle == 'last':  # Always draw first card
            action = self.hand.pop()
            add_a_card_to_board(self.board, action)
            return

        # Pick randomly
        if self.playstyle == 'random':
            random.shuffle(self.hand)
            action = self.hand.pop()
            add_a_card_to_board(self.board, action)
            return

    def get_score(self):
        return get_score(self.board)

    def feed_reward(self, reward):
        return
