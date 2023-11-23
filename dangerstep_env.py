import gymnasium as gym
from gymnasium import spaces
import numpy as np
from dangerstep import DangerStepGame
from stable_baselines3.common.env_checker import check_env

class DangerStepEnv(gym.Env):

    def __init__(self):
        super(DangerStepEnv, self).__init__()
        self.action_space = spaces.Discrete(8)  # 8 possible moves
        self.observation_space = spaces.Box(low=0, high=9, shape=(31, 80), dtype=np.int32)
        self.game = DangerStepGame()  # Initialize the game
        self.state = self.game.grid
        self.score = 0
        self.exploration_bonus = 0.1  # Adjust as needed
        self.done = False
    
    def step(self, action):
        action_map = {0: 'n', 1: 'e', 2: 's', 3: 'w', 4: 'u', 5: 'r', 6: 'd', 7: 'l'}
        direction = action_map.get(action)
        reward, done = self._take_action(direction)
        self.done = done
        
        info = {}
        return self.state, reward, done, False ,info

    def _take_action(self, direction):
        reward = 0
        move_bonus = 2
        end_game_penalty = -20
        same_direction_penalty = -10  # Penalty for going in the same direction more than 3 times
        max_same_direction = 3
        reward = move_bonus

        if not hasattr(self, 'last_moves'):
            self.last_moves = []
        self.last_moves.append(direction)
        if len(self.last_moves) > max_same_direction:
            self.last_moves.pop(0)  # Remove the oldest move
        if all(move == direction for move in self.last_moves):
            reward += same_direction_penalty  # Apply the penalty

         # Get the current position of the player before moving
        current_x, current_y = self.game.player_position
        #print(f"{current_x}, {current_y}")

        # Perform the move
        self.game.move(direction)
        reward += move_bonus
        
        # Get the new position of the player after moving
        new_x, new_y = self.game.player_position

        # Calculate the move
        move_x, move_y = new_x - current_x, new_y - current_y

        # Print diagnostic information
        #print(f"Action: {direction}, Move: ({move_x}, {move_y}), New Position: ({new_x}, {new_y})")

        if self.game.game_over:
            reward += end_game_penalty
            #print('haha game over')
        else:
           # print (self.score)
            self.last_moves.clear()

        self.score = self.game.score
        self.state = self.game.grid
        return reward, self.game.game_over

    def reset(self,seed=None):
        self.state = self.game.reset()  # Reset the game state
        self.score = 0
        self.done = False
        info = {}
        return self.state,info


    def render(self, mode='human', close=False):
        # Rendering logic (if needed)
        pass

    def seed(self, seed=None):
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]
    
if __name__ == "__main__":
    env = DangerStepEnv()
    check_env(env)
