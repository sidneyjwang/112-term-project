from cmu_112_graphics import *
import random
import time
import string

####################################
# this isn't sand
####################################

# this project uses cmu-112-graphics, which was taken from
# https://www.cs.cmu.edu/~112/

# from the 112 course website:
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

# takes in a rgbString and converts it to RGB
def rgbStringtoRGB(rgbString):
    red1 = convertHexDigitToBaseTen(rgbString[1])
    red2 = convertHexDigitToBaseTen(rgbString[2])
    green1 = convertHexDigitToBaseTen(rgbString[3])
    green2 = convertHexDigitToBaseTen(rgbString[4])
    blue1 = convertHexDigitToBaseTen(rgbString[5])
    blue2 = convertHexDigitToBaseTen(rgbString[6])
    print(red1,red2,green1,green2,blue1,blue2)
    return (red2 + 16*red1, green2 + 16*green1, blue2 + 16*blue1)

# helper function for rgbStringtoRGB    
def convertHexDigitToBaseTen(digit):
    if digit in string.digits:
        return int(digit)
    else:
        return string.ascii_lowercase.find(digit) + 10

def appStarted(app):
    app.sand = [] # a list to keep track of all particle objects
    app.timerDelay = 5 # put this at 5 when not debugging
    app.currentX = 0 # the x position of the mouse
    app.currentY = 0 # the y position of the mouse
    app.mouseIsPressed = False # boolean flag: is the mouse being held?
    app.effectiveAppWidth = app.width # for experimentation purposes: make the window smaller
    app.effectiveAppHeight = app.height # for experimentation purposes: make the window smaller
    app.sandGrainSize = 2 # for experimenation purposes: make the sand actually visible
    # keep track of the highest sand grain particle per column:
    app.maxValuesPerCol = [app.effectiveAppHeight // app.sandGrainSize-1] * (app.effectiveAppWidth // app.sandGrainSize)
    # sand grains that are no longer objects and have become part of the background
    app.background = app.loadImage('blacktestbackground.png')

    app.leftcounter = 0
    app.rightcounter = 0
    app.timerIsRunning = False

class Particle:
    GRAVITY = 1.5
    MAX_VELOCITY = 15
    HEIGHT = 0
    WIDTH = 0
    TOTAL_PARTICLES = 0
    PARTICLE_SIZE = 2
    def __init__(self, particleNumber, col, row, xVelocity, yVelocity, intendedColor, 
                colorVariation, height, width, particleSize=2):
        self.particleNumber = particleNumber
        self.col = col
        self.row = row
        self.yVelocity = yVelocity
        self.time = 0
        self.xVelocity = xVelocity
        self.R = intendedColor[0] + colorVariation[0]
        self.G = intendedColor[1] + colorVariation[1]
        self.B = intendedColor[1] + colorVariation[2]
        if self.R > 255: self.R = 255
        elif self.R < 0: self.R = 0
        if self.G > 255: self.G = 255
        elif self.G < 0: self.G = 0
        if self.B > 255: self.B = 255
        elif self.B < 0: self.B = 0
        self.color = rgbString(self.R, self.G, self.B)
        self.canSlide = False
        Particle.HEIGHT = height
        Particle.WIDTH = width
        Particle.TOTAL_PARTICLES += 1
        Particle.PARTICLE_SIZE = particleSize

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
        if self.row >= Particle.HEIGHT // Particle.PARTICLE_SIZE:
            self.row = Particle.HEIGHT // Particle.PARTICLE_SIZE - 1
            self.yVelocity = 0
        # revisit once sand piling starts:
        if self.col >= Particle.WIDTH // Particle.PARTICLE_SIZE:
            self.col = Particle.WIDTH // Particle.PARTICLE_SIZE - 1
            self.xVelocity = 0
        elif self.col < 0:
            self.col = 0
            self.xVelocity = 0

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
        xVelocity = int(random.triangular(0, 3, 0.5)) * signFlip
        yVelocity = int(random.random() * 8)
        newParticle = Particle(i, x, y, xVelocity, yVelocity, 
                        (255,100,100), (rVar,gVar,bVar), app.effectiveAppHeight, 
                        app.effectiveAppWidth, app.sandGrainSize)
        app.sand.append(newParticle)

# draw all of the sand objects        
def drawSand(app, canvas):
    for particle in app.sand:
        x0,y0,x1,y1 = getCellBounds(app, particle.row, particle.col)
        canvas.create_rectangle(x0,y0,x1,y1, 
                                fill=particle.color, width=0)

def getCellBounds(app, row, col):
    x0, y0 = col * app.sandGrainSize, row * app.sandGrainSize
    x1, y1 = x0 + app.sandGrainSize, y0 + app.sandGrainSize
    return x0,y0,x1,y1

def getCell(app, x, y):
    row = y // app.sandGrainSize
    col = x // app.sandGrainSize
    return row, col

def redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2,  
                        image=ImageTk.PhotoImage(app.background))
    canvas.create_rectangle(0, 0, app.effectiveAppWidth, app.effectiveAppHeight, outline='white')
    drawSand(app, canvas)

# given a certain cell, change the background pixels in that cell to be a color
def changePixelsGivenCell(app, row, col, color):
    x0,y0,x1,y1 = getCellBounds(app, row, col)
    for x in range(x0, x1):
        for y in range(y0, y1):
            app.background.putpixel((x,y), color)

# create the particles
def timerFired(app):
    # when the mouse is pressed, create shower of particles
    if app.mouseIsPressed:
        addParticles(app, app.currentX, app.currentY)
    if app.timerIsRunning:
        doStep(app)
    # go through each active particle and move it accordingly

def keyPressed(app, event):
    if event.key == 's':
        doStep(app)
    if event.key == 'Space':
        app.timerIsRunning = not app.timerIsRunning

def doStep(app):
    i = 0
    while i < len(app.sand):
        particle = app.sand[i]
        shouldContinue = True
        nextX, nextY = particle.getMovePosition()
        if nextX >= app.effectiveAppWidth // app.sandGrainSize:
            nextX = app.effectiveAppWidth // app.sandGrainSize - 1
        elif nextX < 0:
            nextX = 0
        if nextY > app.maxValuesPerCol[nextX]: 
            nextY = app.maxValuesPerCol[nextX]
        x0,y0,x1,y1 = getCellBounds(app, nextY, nextX)
        # the sand hit the bottom! remove the particle and color the background
        if nextY >= app.effectiveAppHeight // app.sandGrainSize - 1:
            print('hit bottom') 
            app.sand.remove(particle)
            shouldContinue = False
            changePixelsGivenCell(app, app.effectiveAppHeight // app.sandGrainSize - 1, 
                    nextX, (100,100,255))
            app.maxValuesPerCol[nextX] -= 1
            continue
        # the sand hit other sand! it's okay to slide now
        elif app.background.getpixel((x0,y1)) != (0,0,0) and particle.canSlide == False: 
            print('ready to slide!')
            particle.canSlide = True
        # the particle is able to slide
        if particle.canSlide:
            print('entering the canSlide if statement...')
            nextLX = nextX - 1
            nextRX = nextX + 1
            nextSY = nextY + 1
            if nextRX >= app.effectiveAppWidth // app.sandGrainSize - 1:
                nextRX = app.effectiveAppWidth // app.sandGrainSize - 1
            if nextLX <= 0:
                nextLX = 0
            print(f'row, col: {particle.row}, {particle.col}')
            print(f'nextY, nextX: {nextY}, {nextX}')
            print(f'nextRow, nextLCol, nextRCol: {nextSY}, {nextLX}, {nextRX}')
            lx0,ly0,lx1,ly1 = getCellBounds(app, nextSY, nextLX)
            rx0,ry0,rx1,ry1 = getCellBounds(app, nextSY, nextRX)
            directions = []
            g = app.sandGrainSize // 2
            print(f'lx0+1, ly1-1: {lx0+1}, {ly1-1}')
            print(f'rx0+1, ry1-1: {rx0+1}, {ry1-1}')
            print(f'left pixel value: {app.background.getpixel((lx0+g,ly1-g))}')
            print(f'right pixel value: {app.background.getpixel((rx0+g,ry1-g))}')
            print(f'length of app.sand: {len(app.sand)}')
            if (nextLX >= 0 and app.background.getpixel((lx0+g,ly1-g)) == (0,0,0) and 
                nextSY <= app.maxValuesPerCol[nextLX]):
                print('slide left!')
                directions.append((nextSY, nextLX))
            # if rightposition doesn't move out of grid and isn't occupied: move there
            if (nextRX < app.effectiveAppWidth // app.sandGrainSize and 
                app.background.getpixel((rx0+g,ry1-g)) == (0,0,0) and
                nextSY <= app.maxValuesPerCol[nextRX]):
                print('slide right!')
                directions.append((nextSY, nextRX))
            # otherwise: stay and stack
            if len(directions) == 0:
                print('no slide')
                changePixelsGivenCell(app, nextY, nextX, (100,100,255))
                app.maxValuesPerCol[nextX] -= 1
                app.sand.remove(particle)
                shouldContinue = False
            # slide!
            else:
                randomIndex = random.choice(directions)
                particle.row, particle.col = nextSY, randomIndex[1]
                particle.yVelocity = 1
                particle.xVelocity = 0
        # didn't hit anything; just go ahead and keep moving
        if not particle.canSlide:
            particle.drop()
            print('particle dropped')
        if shouldContinue:
            i += 1

runApp(width=600, height=400)