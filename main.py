import pygame


class Node:
    def __init__(self, value, point):
        self.value = value
        self.point = point
        self.parent = None
        self.H = 0
        self.G = 0

    def move_cost(self, other):
        return 0 if self.value == '.' else 1


def children(point, grid):
    x, y = point.point
    links = [grid[d[0]][d[1]]
             for d in [(x-1, y), (x, y - 1), (x, y + 1), (x+1, y)]]
    return [link for link in links if link.value != '%']


def manhattan(point, point2):
    return abs(point.point[0] - point2.point[0]) + abs(point.point[1]-point2.point[0])


def aStar(start, goal, grid):
    openset = set()
    closedset = set()
    current = start
    openset.add(current)
    while openset:
        # Find the item in the open set with the lowest G + H score
        current = min(openset, key=lambda o: o.G + o.H)
        # If it is the item we want, retrace the path and return it
        if current == goal:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]
        # Remove the item from the open set
        openset.remove(current)
        # Add it to the closed set
        closedset.add(current)
        # Loop through the node's children/siblings
        for node in children(current, grid):
            # If it is already in the closed set, skip it
            if node in closedset:
                continue
            # Otherwise if it is already in the open set
            if node in openset:
                # Check if we beat the G score
                new_g = current.G + current.move_cost(node)
                if node.G > new_g:
                    # If so, update the node to have a new parent
                    node.G = new_g
                    node.parent = current
            else:
                # If it isn't in the open set, calculate the G and H score for the node
                node.G = current.G + current.move_cost(node)
                node.H = manhattan(node, goal)
                # Set the parent to our current item
                node.parent = current
                # Add it to the set
                openset.add(node)
    # Throw an exception if there is no path
    raise ValueError('No Path Found')


def next_move(pacman, food, grid):
    # Convert all the points to instances of Node
    for x in xrange(len(grid)):
        for y in xrange(len(grid[x])):
            grid[x][y] = Node(grid[x][y], (x, y))
    # Get the path
    path = aStar(grid[pacman[0]][pacman[1]], grid[food[0]][food[1]], grid)
    # Output the path
    print(len(path) - 1)
    for node in path:
        x, y = node.point
        print(x, y)


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
                aStar(START, END, grid)
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
