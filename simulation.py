import numpy as np
import pygame
from config import LIGHTGREY, BLACK, WHITE, GRID_WIDTH

def create_matrix(dim: int, randomize: bool = True) -> np.ndarray:
    """
    Creates a matrix ((dim+1) x (dim+1)) used for the simulation.
    If randomize is True, values are 0 or 1; otherwise, the matrix is empty.
    The last row and column are forced to 0 to handle borders.
    """
    dim += 1
    if randomize:
        mat = np.random.randint(0, 2, size=(dim, dim))
    else:
        mat = np.zeros((dim, dim), dtype=int)
    mat[-1, :] = 0
    mat[:, -1] = 0
    return mat

def next_generation(matrix: np.ndarray) -> np.ndarray:
    """
    Calculates the next generation of the Game of Life in a vectorized way.
    Uses padding to handle borders and slice summing to count neighbors.
    """
    padded = np.pad(matrix, pad_width=1, mode='constant', constant_values=0)
    # Count neighbors by summing slices
    neighbor_count = (
        padded[:-2, :-2] + padded[:-2, 1:-1] + padded[:-2, 2:] +
        padded[1:-1, :-2] +                      padded[1:-1, 2:] +
        padded[2:  , :-2] + padded[2:  , 1:-1] + padded[2:  , 2:]
    )
    # Apply the rules:
    # A live cell (1) survives with 2 or 3 neighbors;
    # A dead cell (0) becomes alive with exactly 3 neighbors.
    new_matrix = np.where(
        ((matrix == 1) & ((neighbor_count == 2) | (neighbor_count == 3))) |
        ((matrix == 0) & (neighbor_count == 3)),
        1,
        0
    )
    return new_matrix

def draw_grid(surface, matrix: np.ndarray, grid_width: int, grid_height: int):
    # Draws the grid adapting exactly to the grid dimensions.
    # The number of cells (excluding the last row/column used for borders)
    cell_count = matrix.shape[0] - 1

    # Calculate the positions of the edges in a fractional manner
    x_edges = [round(j * grid_width / cell_count) for j in range(cell_count + 1)]
    y_edges = [round(i * grid_height / cell_count) for i in range(cell_count + 1)]
    
    # Draw each cell using the calculated edges
    for i in range(cell_count):
        for j in range(cell_count):
            rect = pygame.Rect(
                x_edges[j], 
                y_edges[i], 
                x_edges[j+1] - x_edges[j], 
                y_edges[i+1] - y_edges[i]
            )
            if matrix[i, j] == 1:
                pygame.draw.rect(surface, BLACK, rect)
            else:
                pygame.draw.rect(surface, WHITE, rect)
            pygame.draw.rect(surface, LIGHTGREY, rect, 1)
