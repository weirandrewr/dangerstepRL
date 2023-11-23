#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>

const int WIDTH = 80;
const int HEIGHT = 31;

struct Position {
    int x, y;
};

std::vector<std::vector<int>> initialize_grid() {
    std::vector<std::vector<int>> grid(HEIGHT, std::vector<int>(WIDTH));
    std::srand(static_cast<unsigned int>(std::time(nullptr)));  // Seed for random number generation
    for (auto &row : grid) {
        for (auto &cell : row) {
            cell = std::rand() % 9 + 1;  // Random number from 1 to 9
        }
    }
    return grid;
}

Position get_move_vector(char direction) {
    switch (direction) {
        case 'u': return {-1, 0};
        case 'd': return {1, 0};
        case 'l': return {0, -1};
        case 'r': return {0, 1};
        case 'n': return {-1, -1};
        case 'e': return {-1, 1};
        case 'w': return {1, -1};
        case 's': return {1, 1};
        default: return {0, 0};
    }
}

bool is_valid_position(const Position &pos) {
    return pos.x >= 0 && pos.x < HEIGHT && pos.y >= 0 && pos.y < WIDTH;
}

void print_grid(const std::vector<std::vector<int>> &grid, const std::vector<std::vector<bool>> &path, const Position &player_pos) {
    for (int i = 0; i < HEIGHT; ++i) {
        for (int j = 0; j < WIDTH; ++j) {
            if (i == player_pos.x && j == player_pos.y) {
                std::cout << 'X';
            } else if (path[i][j]) {
                std::cout << '*';
            } else {
                std::cout << grid[i][j];
            }
        }
        std::cout << std::endl;
    }
}

int main() {
    std::vector<std::vector<int>> grid = initialize_grid();
    std::vector<std::vector<bool>> path(HEIGHT, std::vector<bool>(WIDTH, false));
    Position player_pos = {HEIGHT / 2, WIDTH / 2};
    path[player_pos.x][player_pos.y] = true;  // Starting position
    int score = 0;

    print_grid(grid, path, player_pos);
    std::cout << "Score: " << score << "\nMove (u, d, l, r, n, e, s, w): ";

    char command;
    while (std::cin >> command) {
        Position move_vector = get_move_vector(command);
        Position new_pos = {player_pos.x + move_vector.x, player_pos.y + move_vector.y};

        if (!is_valid_position(new_pos)) {
            std::cout << "Invalid move!" << std::endl;
            continue;
        }

        int steps = grid[new_pos.x][new_pos.y];
        int move_score = 0;
        for (int i = 1; i <= steps; ++i) {
            int intermediate_x = player_pos.x + move_vector.x * i;
            int intermediate_y = player_pos.y + move_vector.y * i;
            Position intermediate_pos = {intermediate_x, intermediate_y};

            if (!is_valid_position(intermediate_pos) || path[intermediate_x][intermediate_y]) {
                std::cout << "Game over! Final score: " << score << std::endl;
                return 0;
            }

            move_score += grid[intermediate_x][intermediate_y];
            path[intermediate_x][intermediate_y] = true;
        }

        player_pos = {player_pos.x + move_vector.x * steps, player_pos.y + move_vector.y * steps};
        score += move_score;
        print_grid(grid, path, player_pos);
        std::cout << "Score: " << score << "\nMove (u, d, l, r, n, e, s, w): ";
    }

    return 0;
}