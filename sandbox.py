####################################
# sandbox mode
####################################

from cmu_112_graphics import *
import random
import time
import string
from particleClass import *

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

class sandbox(Mode):
    def appStarted(mode):
        mode.sand = [] # a list to keep track of all particle objects
        mode.timerDelay = 10 # put this at 10 when not debugging
        mode.currentX = 0 # the x position of the mouse
        mode.currentY = 0 # the y position of the mouse
        mode.mouseIsPressed = False # boolean flag: is the mouse being held?
        mode.effectiveAppWidth = mode.width # for debugging purposes: make the window smaller
        mode.effectiveAppHeight = mode.height # for debugging purposes: make the window smaller
        mode.sandGrainSize = 2 # make the sand actually visible
        mode.Sbackground = mode.loadImage('whiteBackground.png')
        mode.timerIsRunning = True # for debugging: run timer/don't by pressing 0
        mode.shouldContinue = True # this is NOT for debugging! DO NOT DELETE

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
                            mode.app.sandColor, (colorVar,colorVar,colorVar), 
                            mode.effectiveAppHeight, mode.effectiveAppWidth, mode.sandGrainSize)
            mode.sand.append(newParticle)

    # draw all of the sand objects        
    def drawSand(mode, canvas):
        for particle in mode.sand:
            x0,y0,x1,y1 = mode.getCellBounds(particle.row, particle.col)
            canvas.create_rectangle(x0,y0,x1,y1, 
                                    fill=particle.color, width=0)

    def getCellBounds(mode, row, col):
        x0, y0 = col * mode.sandGrainSize, row * mode.sandGrainSize
        x1, y1 = x0 + mode.sandGrainSize, y0 + mode.sandGrainSize
        return x0,y0,x1,y1

    def getCell(mode, x, y):
        row = y // mode.sandGrainSize
        col = x // mode.sandGrainSize
        return row, col

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2,  
                            image=ImageTk.PhotoImage(mode.Sbackground))
        canvas.create_rectangle(0, 0, mode.effectiveAppWidth, mode.effectiveAppHeight, outline='black')
        mode.drawSand(canvas)

    # given a certain cell, change the background pixels in that cell to be a color
    def changePixelsGivenCell(mode, row, col, color):
        x0,y0,x1,y1 = mode.getCellBounds(row, col)
        for x in range(x0, x1):
            for y in range(y0, y1):
                mode.Sbackground.putpixel((x,y), color)

    # create the particles
    def timerFired(mode):
        # when the mouse is pressed, create shower of particles
        if mode.mouseIsPressed:
            mode.addParticles(mode.currentX, mode.currentY)
        if mode.timerIsRunning:
            mode.doStep()

    def keyPressed(mode, event):
        if event.key == 'Space':
            mode.app.setActiveMode(mode.app.gradientMode)
        elif event.key == '0':
            mode.timerIsRunning = not mode.timerIsRunning
        elif event.key == 's':
            mode.doStep()
        elif event.key == 'Enter':
            mode.app.setActiveMode(mode.app.splashscreenMode)

    def slide(mode, particle):
        row, col = particle.row, particle.col
        lrow, lcol = particle.row+1, particle.col-1
        rrow, rcol = particle.row+1, particle.col+1
        directions = []

        bottomRow = mode.effectiveAppHeight // mode.sandGrainSize - 1
        rightMostCol = mode.effectiveAppWidth // mode.sandGrainSize - 1

        if lcol < 0:
            lcol = 0
        if rcol > rightMostCol:
            rcol = rightMostCol
        if lrow > bottomRow:
            lrow = bottomRow
        if rrow > bottomRow:
            rrow = bottomRow

        if not mode.cellIsOccupied(lrow, lcol):
            directions.append((lrow, lcol))
        if not mode.cellIsOccupied(rrow, rcol):
            directions.append((rrow, rcol))
        
        if len(directions) == 0:
            mode.changePixelsGivenCell(row, col, (particle.R, particle.G, particle.B))
            mode.sand.remove(particle)
            mode.shouldContinue = False
        # pick a random direction to slide:
        else:
            randomDirection = random.choice(directions)
            particle.row, particle.col = randomDirection
            particle.yVelocity = 1
            particle.xVelocity = 0
        
    def cellIsOccupied(mode, row, col):
        g = mode.sandGrainSize // 2
        x0,y0,x1,y1 = mode.getCellBounds(row, col)
        print(f'x0+g, y1-g: ({x0+g}, {y1-g})')
        return mode.Sbackground.getpixel((x0+g,y1-g)) != (255,255,255)

    def sandIsOnOtherSand(mode, particle):
        row, col = particle.row, particle.col
        newRow, newCol = row+1, col
        largestRow = mode.effectiveAppHeight // mode.sandGrainSize - 1
        if newRow > largestRow:
            newRow = largestRow
        return mode.cellIsOccupied(newRow, newCol)

    def collisionDetected(mode, particle):
        nextRow, nextCol = particle.getMovePosition()
        rightMostCol = mode.effectiveAppWidth // mode.sandGrainSize - 1
        if nextCol > rightMostCol:
            nextCol = rightMostCol
        elif nextCol < 0:
            nextCol = 0
        maxRowValue = mode.getMaxRowValue(particle.row, nextCol)
        print(f'maxRowValue:{maxRowValue}')
        return nextRow >= maxRowValue #################### if doesn't work, change >= to >

    def getMaxRowValue(mode, startRowValue, col):
        maxRowValue = startRowValue
        print(f'maxRowValue: {maxRowValue}')
        while (maxRowValue < mode.effectiveAppHeight // mode.sandGrainSize and
                not mode.cellIsOccupied(maxRowValue, col)):
            maxRowValue += 1
        return maxRowValue - 1

    def hitBottom(mode, particle):
        nextRow, nextCol = particle.getMovePosition()
        rightMostCol = mode.effectiveAppWidth // mode.sandGrainSize - 1
        if nextCol > rightMostCol:
            nextCol = rightMostCol
        elif nextCol < 0:
            nextCol = 0
        bottomRow = mode.effectiveAppHeight // mode.sandGrainSize - 1
        return nextRow > bottomRow and not mode.cellIsOccupied(bottomRow, nextCol)

    def doStep(mode):
        i = 0
        while i < len(mode.sand):
            g = mode.sandGrainSize // 2 # used for getting pixel color of a cell
            particle = mode.sand[i]          
            mode.shouldContinue = True

            print(f"particle's current position (row, col): {particle.row}, {particle.col}")
            print(f"next position (row, col): {particle.getMovePosition()}")

            # check if the sand is sitting on top of something. if it is, call the slide function:
                # slide: slides the sand if it can slide, if not, colors the background 
            if mode.sandIsOnOtherSand(particle):
                print('particle is sliding/not sliding')
                mode.slide(particle)
            
            # did it hit the bottom?
            elif mode.hitBottom(particle):
                print('the particle hit the bottom')
                nextRow, nextCol = particle.getMovePosition()
                rightMostCol = mode.effectiveAppWidth // mode.sandGrainSize - 1
                if nextCol > rightMostCol:
                    nextCol = rightMostCol
                elif nextCol < 0:
                    nextCol = 0
                bottomRow = mode.effectiveAppHeight // mode.sandGrainSize - 1
                mode.changePixelsGivenCell(bottomRow, nextCol, 
                                        (particle.R, particle.G, particle.B))
                mode.sand.remove(particle)
                mode.shouldContinue = False

            # if it's going to collide with something or reaches the bottom, sit at a legal spot
            elif mode.collisionDetected(particle):
                print('collision detected')
                nextRow, nextCol = particle.getMovePosition()
                if nextCol >= mode.effectiveAppWidth // mode.sandGrainSize:
                    nextCol = mode.effectiveAppWidth // mode.sandGrainSize - 1
                maxRow = mode.getMaxRowValue(particle.row, nextCol)
                print(f'maxRow: {maxRow}')
                particle.row = maxRow
                particle.col = nextCol

            # otherwise, just keep moving
            else:
                print('particle dropped')
                particle.drop()

            if mode.shouldContinue:
                i += 1