import random
from collections import Counter
import numpy as np
import copy
import ast
from scipy.stats import rankdata


# Different in rules: Multiple Wasabi can act on a single sushi
# No tie breaker

CARD_ON_BOARD = {
    0: 'Sashimi',
    1: 'Egg Nigiri',
    2: 'Salmon Nigiri',
    3: 'Squid Nigiri',
    4: 'Wasabi Egg',
    5: 'Wasabi Salmon',
    6: 'Wasabi Squid',
    7: 'Wasabi',
    8: 'Tempura',
    9: 'Dumpling',
    10: 'Maki',
}

CARDS = {
    0: 'Sash1imi',
    1: 'Egg Nigiri',
    2: 'Salmon Nigiri',
    3: 'Squid Nigiri',
    4: 'Wasabi',
    5: 'Tempura',
    6: 'Dumpling',
    7: '1 Maki',
    8: '2 Maki',
    9: '3 Maki',
    # 10: 'Pudding',  # Not implemented
    # 11: 'Chopsticks',  # Not implemented
}


def get_score(board):
    score = 0
    score += board[0] // 3 * 10  # Salmon Nigiri
    score += board[1] * 1  # Sashimi
    score += board[2] * 2  # Squid Nigiri
    score += board[3] * 3  # Egg Nigiri
    score += board[4] * 3  # Wasabi Egg
    score += board[5] * 6  # Wasabi Salmon
    score += board[6] * 9  # Wasabi Squid
    score += board[8] // 2 * 5  # Tempura
    # Dumpling
    if board[9] == 1:
        score += 1
    if board[9] == 2:
        score += 3
    if board[9] == 3:
        score += 6
    if board[9] == 4:
        score += 10
    if board[9] > 4:
        score += ((board[9] - 4) * 5 + 10)
    return score


def add_a_card_to_board(board, card):
    if card == 0:
        board[0] += 1
    if card in [1, 2, 3]:
        if board[7] > 0:
            wasabi_cnt = board[7]
            board[7] = 0
            board[card + 3] += wasabi_cnt  # For each wasabi, add a wasabi combo (combo is always +3 index)
        else:
            board[card] += 1
    if card == 4:
        board[7] += 1
    if card == 5:
        board[8] += 1
    if card == 6:
        board[9] += 1
    if card == 7:
        board[10] += 1
    if card == 8:
        board[10] += 2
    if card == 9:
        board[10] += 3


def get_maki_score(maki_cnt_list):
    maki_rank = rankdata([_*-1 for _ in maki_cnt_list], method='min')
    maki_score = []
    first_count = np.sum(maki_rank == 1)
    second_count = np.sum(maki_rank == 2)
    for rank in maki_rank:
        if rank == 1:
            maki_score.append(6 / first_count)
        elif rank == 2:
            maki_score.append(3 / second_count)
        else:
            maki_score.append(0)
    return maki_score


def translate_board(board):
    board_list = ast.literal_eval(board)
    res = []
    for i, count in enumerate(board_list):
        res.append(f'{CARDS[i]} X {count}')
    return '  '.join(res)

def convert_hand_to_counter(hand):
    counter = Counter(hand)
    res = [0] * len(CARDS)
    for i in range(len(CARDS)):
        res[i] = counter[i]
    return res

def get_actual_card_pool():
    card_pool = []
    card_pool.extend([0] * 14)
    card_pool.extend([1] * 5)
    card_pool.extend([2] * 10)
    card_pool.extend([3] * 5)
    card_pool.extend([4] * 6)
    card_pool.extend([5] * 14)
    card_pool.extend([6] * 14)
    card_pool.extend([7] * 6)
    card_pool.extend([8] * 12)
    card_pool.extend([9] * 8)

    return card_pool