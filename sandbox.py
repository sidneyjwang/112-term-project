from cmu_112_graphics import *
import random
import time

####################################
# this isn't sand
####################################

# this project uses cmu-112-graphics, which was taken from
# https://www.cs.cmu.edu/~112/

# from the 112 course website:
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

class Particle:
    GRAVITY = 1.5
    MAX_VELOCITY = 15
    HEIGHT = 0
    WIDTH = 0
    TOTAL_PARTICLES = 0
    def __init__(self, particleNumber, col, row, xVelocity, yVelocity, intendedColor, 
                colorVariation, height, width):
        self.particleNumber = particleNumber
        self.col = col
        self.row = row
        self.yVelocity = yVelocity
        self.time = 0
        self.xVelocity = xVelocity
        self.R = intendedColor[0] + colorVariation[0]
        self.G = intendedColor[1] + colorVariation[1]
        self.B = intendedColor[1] + colorVariation[2]
        self.canDrop = True
        self.canSlide = False
        if self.R > 255: self.R = 255
        elif self.R < 0: self.R = 0
        if self.G > 255: self.G = 255
        elif self.G < 0: self.G = 0
        if self.B > 255: self.B = 255
        elif self.B < 0: self.B = 0
        self.color = rgbString(self.R, self.G, self.B)
        Particle.HEIGHT = height
        Particle.WIDTH = width
        Particle.TOTAL_PARTICLES += 1

    def getMovePosition(self):
        x, y = int(self.col + self.xVelocity), int(self.row + self.yVelocity)
        return (x, y)
    
    # drops the sand particle
    def drop(self):
        self.row += int(self.yVelocity)
        self.yVelocity += int(Particle.GRAVITY * self.time)
        self.time += 1
        self.col += int(self.xVelocity)
        self.checkLegalMove()

    # check if the proposed move would put a grain inside another one, or move
    # off the screen; if so, undoes the move
    def checkLegalMove(self):
        if self.yVelocity >= Particle.MAX_VELOCITY:
            self.yVelocity = Particle.MAX_VELOCITY
        if self.row >= Particle.HEIGHT // 10:
            self.row = Particle.HEIGHT // 10 - 1
            self.yVelocity = 0
            self.canDrop = False
            self.canSlide = False
        # revisit once sand piling starts:
        if self.col >= Particle.WIDTH // 10:
            self.col = Particle.WIDTH // 10 - 1
            self.xVelocity = 0
        elif self.col < 0:
            self.col = 0
            self.xVelocity = 0

def appStarted(app):
    app.sand = [] # a list to keep track of all particle objects
    app.timerDelay = 100 # put this at 10 when not debugging
    app.currentX = 0 # the x position of the mouse
    app.currentY = 0 # the y position of the mouse
    app.mouseIsPressed = False # boolean flag: is the mouse being held?
    app.effectiveAppWidth = 500 # for experimentation purposes: make the window smaller
    app.effectiveAppHeight = 300 # for experimentation purposes: make the window smaller
    app.sandGrainSize = 10 # for experimenation purposes: make the sand actually visible
    # keep track of the highest sand grain particle per column:
    app.maxValuesPerCol = [app.effectiveAppHeight // app.sandGrainSize-1] * (app.effectiveAppWidth // app.sandGrainSize)
    # sand grains that are no longer objects and have become part of the background
    app.sandCache = [['white'] * (app.effectiveAppWidth // app.sandGrainSize) for i in range(app.effectiveAppHeight // app.sandGrainSize)]

# update the mouse's x and y coordinates, and set the mouseIsPressed boolean to true
def mousePressed(app, event):
    app.mouseIsPressed = True
    app.currentX, app.currentY = getCell(app, event.y, event.x)

# set the mouseIsPressed boolean to false
def mouseReleased(app, event):
    app.mouseIsPressed = False

# update the mouse coordinates when moved
def mouseMoved(app, event):
    app.currentX, app.currentY = getCell(app, event.y, event.x)

# also update mouse coordinates when dragged
def mouseDragged(app, event):
    app.currentX, app.currentY = getCell(app, event.y, event.x)

# when the mouse is pressed, create a shower of sand emerging from the point
# modify here for testing purposes if a single grain is needed instead of a shower
def addParticles(app, x, y):
    sandGrainNumber = int(random.triangular(5, 10, 5))
    for i in range(sandGrainNumber):
        rVar = int(random.triangular(0, 25, 5)) * random.choice([-1, 1])
        gVar = int(random.triangular(0, 25, 5)) * random.choice([-1, 1])
        bVar = int(random.triangular(0, 25, 5)) * random.choice([-1, 1])
        signFlip = random.choice([-1, 1])
        xVelocity = int(random.triangular(0, 4, 0)) * signFlip
        yVelocity = int(random.random() * 8)
        newParticle = Particle(i, x, y, xVelocity, yVelocity, 
                        (255,100,100), (rVar,gVar,bVar), app.effectiveAppHeight, app.effectiveAppWidth)
        app.sand.append(newParticle)

# draw all of the sand objects        
def drawSand(app, canvas):
    for particle in app.sand:
        x0,y0,x1,y1 = getCellBounds(app, particle.col, particle.row)
        canvas.create_rectangle(x0,y0,x1,y1, 
                                fill=particle.color, width=0)

def getCellBounds(app, row, col):
    totalRows = app.effectiveAppHeight / app.sandGrainSize
    totalCols = app.effectiveAppWidth / app.sandGrainSize
    x0, y0 = row * app.sandGrainSize, col * app.sandGrainSize
    x1, y1 = x0 + app.sandGrainSize, y0 + app.sandGrainSize
    return x0,y0,x1,y1

# change width parameter in the rectangle call here to turn the grid on/off
def drawGrid(app, canvas):
    for row in range(app.effectiveAppWidth // app.sandGrainSize):
        for col in range(app.effectiveAppHeight // app.sandGrainSize):
            x0,y0,x1,y1 = getCellBounds(app, row, col)
            color = app.sandCache[col][row]
            if color != 'white':
                canvas.create_rectangle(x0,y0,x1,y1,fill=color,width=0)

def getCell(app, x, y):
    row = y // app.sandGrainSize
    col = x // app.sandGrainSize
    return row, col

def redrawAll(app, canvas):
    drawGrid(app, canvas)
    canvas.create_rectangle(0, 0, app.effectiveAppWidth, app.effectiveAppHeight)
    drawSand(app, canvas)

# create the particles
def timerFired(app):    
    if app.mouseIsPressed:
        addParticles(app, app.currentX, app.currentY)
    # slide!
    
    '''
    for row in range(len(app.sandCache)):
        for col in range(len(app.sandCache[0])):
            # only move the colored cells
            if app.sandCache[row][col] != 'white':
                leftCol, rightCol = col-1, col+1
                nextRow = row + 1
                # check that the left index is in range
                if (leftCol >= 0 and 
                    nextRow < app.effectiveAppHeight // app.sandGrainSize):
                    # if it is, is the south-west cell open? if so, move there!
                    if app.sandCache[nextRow][leftCol] == 'white':
                        print('slide left')
                        print(f'col:{col}', f'leftCol:{leftCol}')
                        app.sandCache[nextRow][leftCol] = app.sandCache[row][col]
                        app.sandCache[row][col] = 'white'
                        app.maxValuesPerCol[col] += 1
                        app.maxValuesPerCol[leftCol] -= 1
                        
                if (rightCol < app.effectiveAppWidth // app.sandGrainSize and
                nextRow < app.effectiveAppHeight // app.sandGrainSize):
                    if app.sandCache[nextRow][rightCol] == 'white':
                        print('slide right')
                        app.sandCache[nextRow][rightCol] = app.sandCache[row][col]
                        app.sandCache[row][col] = 'white'
                        app.maxValuesPerCol[col] += 1
                        app.maxValuesPerCol[rightCol] -= 1
    '''
    
                        

    for particle in (app.sand):
        nextX, nextY = particle.getMovePosition()
        if nextX >= app.effectiveAppWidth // app.sandGrainSize:
            nextX = app.effectiveAppWidth // app.sandGrainSize - 1
        elif nextX < 0:
            nextX = 0
        if nextY > app.maxValuesPerCol[nextX]: 
            nextY = app.maxValuesPerCol[nextX]
        # the sand hit the bottom! remove the particle and color the background
        if nextY >= app.effectiveAppHeight // app.sandGrainSize - 1: 
            app.sand.remove(particle)
            app.sandCache[app.effectiveAppHeight // app.sandGrainSize - 1][nextX] = 'blue'
            app.maxValuesPerCol[nextX] -= 1
            continue
        # the sand hit other sand! remove the particle and color the background square
        elif app.sandCache[nextY+1][nextX] != 'white': 
            app.sandCache[nextY][nextX] = 'blue'
            app.sand.remove(particle)
            app.maxValuesPerCol[nextX] -= 1
        # just go ahead and keep moving
        particle.drop()

def main():
    runApp(width=600, height=400)

if __name__ == '__main__':
    main()