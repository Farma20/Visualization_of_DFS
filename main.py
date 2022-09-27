import pygame
from random import choice

# инициализация константных переменных
RES = WIDTH, HEIGHT = 802, 602
TILE = 50
cols, rows = WIDTH // TILE, HEIGHT // TILE
success = {'s': False}
print(success)


# Создание каркаса pygame
pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()


# класс клетки
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.color = 'black'

    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color('saddlebrown'), (x + 2, y + 2, TILE - 2, TILE - 2))

    def set_color_finish(self):
        self.color = 'red'

    def set_color_dfs_in(self):
        self.color = 'green'

    def set_color_dfs_out(self):
        self.color = 'black'

    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color(self.color), (x, y, TILE, TILE))

        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y), (x + TILE, y), 2)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y), (x + TILE, y + TILE), 2)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y + TILE), (x + TILE, y + TILE), 2)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y), (x, y + TILE), 2)

    def check_cell(self, x, y):
        find_index = x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index]

    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False


def dfs(now_pos, prew_pos):

    sc.fill(pygame.Color('darkslategray'))
    [cell.draw() for cell in grid_cells]
    current_cell.draw_current_cell()
    clock.tick(10)
    grid_cells[now_pos].set_color_dfs_in()
    pygame.display.flip()
    for pos in adjacency_list[now_pos]:

        if pos == finish_idx:
            success['s'] = True
            [cell.draw() for cell in grid_cells]
            current_cell.draw_current_cell()
            clock.tick(10)
            grid_cells[now_pos].set_color_dfs_in()
            pygame.display.flip()
            input()

        elif pos != prew_pos and not success['s']:
            dfs(pos, now_pos)
            grid_cells[pos].set_color_dfs_out()



def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False


grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]

# список смежности итогового графа
adjacency_list = [[] for i in range(cols * rows)]

stack = []

finish = False

while True:
    sc.fill(pygame.Color('darkslategray'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    if not finish:
        fin = choice(grid_cells)
        fin.set_color_finish()
        finish = True
        finish_idx = grid_cells.index(fin)

    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell()

    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        adjacency_list[next_cell.x + next_cell.y * cols].append(current_cell.x + current_cell.y * cols)
        adjacency_list[current_cell.x + current_cell.y * cols].append(next_cell.x + next_cell.y * cols)
        stack.append(current_cell)
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()

    if current_cell == grid_cells[0]:
        with open('text.txt', 'w') as file:
            file.write(f"{cols * rows}\n")
            file.write('0\n')
            file.write(f'{finish_idx}\n')

            # вывод списка смежности
            for adj_list in adjacency_list:
                file.write(' '.join(map(str, adj_list)))
                file.write('\n')
        break

    pygame.display.flip()
    clock.tick(90)



while True:
    sc.fill(pygame.Color('darkslategray'))

    success['s'] = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dfs(0, 0)

    [cell.draw() for cell in grid_cells]
    current_cell.draw_current_cell()

    pygame.display.flip()
    clock.tick(10)
