import torch
from torch import nn, optim
from utils import *
from Player import BasePlayer
import pandas as pd

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'


class DeepPlayer(BasePlayer):

    def __init__(self, name, num_of_opponents, memory_turns=0, use_chopsticks=False):
        self.name = name
        self.hand = []
        self.board = [0] * len(CARD_ON_BOARD)
        feature_size = len(CARDS) + len(CARD_ON_BOARD) * (num_of_opponents+1) + memory_turns * len(CARDS)
        self.model = LargerModel(feature_size).to(DEVICE)
        self.memory_turns = memory_turns
        self.memory = [[0] * len(CARDS) for _ in range(self.memory_turns)]
        self.use_chopsticks = use_chopsticks

        self.criterion = nn.MSELoss().to(DEVICE)
        self.optimizer = optim.SGD(self.model.parameters(), lr=0.01)
        self.decay_gamma = 0.9
        self.exp_rate = 0.3

        self.states_in_game = []

        self.prepare_for_next_round()

    def draw(self, card):
        self.hand.append(card)

    def pick_a_card(self, all_player_boards):
        action = None
        other_player_board_feature = []
        for player, board in all_player_boards:
            if player != self:
                other_player_board_feature.extend(board)
        if self.memory_turns > 0:
            model_input = self.board + convert_hand_to_counter(self.hand) + other_player_board_feature + \
                      list(pd.core.common.flatten(self.memory))
        else:
            model_input = self.board + convert_hand_to_counter(self.hand) + other_player_board_feature

        if random.random() < self.exp_rate:
            action = random.choice(self.hand)

        else:
            # Choose based on action
            action_values = self.model(torch.FloatTensor(model_input).to(DEVICE))
            action_value_rank = torch.argsort(action_values, descending=True)
            for r in action_value_rank:
                if r.item() in self.hand:
                    action = r.item()
                    break

        # Take a card based on action
        self.hand.remove(action)
        add_a_card_to_board(self.board, action)

        # Add state to memory
        # self.states_in_game.append(self.board + convert_hand_to_counter(self.hand))
        self.states_in_game.append((model_input, action))

        # Add hand to memory for model input
        if self.memory_turns > 0:
            self.memory.append(convert_hand_to_counter(self.hand))
            self.memory = self.memory[(-1 * self.memory_turns):]

    def get_score(self):
        return get_score(self.board)

    def feed_reward(self, reward):
        for state, action in self.states_in_game[::-1]:
            self.optimizer.zero_grad()
            state_tensor = torch.FloatTensor(state)
            y_pred = self.model(state_tensor)
            y_true = y_pred.detach().clone()
            y_true[action] = reward
            loss = self.criterion(y_pred, y_true)
            loss.backward()
            self.optimizer.step()
            reward *= self.decay_gamma

    def prepare_for_next_round(self):
        super().prepare_for_next_round()
        self.states_in_game = []
        self.memory = [[0]*len(CARDS) for _ in range(self.memory_turns)]


class Model(torch.nn.Module):

    def __init__(self, feature_size):
        super(Model, self).__init__()
        self.linear1 = torch.nn.Linear(feature_size, 128)
        self.linear2 = torch.nn.Linear(128, 32)
        self.linear3 = torch.nn.Linear(32, 16)
        self.linear4 = torch.nn.Linear(16, len(CARDS))
        self.relu = nn.ReLU()

    def forward(self, x):
        out = x
        out = self.linear1(out)
        out = self.relu(out)
        out = self.linear2(out)
        out = self.relu(out)
        out = self.linear3(out)
        out = self.relu(out)
        out = self.linear4(out)
        return out


class LargerModel(torch.nn.Module):

    def __init__(self, feature_size):
        super(LargerModel, self).__init__()
        self.linear1 = torch.nn.Linear(feature_size, 256)
        self.linear2 = torch.nn.Linear(256, 128)
        self.linear3 = torch.nn.Linear(128, 128)
        self.linear4 = torch.nn.Linear(128, 64)
        self.linear5 = torch.nn.Linear(64, len(CARDS))
        self.relu = nn.ReLU()

    def forward(self, x):
        out = x
        out = self.linear1(out)
        out = self.relu(out)
        out = self.linear2(out)
        out = self.relu(out)
        out = self.linear3(out)
        out = self.relu(out)
        out = self.linear4(out)
        out = self.relu(out)
        out = self.linear5(out)
        return out