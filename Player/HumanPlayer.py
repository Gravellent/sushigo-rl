from utils import *
from Player.BasePlayer import BasePlayer

class HumanPlayer(BasePlayer):

    def __init__(self, name):
        super().__init__(name)
        self.prepare_for_next_round()

    def draw(self, card):
        self.hand.append(card)

    def pick_a_card(self, all_player_boards):
        action = None
        print("Board:")
        for i in range(len(self.board)):
            print(f"{CARD_ON_BOARD[i]} X {self.board[i]}")
        print('-' * 50)
        for card in self.hand:
            print(f"{card}, {CARDS[card]}")
        print('-' * 50)
        while True:
            action = int(input("Please choose a card"))
            if action in self.hand:
                break
            else:
                print("Invalid choice!")
        self.hand.remove(action)
        add_a_card_to_board(self.board, action)

    def get_score(self):
        return get_score(self.board)

    def feed_reward(self, reward):
        return
