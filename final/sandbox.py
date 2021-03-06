####################################
# sandbox mode
####################################

from cmu_112_graphics import *
import random
import string
from particleClass import *
import copy

class sandbox(Mode):
    def appStarted(mode):
        mode.sand = [] # a list to keep track of all particle objects
        mode.timerDelay = 5 # put this at 5 when not debugging
        mode.currentX = 0 # the x position of the mouse
        mode.currentY = 0 # the y position of the mouse
        mode.mouseIsPressed = False # boolean flag: is the mouse being held?
        mode.effectiveAppWidth = mode.width # for experimentation purposes: make the window smaller
        mode.effectiveAppHeight = mode.height # for experimentation purposes: make the window smaller
        mode.sandGrainSize = 2 # for experimenation purposes: make the sand actually visible
        # keep track of the highest sand grain particle per column:
        mode.maxValuesPerCol = [mode.effectiveAppHeight // mode.sandGrainSize-1] * (mode.effectiveAppWidth // mode.sandGrainSize)
        # sand grains that are no longer objects and have become part of the background
        mode.Sbackground = mode.loadImage('whiteBackground.png')
        mode.timerIsRunning = True
        mode.currentSandColor = copy.deepcopy(mode.app.sandColor[0])
        mode.betweenColors = True
        mode.rDifference = 0
        mode.gDifference = 0
        mode.bDifference = 0
        mode.counter = 50

    # wipe the canvas
    def resetAll(mode):
        for x in range(mode.width):
            for y in range(mode.height):
                if mode.Sbackground.getpixel((x,y)) != (255,255,255):
                    mode.Sbackground.putpixel((x,y), (255,255,255))
        mode.maxValuesPerCol = [mode.effectiveAppHeight // mode.sandGrainSize-1] * (mode.effectiveAppWidth // mode.sandGrainSize)
        mode.sand = []

    # update the mouse's x and y coordinates, and set the mouseIsPressed boolean to true
    def mousePressed(mode, event):
        mode.mouseIsPressed = True
        mode.currentX, mode.currentY = mode.getCell(event.y, event.x)

    # set the mouseIsPressed boolean to false
    def mouseReleased(mode, event):
        mode.mouseIsPressed = False

    # update the mouse coordinates when moved
    def mouseMoved(mode, event):
        mode.currentX, mode.currentY = mode.getCell(event.y, event.x)

    # also update mouse coordinates when dragged
    def mouseDragged(mode, event):
        mode.currentX, mode.currentY = mode.getCell(event.y, event.x)

    # when the mouse is pressed, create a shower of sand emerging from the point
    # modify here for testing purposes if a single grain is needed instead of a shower
    def addParticles(mode, x, y):
        sandGrainNumber = int(random.triangular(5, 10, 5))
        for i in range(sandGrainNumber):
            colorVar = int(random.triangular(0, 10, 1)) * random.choice([-1, 1])
            signFlip = random.choice([-1, 1])
            xVelocity = int(random.triangular(0, 3, 0.5)) * signFlip
            yVelocity = int(random.random() * 8)
            newParticle = Particle(i, x, y, xVelocity, yVelocity, 
                            mode.currentSandColor, (colorVar,colorVar,colorVar), 
                            mode.effectiveAppHeight, mode.effectiveAppWidth, mode.sandGrainSize)
            mode.sand.append(newParticle)

    # draw all of the sand objects        
    def drawSand(mode, canvas):
        for particle in mode.sand:
            x0,y0,x1,y1 = mode.getCellBounds(particle.row, particle.col)
            canvas.create_rectangle(x0,y0,x1,y1, 
                                    fill=particle.color, width=0)

    # get the coordinates for a specific cell
    def getCellBounds(mode, row, col):
        x0, y0 = col * mode.sandGrainSize, row * mode.sandGrainSize
        x1, y1 = x0 + mode.sandGrainSize, y0 + mode.sandGrainSize
        return x0,y0,x1,y1

    # given an x, y pixel pair, find which cell it belongs to
    def getCell(mode, x, y):
        row = y // mode.sandGrainSize
        col = x // mode.sandGrainSize
        return row, col

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2,  
                            image=ImageTk.PhotoImage(mode.Sbackground))
        canvas.create_rectangle(0, 0, mode.effectiveAppWidth, mode.effectiveAppHeight, outline='white')
        mode.drawSand(canvas)

    # given a certain cell, change the background pixels in that cell to be a color
    def changePixelsGivenCell(mode, row, col, color):
        x0,y0,x1,y1 = mode.getCellBounds(row, col)
        for x in range(x0, x1):
            for y in range(y0, y1):
                mode.Sbackground.putpixel((x,y), color)

    # takes in two colors and determines if they're "almost equal"
    def almostEqual(mode, x, y):
        return (abs(x[0]-y[0]) + abs(x[1]-y[1]) + abs(x[2]-y[2])) < 10 ** -6

    # create the particles
    def timerFired(mode):
        # when the mouse is pressed, create shower of particles
        if mode.mouseIsPressed:
            if len(mode.app.sandColor) > 1:
                mode.counter += 1
            mode.addParticles(mode.currentX, mode.currentY)
            if (len(mode.app.sandColor) > 1 and mode.counter > 200
            and mode.almostEqual(mode.currentSandColor, mode.app.sandColor[1])):
                mode.betweenColors = False
                mode.counter = 0
                mode.app.sandColor[0], mode.app.sandColor[1] = mode.app.sandColor[1], mode.app.sandColor[0]
            elif (len(mode.app.sandColor) > 1 and mode.counter > 200
            and mode.almostEqual(mode.currentSandColor, mode.app.sandColor[0])):
                mode.betweenColors = True
                mode.counter = 0
                mode.app.sandColor[0], mode.app.sandColor[1] = mode.app.sandColor[1], mode.app.sandColor[0]
                
            mode.currentSandColor[0] += mode.rDifference / 400
            mode.currentSandColor[1] += mode.gDifference / 400
            mode.currentSandColor[2] += mode.bDifference / 400
        if mode.timerIsRunning:
            mode.doStep()
        # update the color
        if mode.app.returnedToSandbox:
            mode.currentSandColor = copy.deepcopy(mode.app.sandColor[0])
            mode.app.returnedToSandbox = False
        # if there's a gradient: calculate the rate of change
        if len(mode.app.sandColor) > 1:
            mode.rDifference = mode.app.sandColor[1][0] - mode.app.sandColor[0][0]
            mode.gDifference = mode.app.sandColor[1][1] - mode.app.sandColor[0][1]
            mode.bDifference = mode.app.sandColor[1][2] - mode.app.sandColor[0][2]

    def keyPressed(mode, event):
        # bring up the gradient picker
        if event.key == 'Space':
            mode.app.setActiveMode(mode.app.gradientMode)
            mode.app.gradientModeJustOpened = True
        elif event.key == '0':
            mode.timerIsRunning = not mode.timerIsRunning
        elif event.key == 's':
            mode.doStep()
        # enter returns home
        elif event.key == 'Enter':
            mode.app.setActiveMode(mode.app.splashscreenMode)
        # clear the screen if r is pressed
        elif event.key == 'r':
            mode.resetAll()

    # detects if a particle hit the bottom of the screen
    def particleHitBottom(mode, particle):
        nextY, nextX = particle.getMovePosition()
        if nextX >= mode.effectiveAppWidth // mode.sandGrainSize:
            nextX = mode.effectiveAppWidth // mode.sandGrainSize - 1
        elif nextX < 0:
            nextX = 0
        if nextY > mode.maxValuesPerCol[nextX]: 
            nextY = mode.maxValuesPerCol[nextX]
        x0,y0,x1,y1 = mode.getCellBounds(nextY, nextX)
        if nextY >= mode.effectiveAppHeight // mode.sandGrainSize - 1:
            return True
        return False

    # if a particle hit the bottom, call this function to leave it on the bottom
    # and stop moving
    def leaveParticleOnBottom(mode, particle):
        nextY, nextX = particle.getMovePosition()
        if nextX >= mode.effectiveAppWidth // mode.sandGrainSize:
            nextX = mode.effectiveAppWidth // mode.sandGrainSize - 1
        elif nextX < 0:
            nextX = 0
        if nextY > mode.maxValuesPerCol[nextX]: 
            nextY = mode.maxValuesPerCol[nextX]
        x0,y0,x1,y1 = mode.getCellBounds(nextY, nextX)
        mode.sand.remove(particle)
        mode.changePixelsGivenCell(mode.effectiveAppHeight // mode.sandGrainSize - 1, 
                nextX, (particle.R, particle.G, particle.B))
        mode.maxValuesPerCol[nextX] -= 1
    
    # detects collisions with existing sand
    def collisionDetected(mode, particle):
        nextY, nextX = particle.getMovePosition()
        if nextX >= mode.effectiveAppWidth // mode.sandGrainSize:
            nextX = mode.effectiveAppWidth // mode.sandGrainSize - 1
        elif nextX < 0:
            nextX = 0
        if nextY > mode.maxValuesPerCol[nextX]: 
            nextY = mode.maxValuesPerCol[nextX]
        x0,y0,x1,y1 = mode.getCellBounds(nextY, nextX)
        return mode.Sbackground.getpixel((x0,y1)) != (255,255,255) and not particle.canSlide
    
    # slide!!
    def slide(mode, particle):
        nextY, nextX = particle.getMovePosition()
        if nextX >= mode.effectiveAppWidth // mode.sandGrainSize:
            nextX = mode.effectiveAppWidth // mode.sandGrainSize - 1
        elif nextX < 0:
            nextX = 0
        if nextY > mode.maxValuesPerCol[nextX]: 
            nextY = mode.maxValuesPerCol[nextX]
        x0,y0,x1,y1 = mode.getCellBounds(nextY, nextX)
        
        nextLX = nextX - 1
        nextRX = nextX + 1
        nextSY = nextY + 1
        if nextRX >= mode.effectiveAppWidth // mode.sandGrainSize - 1:
            nextRX = mode.effectiveAppWidth // mode.sandGrainSize - 1
        if nextLX <= 0:
            nextLX = 0
        lx0,ly0,lx1,ly1 = mode.getCellBounds(nextSY, nextLX)
        rx0,ry0,rx1,ry1 = mode.getCellBounds(nextSY, nextRX)
        directions = []
        g = mode.sandGrainSize // 2
        # slide left
        if (nextLX >= 0 and mode.Sbackground.getpixel((lx0+g,ly1-g)) == (255,255,255) and 
            nextSY <= mode.maxValuesPerCol[nextLX]):
            directions.append((nextSY, nextLX))
        # slide right
        if (nextRX < mode.effectiveAppWidth // mode.sandGrainSize and 
            mode.Sbackground.getpixel((rx0+g,ry1-g)) == (255,255,255) and
            nextSY <= mode.maxValuesPerCol[nextRX]):
            directions.append((nextSY, nextRX))
        # if it can't do either, stay in place
        if len(directions) == 0:
            mode.changePixelsGivenCell(nextY, nextX, (particle.R, particle.G, particle.B))
            mode.maxValuesPerCol[nextX] -= 1
            mode.sand.remove(particle)
            shouldContinue = False
        # pick a random direction to slide:
        else:
            randomIndex = random.choice(directions)
            particle.row, particle.col = nextSY, randomIndex[1]
            particle.yVelocity = 1
            particle.xVelocity = 0
    
    def doStep(mode):
        i = 0
        while i < len(mode.sand):
            particle = mode.sand[i]
            shouldContinue = True
            # the sand hit the bottom! remove the particle and color the background
            if mode.particleHitBottom(particle):
                shouldContinue = False
                mode.leaveParticleOnBottom(particle)
                continue
            # the sand hit other sand! it's okay to slide now
            elif mode.collisionDetected(particle): 
                particle.canSlide = True
            # the particle is able to slide, so do it
            if particle.canSlide:
                mode.slide(particle)
            # didn't hit anything; just go ahead and keep moving
            if not particle.canSlide:
                particle.drop()
            if shouldContinue:
                i += 1