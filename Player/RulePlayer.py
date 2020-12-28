from utils import *
from Player.BasePlayer import BasePlayer


class RulePlayer(BasePlayer):

    def __init__(self, name, playstyle='simple'):
        super().__init__(name)
        self.playstyle = playstyle
        self.prepare_for_next_round()

        self.priority = [3, 0, 5, 2, 9, 6, 8, 7, 1, 4]

    def draw(self, card):
        self.hand.append(card)

    def pick_a_card(self, all_player_boards):
        for card in self.priority:  # Choose based on priority
            if card in self.hand:
                self.hand.remove(card)
                add_a_card_to_board(self.board, card)
                return

    def get_score(self):
        return get_score(self.board)

    def feed_reward(self, reward):
        return

    def prepare_for_next_round(self):
        self.hand = []
        self.board = [0] * len(CARD_ON_BOARD)
