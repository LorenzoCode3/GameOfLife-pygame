import pygame
import numpy

class Button:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.backgroundColor = DARKGREY
        self.backgroundHoverColor = WHITE
        self.text = text
        self.textColor = BLACK
        self.textSurface = FONT.render(text, True, self.textColor)

    # Handles button click returning true if the button gets clicked
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
            else:
                return False
    
    # Draws the button, handling hover effect
    def draw(self, window, mousePos):
        if self.rect.collidepoint(mousePos): #pygame.mouse.get_pos()
            pygame.draw.rect(window, self.backgroundColor, self.rect, 0)
        else:
            pygame.draw.rect(window, self.backgroundHoverColor, self.rect, 0)
        window.blit(self.textSurface, (self.rect.x+5, self.rect.y+5))

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = LIGHTGREY
        self.text = text
        self.textSurface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box
            self.color = DARKGREY if self.active else LIGHTGREY
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text
                self.textSurface = FONT.render(self.text, True, self.color)

    def draw(self, window):
        # Blit the text
        window.blit(self.textSurface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect
        pygame.draw.rect(window, self.color, self.rect, 2)

def drawGrid():
    # Blocksize describe the size(in pixels) of every cell
    blockSize = int(GRID_WIDTH/matrixDim)
    # Iterate through the grid(also the matrix)
    for x in range(0, GRID_WIDTH, blockSize):
        for y in range(0, GRID_HEIGHT, blockSize):
            # Create rect object with the position[x, y], and the size of the cell[blockSize, blockSize]
            rect = pygame.Rect(x, y, blockSize, blockSize)
            # If the value of the matrix[x, y] is 0 draw white cell, if 1 draw black cell
            if(matrix.item((int(x/blockSize), int(y/blockSize))) == 0):
                pygame.draw.rect(window, WHITE, rect, 0)
                pygame.draw.rect(window, LIGHTGREY, rect, 1)
            else:
                pygame.draw.rect(window, BLACK, rect, 0)
                pygame.draw.rect(window, LIGHTGREY, rect, 1)

def nextGenereation():
    # Creating a new temporary empty matrix to work on
    nextMatrix = numpy.random.randint(1, size=((matrixDim, matrixDim)))

    # Interating the matrix to update the state of the cells
    for x in range(matrixDim):
        for y in range(matrixDim):
            count = 0
			# 1|2|3
			# 4| |5
			# 6|7|8
            if(matrix.item((int(x-1),int(y-1))) == 1): count += 1 #1
            if(matrix.item((int(x),int(y-1))) == 1): count += 1 #2
            if(matrix.item((int(x+1),int(y-1))) == 1): count += 1 #3
            if(matrix.item((int(x-1),int(y))) == 1): count += 1 #4
            if(matrix.item((int(x+1),int(y))) == 1): count += 1 #5
            if(matrix.item((int(x-1),int(y+1))) == 1): count += 1 #6
            if(matrix.item((int(x),int(y+1))) == 1): count += 1 #7
            if(matrix.item((int(x+1),int(y+1))) == 1): count += 1 #8
			
			# Living cell conditions
            if((count < 2) and (matrix.item((x,y)) == 1)): nextMatrix[x][y] = 0
            if((count == 2 or count == 3) and (matrix.item((x,y)) == 1)): nextMatrix[x][y] = 1
            if((count>3) and (matrix.item((x,y)) == 1)): nextMatrix[x][y] = 0
			# Dead cell condition
            if((count==3) and (matrix.item((x,y)) == 0)): nextMatrix[x][y] = 1

    # Saving results from the temporary matrix to the main one 
    for x in range(matrixDim):
        for y in range(matrixDim):
            matrix[x][y] = nextMatrix.item((x,y))

def drawUI():
    # Draws the input boxes
    for box in inputBoxes:
        box.draw(window)

    # Draws the labels, specifying the position
    window.blit(label1, (WINDOW_WIDTH-(WINDOW_WIDTH/2)+160, (WINDOW_HEIGHT/2)+64))
    window.blit(label2, (WINDOW_WIDTH-(WINDOW_WIDTH/2)+160, (WINDOW_HEIGHT/2)+128))
    window.blit(label3, (WINDOW_WIDTH-(WINDOW_WIDTH/2)+160, (WINDOW_HEIGHT/2)+96))
    window.blit(label4, (WINDOW_WIDTH-(WINDOW_WIDTH/2)+160, (WINDOW_HEIGHT/2)+160))
    window.blit(descriptionLabel1, (WINDOW_WIDTH-(WINDOW_WIDTH/2)+160, (WINDOW_HEIGHT/2)-64))
    window.blit(descriptionLabel2, (WINDOW_WIDTH-(WINDOW_WIDTH/2)+160, (WINDOW_HEIGHT/2)-32))
    window.blit(descriptionLabel3, (WINDOW_WIDTH-(WINDOW_WIDTH/2)+160, (WINDOW_HEIGHT/2)))

    # Draws the buttons
    mousePos = pygame.mouse.get_pos()
    for button in buttons:
        button.draw(window, mousePos)

##those two functions can be merged in one
def createRandomMatrix(dim):
    # The nextGeneration() algorithm has a problem on the right and bottom corner(matrix goes out of bounds)
    # So i've added a row and a column to make it work as intended
    dim += 1
    # Filling the matrix with 0s and 1s
    mat = numpy.random.randint(2, size=((dim, dim)))
    # Slicing to fill with 0s the right and bottom corner
    mat[-1:, :] = 0
    mat[:, -1:] = 0
    print('Random matrix generated')
    return mat

def createBlankMatrix(dim):
    dim += 1
    # Filling the matrix with 0s
    mat = numpy.random.randint(1, size=((dim, dim)))
    # Slicing to fill with 0s the right and bottom corner
    mat[-1:, :] = 0
    mat[:, -1:] = 0
    print('Blank matrix generated')
    return mat

def pauseGeneration(pause):
    # Negate the passed value and return it, printing the state
    pause = not pause
    if(pause == True): print("Generation paused")
    if(pause == False): print("Generation unpaused")
    return pause

# Pygame setup
pygame.init()

# Constraints
BLACK = pygame.Color("gray5")
DARKGREY = pygame.Color("gray30")
GREY = pygame.Color("gray45")
LIGHTGREY = pygame.Color("gray60")
WHITE = pygame.Color("gray85")
GRID_HEIGHT = 720
GRID_WIDTH = 720
WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280
FONT = pygame.font.Font(None, 32)

# Pygame window and time variables
pygame.display.set_caption('GameOfLife in Pygame')
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Global varibles
paused = False
fps = 5
matrixDim = 20

# Matrix container
matrix = createRandomMatrix(matrixDim)

# UI elements containers
# Input boxes
inputBox1 = InputBox(WINDOW_WIDTH-(WINDOW_WIDTH/4)+32, (WINDOW_HEIGHT/2)+64, 128, 32, str(matrixDim))
inputBox2 = InputBox(WINDOW_WIDTH-(WINDOW_WIDTH/4)+32, (WINDOW_HEIGHT/2)+128, 128, 32, str(fps))
inputBoxes = [inputBox1, inputBox2]

# Labels
label1 = FONT.render("Grid Size:", 1, BLACK)
label2 = FONT.render("Fps:", 1, BLACK)
label3 = FONT.render("Min:2, Max:80", 1, BLACK)
label4 = FONT.render("Min:1, Max:30", 1, BLACK)
descriptionLabel1 = FONT.render('- To change tiles directly on the grid' , True , BLACK)
descriptionLabel2 = FONT.render('pause the generation first' , True , BLACK)
descriptionLabel3 = FONT.render('- Press space to pause' , True , BLACK)

# Buttons
button1 = Button(WINDOW_WIDTH-(WINDOW_WIDTH/3), 64, 200, 32, 'Pause')
button2 = Button(WINDOW_WIDTH-(WINDOW_WIDTH/3), 128, 200, 32, 'Delete all')
button3 = Button(WINDOW_WIDTH-(WINDOW_WIDTH/3), 192, 200, 32, 'Generate random')
buttons = [button1, button2, button3]

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Checks if keys are pressed
        if event.type == pygame.KEYDOWN:
            # If space pause the game
            if(event.dict.get("key") == pygame.K_SPACE):
                paused = pauseGeneration(paused)
        # Checks mouse left click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if(paused):
                # Gets the right cell of the matrix from mouse position and cell size
                blockSize = int(GRID_WIDTH/matrixDim)
                x = int(event.dict.get("pos")[0] / blockSize)
                y = int(event.dict.get("pos")[1] / blockSize)
                # Negate the value of the cell inside the matrix
                if((x < matrixDim) and (y < matrixDim)):
                    if(matrix[x][y] == 1): matrix[x][y] = 0
                    else: matrix[x][y] = 1
        # Handle events regarding the grid size input box, saving result into newdim
        newDim = inputBox1.handle_event(event)
        # If newdim isn't none change the size of the matrix
        if(newDim):
            # Cast string into int
            newDim = int(newDim)
            if(newDim >= 2 and newDim <= 80):
                print("Matrix dim setted to:", newDim)
                matrixDim = newDim
                matrix = createBlankMatrix(matrixDim)
        # If newspeed isn't none change the fps
        newSpeed = inputBox2.handle_event(event)
        if(newSpeed):
            # Cast string into int
            newSpeed = int(newSpeed)
            if(newSpeed >= 1 and newSpeed <= 30):
                print("Fps setted to:", newSpeed)
                fps = newSpeed
        # Checks buttons state
        if button1.handle_event(event) == True:
            paused = pauseGeneration(paused)
        if button2.handle_event(event) == True:
            matrix = createBlankMatrix(matrixDim)
        if button3.handle_event(event) == True:
            matrix = createRandomMatrix(matrixDim)

    # Does background color, prints grid and UI
    window.fill(GREY)
    drawGrid()
    drawUI()

    # Refresh the screen visualizing elements
    pygame.display.flip()

    # Block generations if game is paused
    if(not paused):
        nextGenereation()
    
    ##should do this with 2 threads: one for the menu at 30 and one for the grid at 'fps'
    if(not paused):
        clock.tick(fps)
    else:
        clock.tick(30)

pygame.quit()