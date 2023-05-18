import pygame
import random

# Maze dimensions
WIDTH = 25
HEIGHT = 20
CELL_SIZE = 50
WINDOW_SIZE = (WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}

    def draw(self, screen):
        x, y = self.x * CELL_SIZE, self.y * CELL_SIZE
        if self.visited:
            pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))

        if self.walls['top']:
            pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y))
        if self.walls['right']:
            pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE))
        if self.walls['bottom']:
            pygame.draw.line(screen, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE))
        if self.walls['left']:
            pygame.draw.line(screen, BLACK, (x, y), (x, y + CELL_SIZE))

def generate_maze(width, height):
    stack = []
    maze = [[Cell(x, y) for y in range(height)] for x in range(width)]
    current = maze[0][0]
    current.visited = True
    stack.append(current)

    while stack:
        neighbors = []
        x, y = current.x, current.y

        if x > 0 and not maze[x - 1][y].visited:
            neighbors.append(('left', maze[x - 1][y]))
        if x < width - 1 and not maze[x + 1][y].visited:
            neighbors.append(('right', maze[x + 1][y]))
        if y > 0 and not maze[x][y - 1].visited:
            neighbors.append(('top', maze[x][y - 1]))
        if y < height - 1 and not maze[x][y + 1].visited:
            neighbors.append(('bottom', maze[x][y + 1]))

        if neighbors:
            direction, next_cell = random.choice(neighbors)
            current.walls[direction] = False
            next_cell.walls[{'left': 'right', 'right': 'left', 'top': 'bottom', 'bottom': 'top'}[direction]] = False
            next_cell.visited = True
            stack.append(next_cell)
            current = next_cell
        else:
            current = stack.pop()

    return maze

def solve_maze(maze, start, end):
    stack = [(start, [])]
    visited = set()

    while stack:
        current, path = stack.pop()
        if current == end:
            return path + [current]

        visited.add(current)
        x, y = current.x, current.y

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                neighbor = maze[nx][ny]
                if neighbor not in visited and not current.walls[{'-1,0': 'left', '1,0': 'right', '0,-1': 'top', '0,1': 'bottom'}[f'{dx},{dy}']]:
                    stack.append((neighbor, path + [current]))

def draw_solution(screen, solution):
    for cell in solution:
        x, y = cell.x * CELL_SIZE, cell.y * CELL_SIZE
        pygame.draw.rect(screen, GREEN, (x + CELL_SIZE // 4, y + CELL_SIZE // 4, CELL_SIZE // 2, CELL_SIZE // 2))

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Maze Generator and Solver')
    clock = pygame.time.Clock()

    maze = generate_maze(WIDTH, HEIGHT)
    solution = solve_maze(maze, maze[0][0], maze[WIDTH - 1][HEIGHT - 1])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        for row in maze:
            for cell in row:
                cell.draw(screen)

        draw_solution(screen, solution)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
