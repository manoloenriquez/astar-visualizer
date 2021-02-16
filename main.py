import pygame
from node import Node
from style import Color

# Pygame Initialization
pygame.init()
WIDTH, HEIGHT = 640, 640
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('A* Visualizer')

# Constants
n = 16
size = WIDTH // n
delay = 15

positions = []
    
# A* Algorithm
open = []
closed = []
walls = []
path = []
start = None
end = None

def search():
    open.append(start)
    while len(open) > 0:
        visualizer()
        pygame.display.update()
        pygame.time.wait(delay)

        curr_node = get_lowest_fcost()
        open.remove(curr_node)
        
        # Reached Goal
        if curr_node == end:
            while curr_node is not None:
                path.append(curr_node)
                curr_node = curr_node.parent

            return

        closed.append(curr_node)
        adjacent = get_adjacent_nodes(curr_node, n)

        for node in adjacent:
            if node is None or node in closed:
                continue
            
            node.compute_gcost(start)
            node.compute_hcost(end)
            node.compute_fcost()

            if node in open:
                temp = None
                for i in open:
                    if i == node:
                        temp = i

                if node.g < temp.g:
                    open.remove(temp)
                    open.append(node)

            if node not in open:
                open.append(node)

def get_lowest_fcost() -> Node:
    node = None
    for i in range(len(open)):
        open[i].compute_gcost(start)
        open[i].compute_hcost(end)
        open[i].compute_fcost()
        
        if i == 0 or node.f > open[i].f:
            node = open[i]

    return node

def valid_diagonal(node):
    up = None
    right = None
    down = None
    left = None

    if node.y - 1 >= 0:
        up = Node(node.x, node.y - 1 , node)
        if up in walls:
            return False
    
    if node.x + 1 < n:
        right = Node(node.x + 1, node.y, node)
        if right in walls:
            return False

    if node.y + 1 < n:
        down = Node(node.x, node.y + 1, node)
        if down in walls:
            return False

    if node.x - 1 >= 0:
        left = Node(node.x - 1, node.y, node)
        if left in walls:
            return False

    return True

def get_adjacent_nodes(node, n) -> list:
    up = None
    right = None
    down = None
    left = None
    top_left = None
    top_right = None
    bottom_right = None
    bottom_left = None

    if node.y - 1 >= 0:
        up = Node(node.x, node.y - 1 , node)
        if up in walls:
            up = None
    
    if node.x + 1 < n:
        right = Node(node.x + 1, node.y, node)
        if right in walls:
            right = None

    if node.y + 1 < n:
        down = Node(node.x, node.y + 1, node)
        if down in walls:
            down = None

    if node.x - 1 >= 0:
        left = Node(node.x - 1, node.y, node)
        if left in walls:
            left = None

    if node.x - 1 >= 0 and node.y - 1 >= 0:
        top_left = Node(node.x - 1, node.y - 1, node)
        if top_left in walls or not valid_diagonal(top_left):
            top_left = None

    if node.x + 1 < n and node.y - 1 >= 0:
        top_right = Node(node.x + 1, node.y - 1, node)
        if top_right in walls or not valid_diagonal(top_right):
            top_right = None

    if node.x + 1 < n and node.y + 1 < n:
        bottom_right = Node(node.x + 1, node.y + 1, node)
        if bottom_right in walls or not valid_diagonal(bottom_right):
            bottom_right = None

    if node.x - 1 >= 0 and node.y + 1 < n:
        bottom_left = Node(node.x - 1, node.y + 1, node)
        if bottom_left in walls or not valid_diagonal(bottom_left):
            bottom_left = None

    return [ up, right, down, left, top_left, top_right, bottom_right, bottom_left ]

# GUI
def draw_grid():
    for row in range(n):
        for col in range(n):
            rect = pygame.Rect(row * size, col * size, size, size)
            pygame.draw.rect(WIN, Color.GRAY, rect, 1)

def add_pos(x, y, key_pressed):
    global start
    global end
    node = Node(x, y, None, key_pressed)
    positions.append(node)

    if start is not None:
        if key_pressed == 's':
            temp = start
            positions.remove(temp)

    if end is not None:
        if key_pressed == 'e':
            temp = end
            positions.remove(temp)

    if node.wall:
        walls.append(node)
    elif node.start:
        start = node
    elif node.end:
        end = node

    

def remove_pos(x, y):
    node = Node(x, y)
    if node in positions:
        positions.remove(node)
    if node in walls:
        walls.remove(node)

def draw_positions():
    for pos in positions:
        x, y = pos.x, pos.y
        rect = pygame.Rect(x * size + 1, y * size + 1, size - 1, size - 1)
        
        if pos.wall:
            pygame.draw.rect(WIN, Color.BLACK, rect, 0)
        
        if pos.start:
            pygame.draw.rect(WIN, Color.BLUE, rect, 0)

        if pos.end:
            pygame.draw.rect(WIN, Color.RED, rect, 0)

def visualizer():
    if open is not None:
        for pos in open:
            if pos == start or pos == end:
                continue

            x, y = pos.x, pos.y
            rect = pygame.Rect(x * size + 1, y * size + 1, size - 1, size - 1)

            pygame.draw.rect(WIN, Color.OPEN, rect, 0)
    
    if closed is not None:
        for pos in closed:
            if pos == start or pos == end:
                continue

            x, y = pos.x, pos.y
            rect = pygame.Rect(x * size + 1, y * size + 1, size - 1, size - 1)

            pygame.draw.rect(WIN, Color.CLOSED, rect, 0)
    
    if path is not None:
        for pos in path:
            if pos == start or pos == end:
                continue

            x, y = pos.x, pos.y
            rect = pygame.Rect(x * size + 1, y * size + 1, size - 1, size - 1)

            pygame.draw.rect(WIN, Color.PATH, rect, 0)

def reset():
    global open
    global closed
    global walls
    global path
    global start
    global end
    global positions
    
    open = []
    closed = []
    walls = []
    path = []
    start = None
    end = None
    positions = []

# Main
def main():
    run = True
    key_pressed = ''
    drag = False
    click = -1
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                drag = True
                pos = pygame.mouse.get_pos()
                x = int(pos[0] // size)
                y = int(pos[1] // size)

                click = event.button
                if click == 1:
                    add_pos(x, y, key_pressed)
                elif click == 3:
                    remove_pos(x, y)
            if event.type == pygame.MOUSEBUTTONUP:
                drag = False
            if event.type == pygame.MOUSEMOTION:
                if drag:
                    pos = pygame.mouse.get_pos()
                    x = int(pos[0] // size)
                    y = int(pos[1] // size)

                    if click == 1:
                        add_pos(x, y, key_pressed)
                    elif click == 3:
                        remove_pos(x, y)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    key_pressed = 's'
                if event.key == pygame.K_e:
                    key_pressed = 'e'
                if event.key == pygame.K_SPACE:
                    if start is not None and end is not None:
                        search()
                if event.key == pygame.K_BACKSPACE:
                    reset()

            if event.type == pygame.KEYUP:
                key_pressed = ''

        WIN.fill(Color.WHITE)
        draw_grid()
        draw_positions()
        if path is not None:
            visualizer()
        pygame.display.update() # update game window
    
    pygame.quit()

if __name__ == '__main__':
    main()