import pygame


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
                print("Start ", pos, "Grid coordinates: ", row, column)
            elif event.type == pygame.MOUSEBUTTONDOWN and count == 1:
                count += 1
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # Set that location to one
                grid[row][column] = 2
                path = grid
                print("End ", pos, "Grid coordinates: ", row, column)
            elif event.type == pygame.MOUSEBUTTONDOWN and count >= 2:
                count += 1
                # User clicks the mouse. Get the position
                pos = (pygame.mouse.get_pos())
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # Set that location to one
                grid[row][column] = 1

        # Set the screen background
        screen.fill(BLACK)

        # Draw the grid
        for row in range(50):
            for column in range(50):
                color = WHITE
                if grid[row][column] == 1:
                    color = BLACK
                if grid[row][column] == 2:
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
