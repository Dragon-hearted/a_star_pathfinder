import pygame
import math
from queue import PriorityQueue

# Setup window
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinder Algorithm")

# Color palette
RED = (255, 0, 0)  # Node has been considered (closed)
GREEN = (0, 255, 0)  # Node is open for consideration
WHITE = (255, 255, 255)  # Default/untouched node
BLACK = (0, 0, 0)  # Barrier node, cannot be used
PURPLE = (128, 0, 128)  # Node is part of the final path
PINK = (255, 0, 255)  # Start node
BLUE = (0, 0, 128)  # End node
GREY = (128, 128, 128)  # Grid lines


class Node:
    """
    A class representing a single node in the grid.
    """

    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        """
        Returns the position of the node as a tuple (row, col).
        """
        return self.row, self.col

    def is_closed(self):
        """
        Returns True if the node has been considered (closed).
        """
        return self.color == RED

    def is_open(self):
        """
        Returns True if the node is open for consideration.
        """
        return self.color == GREEN

    def is_barrier(self):
        """
        Returns True if the node is a barrier.
        """
        return self.color == BLACK

    def is_start(self):
        """
        Returns True if the node is the start node.
        """
        return self.color == PINK

    def is_end(self):
        """
        Returns True if the node is the end node.
        """
        return self.color == BLUE

    def reset(self):
        """
        Resets the node to its default color.
        """
        self.color = WHITE

    def make_start(self):
        """
        Sets the node color to the start color.
        """
        self.color = PINK

    def make_closed(self):
        """
        Sets the node color to the closed color.
        """
        self.color = RED

    def make_open(self):
        """
        Sets the node color to the open color.
        """
        self.color = GREEN

    def make_barrier(self):
        """
        Sets the node color to the barrier color.
        """
        self.color = BLACK

    def make_end(self):
        """
        Sets the node color to the end color.
        """
        self.color = BLUE

    def make_path(self):
        """
        Sets the node color to the path color.
        """
        self.color = PURPLE

    def draw(self, win):
        """
        Draws the node on the window.
        Args:
            win (pygame.Surface): The window to draw the node on.
        """
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        """
        Updates the neighbors of the node.
        Args:
            grid (list): The grid containing all the nodes.
        """
        self.neighbours = []
        # Moving down in the grid
        if (
            self.row < self.total_rows - 1
            and not grid[self.row + 1][self.col].is_barrier()
        ):
            self.neighbours.append(grid[self.row + 1][self.col])
        # Moving up in the grid
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row - 1][self.col])
        # Moving right in the grid
        if (
            self.col < self.total_rows - 1
            and not grid[self.row][self.col + 1].is_barrier()
        ):
            self.neighbours.append(grid[self.row][self.col + 1])
        # Moving left in the grid
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def heuristic(p1, p2):
    """
    Heuristic function for A* algorithm using Manhattan distance.
    Args:
        p1 (tuple): The position of the first node.
        p2 (tuple): The position of the second node.
    Returns:
        int: The Manhattan distance between the two nodes.
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def create_grid(rows, width):
    """
    Creates a grid of nodes.
    Args:
        rows (int): The number of rows and columns in the grid.
        width (int): The width of the window.
    Returns:
        list: A 2D list representing the grid.
    """
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    """
    Draws grid lines on the window.
    Args:
        win (pygame.Surface): The window to draw on.
        rows (int): The number of rows and columns in the grid.
        width (int): The width of the window.
    """
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    """
    Draws the entire grid on the window.
    Args:
        win (pygame.Surface): The window to draw on.
        grid (list): The grid containing all the nodes.
        rows (int): The number of rows and columns in the grid.
        width (int): The width of the window.
    """
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    """
    Gets the position of the mouse click in terms of grid coordinates.
    Args:
        pos (tuple): The (x, y) position of the mouse click.
        rows (int): The number of rows and columns in the grid.
        width (int): The width of the window.
    Returns:
        tuple: The (row, col) position in the grid.
    """
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def reconstruct_path(came_from, current, draw):
    """
    Reconstructs the path from start to end node.
    Args:
        came_from (dict): A dictionary mapping nodes to their predecessors.
        current (Node): The current node.
        draw (function): The function to draw the grid.
    """
    while current in came_from:
        current = came_from[current]
        if not current.is_start():  # Do not recolor the start node
            current.make_path()
        draw()


def a_star_algorithm(draw, grid, start, end):
    """
    Runs the A* algorithm to find the shortest path.
    Args:
        draw (function): The function to draw the grid.
        grid (list): The grid containing all the nodes.
        start (Node): The start node.
        end (Node): The end node.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + heuristic(
                    neighbour.get_pos(), end.get_pos()
                )

                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def instructions_page():
    """
    Displays the instructions page.
    """
    WIN.fill(WHITE)
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    text = font.render("Welcome to A* Pathfinder Algorithm", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, 100))
    WIN.blit(text, text_rect)

    instructions = [
        "Instructions:",
        "1. Left-click to add the start node (PINK).",
        "2. Left-click again to add the end node (BLUE).",
        "3. After adding start and end nodes, left-click to add barriers (Black).",
        "4. Right-click to remove a node.",
        "5. Click 'Space' to start the algorithm.",
        "",
        "Press 'Start' to begin!",
    ]

    y_offset = 200
    for instruction in instructions:
        text = font.render(instruction, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, y_offset))
        WIN.blit(text, text_rect)
        y_offset += 40

    pygame.display.update()


def draw_start_button():
    """
    Draws the start button.
    """
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    text = font.render("Start", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, 600))
    pygame.draw.rect(
        WIN,
        GREEN,
        (
            text_rect.x - 10,
            text_rect.y - 10,
            text_rect.width + 20,
            text_rect.height + 20,
        ),
    )
    WIN.blit(text, text_rect)
    pygame.display.update()


def draw_restart_quit_buttons():
    """
    Draws the restart and quit buttons.
    """
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    restart_text = font.render("Restart", True, BLACK)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2 - 100, 600))
    pygame.draw.rect(
        WIN,
        GREEN,
        (
            restart_rect.x - 10,
            restart_rect.y - 10,
            restart_rect.width + 20,
            restart_rect.height + 20,
        ),
    )
    WIN.blit(restart_text, restart_rect)

    quit_text = font.render("Quit", True, BLACK)
    quit_rect = quit_text.get_rect(center=(WIDTH // 2 + 100, 600))
    pygame.draw.rect(
        WIN,
        RED,
        (
            quit_rect.x - 10,
            quit_rect.y - 10,
            quit_rect.width + 20,
            quit_rect.height + 20,
        ),
    )
    WIN.blit(quit_text, quit_rect)
    pygame.display.update()


def main(win, width):
    """
    The main function to run the A* Pathfinder Algorithm.
    Args:
        win (pygame.Surface): The window to draw on.
        width (int): The width of the window.
    """
    rows = 50
    grid = create_grid(rows, width)

    start_node = None
    end_node = None

    run = True
    started = False
    path_found = False

    while run:
        draw(win, grid, rows, width)
        if path_found:
            draw_restart_quit_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started and not path_found:
                continue

            if pygame.mouse.get_pressed()[0]:  # LEFT CLICK
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                node = grid[row][col]
                if not start_node and node != end_node:
                    start_node = node
                    start_node.make_start()

                elif not end_node and node != start_node:
                    end_node = node
                    end_node.make_end()

                elif node != end_node and node != start_node:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT CLICK
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                node = grid[row][col]
                node.reset()
                if node == start_node:
                    start_node = None
                elif node == end_node:
                    end_node = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_node and end_node:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)

                    path_found = a_star_algorithm(
                        lambda: draw(win, grid, rows, width), grid, start_node, end_node
                    )
                    started = True

                if event.key == pygame.K_r:
                    start_node = None
                    end_node = None
                    grid = create_grid(rows, width)
                    started = False
                    path_found = False

            if path_found:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if 240 <= pos[0] <= 360 and 570 <= pos[1] <= 630:
                            # Restart button clicked
                            start_node = None
                            end_node = None
                            grid = create_grid(rows, width)
                            started = False
                            path_found = False
                        elif 440 <= pos[0] <= 560 and 570 <= pos[1] <= 630:
                            # Quit button clicked
                            run = False

    pygame.quit()


def display_instructions_and_start():
    """
    Displays instructions and handles the start button click.
    Returns:
        bool: True if the start button is clicked, False otherwise.
    """
    instructions_page()
    draw_start_button()
    start_button_clicked = False

    while not start_button_clicked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if 350 <= pos[0] <= 450 and 570 <= pos[1] <= 630:
                        start_button_clicked = True
                        return True


if __name__ == "__main__":
    if display_instructions_and_start():
        main(WIN, WIDTH)
