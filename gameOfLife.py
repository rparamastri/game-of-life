# gameOfLife.py
# author: Renata Paramastri
# Game of life with matplotlib

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib.widgets import Button

ALIVE = 1
DEAD = 0

# board settings
HEIGHT = 30
WIDTH = 30
CMAP = plt.cm.inferno
SHOW_GRID = False
INTERVAL = 175  # milliseconds pause between frames
GRID_BOTTOM = 0.2

class Game:
    def __init__(self, mat):
        self.mat = mat
        self.height, self.width = mat.get_array().shape
        matFig = self.mat.figure

        self.animated = False
        self.animation = FuncAnimation(fig, self.update, interval = INTERVAL)

        self.keyCid = fig.canvas.mpl_connect('key_press_event', self.onKeyPress)
        self.cid = matFig.canvas.mpl_connect('pick_event', self.onPick)


    def randomizeBoard(self):
        """ Populates the board with ones and zeros randomly."""
        randomBoard = np.random.randint(2, size=(self.height, self.width))
        self.mat.set_data(randomBoard)

    def clearBoard(self):
        zeroMatrix = np.zeros((self.height, self.width))
        self.mat.set_data(zeroMatrix)

    def countNeighbours(self, row, col):
        """Given a cell at row and col in the board, count the number
        of neighbours that are alive.
        If the cell is at an edge cell, the function treats the board as a torus.
        Returns the number of neighbours that are alive.
        """
        board = self.mat.get_array()
        neighbours = 0

        # use mods to implement the torus board
        rowAbove = board[(row - 1) % self.height]
        neighbours += rowAbove[(col - 1) % self.width]
        neighbours += rowAbove[col]
        neighbours += rowAbove[(col + 1) % self.width]

        sameRow = board[row]
        neighbours += sameRow[(col - 1) % self.width]
        neighbours += sameRow[(col + 1) % self.width]

        rowBelow = board[(row + 1) % self.height]
        neighbours += rowBelow[(col - 1) % self.width]
        neighbours += rowBelow[col]
        neighbours += rowBelow[(col + 1) % self.width]

        return neighbours

    def nextLifeGeneration(self):
        """ Given a board, generate the next board
        based on Conway's Game of Life rules.
        Returns this new matrix.
        """
        nextGen = np.zeros((self.height, self.width))
        board = self.mat.get_array()

        for row in range(self.height):
            for col in range(self.width):
                neighbours = self.countNeighbours(row, col)
                cell = board[row][col]
                if cell == ALIVE and (neighbours < 2 or neighbours > 3):
                    nextGen[row][col] = DEAD
                elif cell == DEAD and neighbours == 3:
                    nextGen[row][col] = ALIVE
                else:
                    nextGen[row][col] = cell

        return nextGen

    def onPick(self, event):
        """ Handles clicks on the board grid. """
        if event.artist != mat:
            return
        else:
            mouseEvent = event.mouseevent
            col = round(mouseEvent.xdata)
            row = round(mouseEvent.ydata)
            data = self.mat.get_array()

            # toggle cell status
            if data[row][col] == ALIVE:
                data[row][col] = DEAD
            else:
                data[row][col] = ALIVE

            self.mat.set_data(data)
            self.mat.figure.canvas.draw()

    def onKeyPress(self, event):
        """ Handles the space bar being pressed to stop/play animation. """
        if event.key == ' ':
            self.toggleAnimation()

    def toggleAnimation(self):
            self.animated = not self.animated
            animate()

    def update(self, i):
        """ Wrapper function of nextLifeGeneration for FuncAnimation."""
        if self.animated:  # only compute a new board when animating
            nextGen = self.nextLifeGeneration()
            self.mat.set_data(nextGen)
        return self.mat,

def animate():
    """ Tell pyplot to draw the figure. """
    fig.canvas.draw()

def pButtonClicked(event):
    game.toggleAnimation()

    if game.animated:
        pButton.label.set_text("Pause")
    else:  # when animation is paused
        pButton.label.set_text("Play")

def randomButtonClicked(event):
    game.randomizeBoard()

def clearButtonClicked(event):
    game.clearBoard()

print("Click on the grid to kill/resurrect cells!")
print("Hit the space bar to start animating.")

plt.ion()  # turn on interactive mode so that users can type in shell commands

fig, ax = plt.subplots()
plt.subplots_adjust(bottom = GRID_BOTTOM)  # leave space for button

randomData = np.random.randint(2, size=(HEIGHT,WIDTH))
mat = ax.matshow(randomData, picker = True, cmap = CMAP)

if SHOW_GRID:
    xAxis = ax.get_xaxis()
    yAxis = ax.get_yaxis()

    xAxis.set_ticklabels([])
    yAxis.set_ticklabels([])

    xAxis.set_ticks(np.arange(WIDTH)  + 0.5)
    yAxis.set_ticks(np.arange(HEIGHT) + 0.5)

    ax.grid(color = 'w')

game = Game(mat)

# button for pause and play
axPButton = plt.axes([0.8, 0.1, 0.1, 0.05])
pButton = Button(axPButton, "Play")
pButton.on_clicked(pButtonClicked)

# button for randomizing board
axRandomButton = plt.axes([0.65, 0.1, 0.1, 0.05])
randomButton = Button(axRandomButton, "Random")
randomButton.on_clicked(randomButtonClicked)

# button for clearing the board
axClearButton = plt.axes([0.5, 0.1, 0.1, 0.05])
clearButton = Button(axClearButton, "Clear")
clearButton.on_clicked(clearButtonClicked)


plt.show()

