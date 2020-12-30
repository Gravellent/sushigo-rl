from utils import *


class State:

    def __init__(self, card_pool):
        self.original_card_pool = card_pool
        self.card_pool = copy.copy(self.original_card_pool)
        self.players = []
        self.starting_hand_size = 10
        self.scoreboard = []
        self.deterministic = False

    def add_player(self, player):
        self.players.append(player)

    def deal(self):
        for p in self.players:
            p.prepare_for_next_round()
            for _ in range(self.starting_hand_size):
                if not self.deterministic:
                    random.shuffle(self.card_pool)
                p.draw(self.card_pool.pop())

    def play(self, num_of_rounds=1, output_result=False):
        self.scoreboard = [0] * len(self.players)
        for r in range(num_of_rounds):
            # Clean up board
            for p in self.players:
                p.board = []

            self.deal()
            # print(self.players[0].hand, self.players[1].hand)
            for turn in range(self.starting_hand_size): # Round num is same as starting hand sizer
                all_player_boards = []  # A list of (player class, player board), to check if it's the player's board
                for p in self.players:
                    all_player_boards.append((p, p.board))
                for p in self.players:
                    p.pick_a_card(all_player_boards)
                self.pass_around()
            for i, p in enumerate(self.players):
                self.scoreboard[i] += p.get_score()

            # Adjustment for Maki
            maki_score = get_maki_score([_.board[10] for _ in self.players])
            for i in range(len(maki_score)):
                self.scoreboard[i] += maki_score[i]

        max_score = max(self.scoreboard)
        if output_result:
            for i, p in enumerate(self.players):
                print("Player", i)
                for i in range(len(p.board)):
                    print(f"{CARD_ON_BOARD[i]} X {p.board[i]}")
            print(self.scoreboard, max_score)
        for i, p in enumerate(self.players):
            if self.scoreboard[i] == max_score:
                self.stats[i] += 1
                p.feed_reward(max(1, len(self.players) - 1))
            else:
                p.feed_reward(-1)

    def play_games(self, num_of_games=1, round_per_game=1, output_result=False):
        self.stats = [0] * len(self.players)
        for i in range(num_of_games):
            self.refresh_state()
            self.play(output_result=output_result, num_of_rounds=round_per_game)
        # print(self.stats)

    def pass_around(self):
        tmp = self.players[-1].hand
        for i in range(len(self.players) - 1, 0, -1):
            self.players[i].hand = self.players[i-1].hand  # Pass to next player
        self.players[0].hand = tmp  # First player get the last player's hand


    def refresh_state(self):
        self.scoreboard = []
        self.card_pool = copy.copy(self.original_card_pool)

from Player import *
if __name__ == '__main__':
    card_pool = []
    card_pool.extend([0] * 0)
    card_pool.extend([1] * 10)
    card_pool.extend([2] * 10)
    card_pool.extend([3] * 10)
    card_pool.extend([7] * 30)  # Wasabi
    card_pool.extend([8] * 0)  # Tempura

    state = State(card_pool)
    p1 = BasePlayer('Player 1', playstyle='random')
    p2 = BasePlayer('Player 2', playstyle='random')
    state.add_player(p1)
    state.add_player(p2)
    state.play_games(1)