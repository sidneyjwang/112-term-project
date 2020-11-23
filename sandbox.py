from cmu_112_graphics import *
import random
import time

####################################
# this isn't sand
####################################

# from the 112 course website:
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

class Particle:
    GRAVITY = 1.5
    MAX_VELOCITY = 15
    HEIGHT = 0
    WIDTH = 0
    TOTAL_PARTICLES = 0
    def __init__(self, particleNumber, xPos, yPos, xVelocity, yVelocity, intendedColor, 
                colorVariation, height, width):
        self.particleNumber = particleNumber
        self.xPos = xPos
        self.yPos = yPos
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
        x, y = int(self.xPos + self.xVelocity), int(self.yPos + self.yVelocity)
        return (x, y)
    
    # drops the sand particle
    def drop(self):
        self.yPos += int(self.yVelocity)
        self.yVelocity += int(Particle.GRAVITY * self.time)
        self.time += 1
        self.xPos += int(self.xVelocity)
        self.checkLegalMove()

    # check if the proposed move would put a grain inside another one, or move
    # off the screen; if so, undoes the move
    def checkLegalMove(self):
        if self.yVelocity >= Particle.MAX_VELOCITY:
            self.yVelocity = Particle.MAX_VELOCITY
        if self.yPos > Particle.HEIGHT:
            self.yPos = Particle.HEIGHT
            self.yVelocity = 0
            self.canDrop = False
            self.canSlide = False
        # revisit once sand piling starts:
        if self.xPos > Particle.WIDTH:
            self.xPos = Particle.WIDTH
            self.xVelocity = 0
        elif self.xPos < 0:
            self.xPos = 0
            self.xVelocity = 0


def appStarted(app):
    app.sand = [] # a list to keep track of all particle objects
    app.timerDelay = 100 # put this at 10 when not debugging
    app.currentX = 0 # the x position of the mouse
    app.currentY = 0 # the y position of the mouse
    app.mouseIsPressed = False # boolean flag: is the mouse being held?
    app.maxValuesPerCol = {}
    app.effectiveAppWidth = 500 # for experimentation purposes: make the window smaller
    app.effectiveAppHeight = 350 # for experimentation purposes: make the window smaller
    app.sandGrainSize = 10 # for experimenation purposes: make the sand actually visible
    for i in range(1, 501):
        app.maxValuesPerCol[i] = 300

# update the mouse's x and y coordinates, and set the boolean to true
def mousePressed(app, event):
    app.mouseIsPressed = True
    app.currentX, app.currentY = getCell(app, event.y, event.x)

# set boolean to false
def mouseReleased(app, event):
    app.mouseIsPressed = False

# update the mouse coordinates when moved
def mouseMoved(app, event):
    app.currentX, app.currentY = getCell(app, event.y, event.x)

# also update mouse coordinates when dragged
def mouseDragged(app, event):
    app.currentX, app.currentY = getCell(app, event.y, event.x)

# when the mouse is pressed, create a shower of sand emerging from the point
def addParticles(app, x, y):
    sandGrainNumber = int(random.triangular(5, 10, 5))
    for i in range(sandGrainNumber):
        rVar = int(random.triangular(0, 25, 5)) * random.choice([-1, 1])
        gVar = int(random.triangular(0, 25, 5)) * random.choice([-1, 1])
        bVar = int(random.triangular(0, 25, 5)) * random.choice([-1, 1])
        signFlip = random.choice([-1, 1])
        xVelocity = int(random.triangular(0, 4, 1)) * signFlip
        yVelocity = random.random()**2 * 8
        newParticle = Particle(i, x, y, xVelocity, yVelocity, 
                        (255,100,100), (rVar,gVar,bVar), app.effectiveAppHeight, app.effectiveAppWidth)
        app.sand.append(newParticle)

# draw all of the sand objects        
def drawSand(app, canvas):
    for particle in app.sand:
        x0,y0,x1,y1 = getCellBounds(app, particle.xPos, particle.yPos)
        print(x0,y0,x1,y1)
        canvas.create_rectangle(x0,y0,x1,y1, 
                                fill=particle.color, width=0)

def getCellBounds(app, row, col):
    width = 10
    totalRows = app.effectiveAppHeight / app.sandGrainSize
    totalCols = app.effectiveAppWidth / app.sandGrainSize
    x0, y0 = row * app.sandGrainSize, col * app.sandGrainSize
    x1, y1 = x0 + app.sandGrainSize, y0 + app.sandGrainSize
    return x0,y0,x1,y1

def drawGrid(app, canvas):
    for row in range(app.effectiveAppWidth // app.sandGrainSize):
        for col in range(app.effectiveAppHeight // app.sandGrainSize):
            x0,y0,x1,y1 = getCellBounds(app, row, col)
            canvas.create_rectangle(x0,y0,x1,y1)

def getCell(app, x, y):
    row = y // app.sandGrainSize
    col = x // app.sandGrainSize
    print(row, col)
    return row, col

def redrawAll(app, canvas):
    drawGrid(app, canvas)
    canvas.create_rectangle(0, 0, app.effectiveAppWidth, app.effectiveAppHeight)
    drawSand(app, canvas)

# create the particles
def timerFired(app):
    if app.mouseIsPressed:
        addParticles(app, app.currentX, app.currentY)
    for particle in range(len(app.sand)):
        # at some point once everything is done, check up here if canSlide and 
        # canDrop are both false. if so, just continue; there's no point in going
        # through the rest of this.
        nextX, nextY = app.sand[particle].getMovePosition()
        if nextX > 500:
            nextX = 500
        elif nextX < 1:
            nextX = 1
        # print(f'Particle #{particle}', 'Current position:', f'({app.sand[particle].xPos}, {app.sand[particle].yPos})')
        # print(f'Particle #{particle}', 'Next position:', f'({nextX}, {nextY})')
        maxColValue = app.maxValuesPerCol[nextX]
        # the sand grain has reached as far down as it will go!
        if app.sand[particle].canDrop:    
            if nextY > maxColValue:
                app.sand[particle].yPos = maxColValue - app.sandGrainSize
                app.maxValuesPerCol[nextX] -= app.sandGrainSize
                app.sand[particle].canDrop = False
                app.sand[particle].canSlide = True
                # set the x velocity to either 1 or -1 in preparation for sliding
                if app.sand[particle].xVelocity != 0:
                    app.sand[particle].xVelocity /= abs(app.sand[particle].xVelocity)
                else:
                    app.sand[particle].xVelocity = 1
            # canDrop starts True, canSlide starts false
            # if canDrop is true:
            else:
                app.sand[particle].drop()
        # elif app.sand[particle].canSlide:
        #     currentX = app.sand[particle].xPos
        #     # slide!
        #     currentMaxValue = app.maxValuesPerCol[currentX]
        #     comparedValue = app.maxValuesPerCol[currentX + app.sand[particle].xVelocity]
        #     print(f'Particle #{particle}: currentX: {currentX}, checkX: {currentX + app.sand[particle].xVelocity} currentMaxValue is {currentMaxValue}, compareValue is {comparedValue}')
        #     if comparedValue > currentMaxValue:
        #         print(f'Particle #{particle}: i done slided')
        #         app.sand[particle].yPos = comparedValue
        #         app.maxValuesPerCol[app.currentX + app.sand[particle].xVelocity] -= 2
        #         app.sand[particle].xPos += app.sand[particle].xVelocity
        #     else:
        #         print(f"Particle #{particle}: i'm done sliding")
        #         app.sand[particle].canSlide = False
        #     # check if it's reached the bottommost point that it can go to; if it is, set canSlide to false
        #     # both should be false at this point

def main():
    runApp(width=600, height=400)

if __name__ == '__main__':
    main()