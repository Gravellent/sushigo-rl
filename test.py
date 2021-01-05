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
        self.p1 = DeepPlayer("Simple Linear", num_of_opponents=0)
        self.state.add_player(self.p1)
        self.state.play_games(1)
        # print(self.p1.model)

    def test_multiple_games(self):
        card_pool = [0] * 10
        self.state = State(card_pool)
        self.state.starting_hand_size = 3
        self.state.refresh_state()
        self.p1 = RandomPlayer("Random")
        self.state.add_player(self.p1)
        self.state.play_games(num_of_games=1, output_result=False, round_per_game=3)

    def test_pudding(self):
        card_pool = [10] * 10
        self.state = State(card_pool)
        self.state.starting_hand_size = 3
        self.state.refresh_state()
        self.p1 = DeepPlayer("Random", num_of_opponents=0)
        self.state.add_player(self.p1)
        self.state.play_games(num_of_games=1, output_result=False, round_per_game=3)
        assert self.p1.board[11] == 9

    def test_pudding_scoring(self):
        pudding_cnt = [5, 5, 1]
        score = get_pudding_score(pudding_cnt)
        assert score == [3, 3, -6]

        pudding_cnt = [5, 5, 5, 5]
        score = get_pudding_score(pudding_cnt)
        assert score == [1.5, 1.5, 1.5, 1.5]

    def test_normal_game(self):
        card_pool = get_actual_card_pool()
        self.state = State(card_pool)
        self.state.starting_hand_size = 8
        self.state.refresh_state()
        self.p1 = RandomPlayer("Random")
        self.p2 = DeepPlayer("Deep", num_of_opponents=1, memory_turns=1)
        self.state.add_player(self.p1)
        self.state.add_player(self.p2)
        self.state.play_games(num_of_games=1, output_result=False, round_per_game=3)


    def test_four_player(self):
        state = State(get_actual_card_pool())
        p1 = DeepPlayer('Deep Learning', num_of_opponents=3)
        p2 = QPlayer('Q Learning')
        p3 = RulePlayer('Rule Based')
        p4 = DeepPlayer('Deep w/ Memory', num_of_opponents=3, memory_turns=3)
        state.add_player(p1)
        state.add_player(p2)
        state.add_player(p3)
        state.add_player(p4)
        state.starting_hand_size = 8
        df = pd.DataFrame()
        all_results = []
        hit_rates = []

        for i in range(5):
            # Train
            p1.exp_rate = 0.3
            p2.exp_rate = 0.3
            state.play_games(200, round_per_game=3)

            # Eval
            p1.exp_rate = 0
            p2.exp_rate = 0
            state.stats = []
            state.play_games(200, round_per_game=3)
            all_results.append(state.stats)