from utils import *
from Player.BasePlayer import BasePlayer


class RulePlayer(BasePlayer):

    def __init__(self, name, playstyle='simple'):
        super().__init__(name)
        self.playstyle = playstyle
        self.prepare_for_next_round()

        self.priority = [4, 3, 2, 0, 10, 5, 9, 8, 7, 6, 1]

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

