import pygame
from game import GameOfLife

def main():
    pygame.init()
    game = GameOfLife()
    game.run()

if __name__ == '__main__':
    main()
