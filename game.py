import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_WIDTH, GRID_HEIGHT, FONT, BLACK, GREY
from ui import Button, InputBox
from simulation import create_matrix, next_generation, draw_grid

class GameOfLife:
    def __init__(self):
        # Initial state of the simulation
        self.paused = False
        self.fps = 5
        self.matrix_dim = 20
        self.matrix = create_matrix(self.matrix_dim, randomize=True)

        # Initialize the window and clock
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Game of Life in Pygame')
        self.clock = pygame.time.Clock()

        # UI elements: input boxes, buttons, and labels
        self.input_box_dim = InputBox(
            WINDOW_WIDTH - (WINDOW_WIDTH // 4) + 32,
            (WINDOW_HEIGHT // 2) + 64,
            128,
            32,
            str(self.matrix_dim)
        )
        self.input_box_fps = InputBox(
            WINDOW_WIDTH - (WINDOW_WIDTH // 4) + 32,
            (WINDOW_HEIGHT // 2) + 128,
            128,
            32,
            str(self.fps)
        )
        self.input_boxes = [self.input_box_dim, self.input_box_fps]

        self.label_grid = FONT.render("Grid Size:", True, BLACK)
        self.label_fps = FONT.render("FPS:", True, BLACK)
        self.label_grid_info = FONT.render("Min:2, Max:80", True, BLACK)
        self.label_fps_info = FONT.render("Min:1, Max:30", True, BLACK)
        self.label_desc1 = FONT.render("- To change tiles directly on the grid", True, BLACK)
        self.label_desc2 = FONT.render("  pause the generation first", True, BLACK)
        self.label_desc3 = FONT.render("- Press space to pause", True, BLACK)

        self.button_pause = Button(WINDOW_WIDTH - (WINDOW_WIDTH // 3), 64, 200, 32, 'Pause')
        self.button_clear = Button(WINDOW_WIDTH - (WINDOW_WIDTH // 3), 128, 200, 32, 'Delete all')
        self.button_rand = Button(WINDOW_WIDTH - (WINDOW_WIDTH // 3), 192, 200, 32, 'Generate random')
        self.buttons = [self.button_pause, self.button_clear, self.button_rand]

    def pause_generation(self):
        # Toggle the pause state and print the current status.
        self.paused = not self.paused
        print("Generation paused" if self.paused else "Generation unpaused")

    def handle_events(self):
        # Handle all events (inputs, clicks, etc.).
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                # Toggle pause with the space key
                if event.key == pygame.K_SPACE:
                    self.pause_generation()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # If the simulation is paused, allow modifying cells by clicking on the grid
                if self.paused:
                    cell_count = self.matrix_dim
                    block_size = GRID_WIDTH // cell_count
                    x, y = event.pos[0] // block_size, event.pos[1] // block_size
                    if x < cell_count and y < cell_count:
                        # Toggle the cell state
                        self.matrix[y, x] = 0 if self.matrix[y, x] == 1 else 1

            # Handle input boxes
            new_dim = self.input_box_dim.handle_event(event)
            if new_dim:
                try:
                    new_dim_int = int(new_dim)
                    if 2 <= new_dim_int <= 80:
                        print("Matrix dimension set to:", new_dim_int)
                        self.matrix_dim = new_dim_int
                        self.matrix = create_matrix(self.matrix_dim, randomize=False)
                    else:
                        print("Dimension out of range (2-80)")
                except ValueError:
                    print("Invalid grid size input.")

            new_fps = self.input_box_fps.handle_event(event)
            if new_fps:
                try:
                    new_fps_int = int(new_fps)
                    if 1 <= new_fps_int <= 30:
                        print("FPS set to:", new_fps_int)
                        self.fps = new_fps_int
                    else:
                        print("FPS out of range (1-30)")
                except ValueError:
                    print("Invalid FPS input.")

            # Handle buttons
            if self.button_pause.handle_event(event):
                self.pause_generation()
            if self.button_clear.handle_event(event):
                self.matrix = create_matrix(self.matrix_dim, randomize=False)
                print("Blank matrix generated")
            if self.button_rand.handle_event(event):
                self.matrix = create_matrix(self.matrix_dim, randomize=True)
                print("Random matrix generated")
        return True

    def draw_ui(self):
        # Draw UI elements: input boxes, labels, and buttons.
        # Draw input boxes
        for box in self.input_boxes:
            box.draw(self.window)

        # Draw labels and descriptions
        base_x = WINDOW_WIDTH - (WINDOW_WIDTH // 2) + 160
        base_y = WINDOW_HEIGHT // 2
        self.window.blit(self.label_grid, (base_x, base_y + 64))
        self.window.blit(self.label_fps, (base_x, base_y + 128))
        self.window.blit(self.label_grid_info, (base_x, base_y + 96))
        self.window.blit(self.label_fps_info, (base_x, base_y + 160))
        self.window.blit(self.label_desc1, (base_x, base_y - 64))
        self.window.blit(self.label_desc2, (base_x, base_y - 32))
        self.window.blit(self.label_desc3, (base_x, base_y))

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.draw(self.window, mouse_pos)

    def run(self):
        # Main game loop.
        running = True
        while running:
            running = self.handle_events()

            # Update the background and draw the grid and UI
            self.window.fill(GREY)
            draw_grid(self.window, self.matrix, GRID_WIDTH, GRID_HEIGHT)
            self.draw_ui()
            pygame.display.flip()

            # Update the simulation if not paused
            if not self.paused:
                self.matrix = next_generation(self.matrix)
                self.clock.tick(self.fps)
            else:
                self.clock.tick(30)
        pygame.quit()
