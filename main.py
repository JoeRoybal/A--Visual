import pygame
import numpy as np


class Node:
    def __init__(self, parent=None, position=None):
        self.position = position
        self.parent = parent
        self.h = 0
        self.g = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def return_path(current_node, maze):
    path = []
    no_rows, no_columns = np.shape(maze)
    result = [[-1 for i in range(no_columns)]for j in range(no_rows)]
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    path = path[::-1]
    start_value = 0
    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1
    return result


def search(maze, cost, start, end):
    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0
    to_visit = []
    visited = []
    to_visit.append(start_node)
    outer_iterations = 0
    max_iterations = (len(maze)//2)**10
    move = [[-1, 0], [0, -1], [1, 0][0, 1]]
    no_rows, no_columns = np.shape(maze)

    while len(to_visit) > 0:
        outer_iterations += 1
        current_node = to_visit[0]
        current_index = 0
        for index, item in enumerate(to_visit):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        if outer_iterations > max_iterations:
            print("too many iterations")
            return return_path(current_node, maze)
        to_visit.pop(current_index)
        visited.append(current_node)
        if current_node == end_node:
            return return_path(current_node, maze)
        children = []
        for new_position in move:
            node_position = (
                current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if (node_position[0] > (no_rows - 1) or
                node_position[0] < 0 or
                node_position[1] > (no_columns - 1) or
                    node_position[1] < 0):
                continue

            if maze[node_position[0]][node_position[1]] != 0:
                continue
            new_node = Node(current_node, node_position)
            children.append(new_node)
        for child in children:
            if len([visited_child for visited_child in visited if visited_child == child]) > 0:
                continue

            child.g = current_node.g + cost
            child.h = (((child.position[0] - end_node.position[0]) ** 2) +
                       ((child.position[1] - end_node.position[1]) ** 2))

            child.f = child.g + child.h

            if len([i for i in to_visit if child == i and child.g > i.g]) > 0:
                continue
            to_visit.append(child)


def main():
    # INIT
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    MARGIN = 2
    grid = []
    path = []
    WIDTH = 10
    HEIGHT = 10
    count = 0
    # Creation of 2d array
    for row in range(50):
        grid.append([])
        for column in range(50):
            grid[row].append(0)

    pygame.init()
    WINDOW_SIZE = [602, 602]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Grid")
    done = False
    clock = pygame.time.Clock()
    START = []
    END = []
    Clicked = False
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN and count == 0:
                count += 1
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # Set that location to one
                grid[row][column] = 2
                START = grid[row][column]
                print("Start ", pos, "Grid coordinates: ", row, column)
            elif event.type == pygame.MOUSEBUTTONDOWN and count == 1:
                count += 1
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # Set that location to one
                grid[row][column] = 3
                END = grid[row][column]
                print("End ", pos, "Grid coordinates: ", row, column)
            # Make draggable
            elif event.type == pygame.MOUSEBUTTONDOWN and count >= 2:
                count += 1
                # User clicks the mouse. Get the position
                pos = (pygame.mouse.get_pos())
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # Set that location to one
                if grid[row][column] == 0:
                    grid[row][column] = 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                path = search(grid, 1, START, END)
                print(path)
        # Set the screen background
        screen.fill(BLACK)
        # Draw the grid
        for row in range(50):
            for column in range(50):
                color = WHITE
                if grid[row][column] == 1:
                    color = BLACK
                if grid[row][column] == 2:
                    color = GREEN
                if grid[row][column] == 3:
                    color = RED
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

        # Limit to 60 frames per second
        clock.tick(60)
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()


pygame.quit()


if __name__ == "__main__":
    main()
