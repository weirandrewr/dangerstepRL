import numpy as np

# Define the game size
WIDTH = 80
HEIGHT = 31

class DangerStepGame:
    def __init__(self):
        self.grid = np.random.randint(1, 10, size=(HEIGHT,WIDTH))
        self.player_position = (HEIGHT // 2, WIDTH // 2)
        self.grid[self.player_position] = 0  # Start position is marked with 0
        self.score = 0
        self.path = set([self.player_position])
        self.game_over = False

    def move(self, direction):  
        if self.game_over:
            return self.score, True

        # Define the movement vectors
        movements = {
            'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1),
            'n': (-1, -1), 'e': (-1, 1), 'w': (1, -1), 's': (1, 1)
        }
        
        dx, dy = movements.get(direction, (0, 0))
        x, y = self.player_position

        # Get the number of steps to move based on new position
        new_x, new_y = x + dx, y + dy
        if not (0 <= new_x < HEIGHT and 0 <= new_y < WIDTH):
            self.game_over = True
            return self.score, True
        steps = self.grid[new_x][new_y]

        # Move and calculate score
        move_score = 0
        for i in range(1, steps + 1):
            intermediate_x, intermediate_y = x + i * dx, y + i * dy
            if not (0 <= intermediate_x < HEIGHT and 0 <= intermediate_y < WIDTH) or (intermediate_x, intermediate_y) in self.path:
                self.game_over = True
                return self.score, True
            move_score += self.grid[intermediate_x][intermediate_y]
            self.path.add((intermediate_x, intermediate_y))
            self.grid[intermediate_x][intermediate_y] = 0  # Leave a breadcrumb

        # Update player position
        self.player_position = (x + steps * dx, y + steps * dy)
        self.score += move_score
        return self.score, False

    def reset(self):
        self.grid = np.random.randint(1, 10, size=(HEIGHT, WIDTH))
        self.player_position = (HEIGHT // 2, WIDTH // 2)
        self.grid[self.player_position] = 0
        self.score = 0
        self.path = set([self.player_position])
        self.game_over = False
        return self.grid

    def render(self):
        print(f"Score: {self.score}")
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if (i, j) == self.player_position:
                    print('X', end=' ')
                elif (i, j) in self.path:
                    print('*', end=' ')
                else:
                    print(self.grid[i, j], end=' ')
            print()
        print()