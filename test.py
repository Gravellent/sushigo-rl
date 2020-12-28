from Player import *
from State import *
import unittest


class TestState(unittest.TestCase):

    def setUp(self):
        pass

    def test_deal(self):
        card_pool = [1, 7, 2, 7][::-1]
        self.state = State(card_pool)
        self.state.starting_hand_size = 2
        self.state.deterministic = True
        self.p1 = RandomPlayer('Player 1', playstyle='last')
        self.p2 = RandomPlayer('Player 2', playstyle='last')
        self.state.add_player(self.p1)
        self.state.add_player(self.p2)
        self.state.deal()
        assert self.p1.hand == [1,7]
        assert self.p2.hand == [2,7]

    def test_wasabi(self):
        card_pool = [1, 4, 2, 4][::-1]
        self.state = State(card_pool)
        self.state.starting_hand_size = 2
        self.state.deterministic = True
        self.p1 = RandomPlayer('Player 1', playstyle='last')
        self.p2 = RandomPlayer('Player 2', playstyle='last')
        self.state.add_player(self.p1)
        self.state.add_player(self.p2)
        self.state.refresh_state()
        self.state.play_games(1)
        assert self.p1.board[5] == 1
        assert sum(self.p1.board) == 1
        assert self.p2.board[4] == 1
        assert sum(self.p2.board) == 1

    def test_dumpling(self):
        card_pool = [6, 6, 6, 6, 6]
        self.state = State(card_pool)

        self.state.starting_hand_size = 5
        self.p1 = RandomPlayer('Player 1', playstyle='last')
        self.state.add_player(self.p1)
        self.state.play_games(1)
        assert get_score(self.p1.board) == 15

        self.state.refresh_state()
        self.state.starting_hand_size = 4
        self.state.play_games(1)
        assert get_score(self.p1.board) == 10

    def test_random_player(self):
        card_pool = [0, 1, 2]
        self.state = State(card_pool)
        self.state.starting_hand_size = 3
        self.p1 = RandomPlayer('Player 1', playstyle='random')
        self.state.add_player(self.p1)
        self.state.play_games(1)
        assert self.p1.board[0] == 1
        assert self.p1.board[1] == 1
        assert self.p1.board[2] == 1

    def test_qplayer(self):
        card_pool = [0, 1, 2]
        self.state = State(card_pool)
        self.state.starting_hand_size = 3
        self.state.refresh_state()
        self.p1 = QPlayer('Q-Player')
        self.state.add_player(self.p1)
        self.state.play_games(1)
        assert self.p1.board[0] == 1
        assert self.p1.board[1] == 1
        assert self.p1.board[2] == 1
        assert(len(self.p1.model_dict) == 4)

    def test_maki_rule(self):
        maki_count = [5, 5, 2, 1]
        score = get_maki_score(maki_count)
        assert score == [3, 3, 0, 0]

        maki_count = [5, 4, 4, 1]
        score = get_maki_score(maki_count)
        assert score == [6, 1.5, 1.5, 0]

        maki_count = [5, 5, 5, 5]
        score = get_maki_score(maki_count)
        assert score == [1.5, 1.5, 1.5, 1.5]

    def test_rule_player(self):
        card_pool = [3, 2, 1, 7]
        self.state = State(card_pool)
        self.state.starting_hand_size = 4
        self.state.refresh_state()
        self.p1 = RulePlayer("Simple Rule")
        self.state.add_player(self.p1)
        self.state.play_games(1)
        assert get_score(self.p1.board) == 6

    def test_deep_player(self):
        card_pool = [3, 2, 1, 7]
        self.state = State(card_pool)
        self.state.starting_hand_size = 4
        self.state.refresh_state()
        self.p1 = DeepPlayer("Simple Linear", memory_for_board=len(CARD_ON_BOARD))
        self.state.add_player(self.p1)
        self.state.play_games(1)
        # print(self.p1.model)
