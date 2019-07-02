import gym
import enum
import numpy as np

from gym import spaces

HEIGHT = 6
WIDTH = 7

class Connect4Env(gym.Env):
    metadata = {'render.modes': ['human', 'bot']}

    def __init__(self):
        self._reset()
        self.player = Player.P1.value
        #self.opponent = Player.P2

    def _step(self, action):
        #### RANDOM CHOIE MOVE
        last_played = self.perform_move(action, Player.P2.value)
        self.update_legal_moves(last_played)
        # TODO: get the random bot's column choice self.done, reward = check_win_condition(last_played
        ######### End of turn
        #self.done, tie = self.check_win_condition()
        #if self.done:
         #   return self.state, reward, self.done, {'state': self.state}
        #AI MOVE
        last_played = self.perform_move(action, Player.P1.value)
        self.update_legal_moves(last_played)
        self.done, reward = check_win_condition(last_played, action, Player.P1.value)
        return self.state, 0, self.done, {'state': self.state}

    def _seed(self, seed=None):
        return

    def _reset(self):
        self.board = np.zeros(HEIGHT * WIDTH).reshape(HEIGHT, WIDTH)
        self.state = {'board': self.board}
        self.done = False
        self.current_player = Player.P1.value
        self.action_space = spaces.Discrete(WIDTH)

    def _render(self, mode='human', close=False):
        print(self.board)
        print("")

    def perform_move(self, action, player_num):
        """ Assumes that the move is legal """
        chosen_col = self.board[:, action]
        for i in range(len(chosen_col)):
            if int(chosen_col[6 - i - 1]) == 0:
                chosen_col[6 - i - 1] = player_num
                break

    def choose_legal_move(self):
        pass

    def check_win_condition(self, last_played, action, player_val):
        tie = False
        done = False
        filled = False
        count = 1
        if Locations.Empty not in self.board:
            filled = True
        if self.board[last_played - 1][action - 1] == player_val or self.board[last_played + 1][action + 1] == player_val:
            done = self.check_d1(last_played, action, player_val)
        if self.board[last_played - 1][action + 1] == player_val or self.board[last_played + 1][action - 1] == player_val:
            done = done or self.check_d2(last_played, action, player_val)
        if self.board[last_played][action - 1] == player_val or self.board[last_played][action + 1] == player_val:
            done = done or self.check_horizontal(last_played, player_val)
        if self.board[last_played + 1][action] == player_val:
            done = done or self.check_vertical(action, player_val)

        if filled and not done:
            # TIE = 0 reward
            return True, 0
        if done:
            # Game won by player = 1 reward; won by opponent = -1
            return True, (1 * player_val)
        else:
            # Game not done = 0 reward
            return False, 0

    def check_d1(row, col, player_val):
        start_r = row - min(row, col)
        start_c = col - min(row, col)
        count = 0
        while start_r < HEIGHT and start_c < WIDTH:
            if board[start_r, start_c] == player_val:
                count = count + 1
                if count == 4:
                    return True
            else:
                count = 0
            start_r = start_r + 1
            start_c = start_c + 1
        return False

    def check_d2(row, col, player_val):
        start_r = row + min(HEIGHT - row, col)
        start_c = col - min(HEIGHT - row, col)
        count = 0
        while start_r >= 0 and start_c < WIDTH:
            if board[start_r, start_c] == player_val:
                count = count + 1
                if count == 4:
                    return True
            else:
                count = 0
            start_r = start_r - 1
            start_c = start_c + 1
        return False
    
    def check_horizontal(row, player_val):
        count = 0
        r = self.board[row,:]
        for i in range(4):
            if r[i] == r[i + 1] == r[i + 2] == r[i + 3] == player_val:
                return True
        return False

    def check_vertical(column, player_val):
        col = self.board[:,column]
        for i in range(3):
            if col[i] == col[i + 1] == col[i + 2] == col[i + 3] == player_val:
                return True
        return False
    
    def update_legal_moves(self):
        temp = self.board.reshape(6,7)
        for i in self.action_space:
            if not np.any(temp[:,i] == 0):
                self.action_space.remove(i)

class Player(enum.Enum):
    P1 = 1
    P2 = -1
    Empty = 0


class Actions(enum.Enum):
    Col1 = 0
    Col2 = 1
    Col3 = 2
    Col4 = 3
    Col5 = 4
    Col6 = 5
    Col7 = 6

