# Game of Life in Pygame

This repository contains an implementation of Conway's famous "Game of Life" using Python and Pygame for graphics and user interaction.

## Features

- **Game of Life Simulation**: Computes subsequent generations of the grid based on Conway's rules.
- **Interactive Graphical Interface**: Displays the grid and allows direct interaction with cells when the simulation is paused.
- **Simulation Controls**: Dynamically adjust the frames per second (FPS) and grid size through dedicated input fields.
- **Reset and Random Generation**: Easily reset the grid or generate a random initial configuration with a simple click.

## Project Structure

- **config.py**  
  Contains the constants and base configurations such as colors, window dimensions, and font settings.

- **game.py**  
  Contains the main `GameOfLife` class which handles simulation logic, user interface, and event processing (keyboard, mouse clicks, etc.).

- **simulation.py**  
  Implements functions for creating the initial matrix, computing the next generation (using vectorized operations with NumPy), and drawing the grid.

- **ui.py**  
  Defines user interface components, including buttons and input boxes, for interacting with the simulation.

- **main.py**  
  The entry point of the program. It initializes Pygame, creates an instance of `GameOfLife`, and starts the simulation.

## Requirements

- Python 3.x
- [Pygame](https://www.pygame.org/news)
- [NumPy](https://numpy.org/)

## Installation

1. **Clone the repository:**

  ```bash
    git clone https://github.com/LorenzoCode3/GameOfLife-pygame.git
  ```

2. **Install the dependencies:**

  ```bash
    pip install pygame numpy
  ```

3. **Run the game:**

  ```bash
    python main.py
  ```

### Controls

- **Pause and Resume:**  
  Press the spacebar or click the "Pause" button to toggle the simulation's pause state.

- **Modify the Grid:**  
  In pause mode, click on a cell in the grid to toggle its state (alive/dead).

- **Adjust Settings:**  
  Use the input boxes to change:
  - The grid size (allowed values: minimum 2, maximum 80).
  - The frames per second (FPS) (allowed values: minimum 1, maximum 30).

- **Reset and Random Generation:**  
  Click the "Delete all" button to reset the grid or the "Generate random" button to create a random initial configuration.

## Contributing

Contributions are welcome! If you wish to propose changes, report bugs, or add new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Enjoy your Game of Life in Pygame!
