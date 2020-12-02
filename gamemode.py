###################################
# game mode
###################################

from cmu_112_graphics import *
import random
import string
from particleClass import *

def getLinePoints(x0,y0,x1,y1):
    didSwitch = False
    # if the line is vertical:
    if y1 > y0 and x0 == x1:
        return [(x0, y0+i) for i in range(y1-y0+1)]
    elif y0 > y1 and x0 == x1:
        return [(x0, y1+i) for i in range(y0-y1+1)]
    # check to see if the slope is greater than 1:
    if abs(y1-y0) > abs(x1-x0):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        didSwitch = True
    # if the line is being drawn from right --> left
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    slope = (y1-y0)/(x1-x0)
    dError = abs(slope)
    yStep = 1
    if y0 > y1:
        yStep = -1
    error = 0
    y = y0
    result = []
    for x in range(x0,x1+1):
        if didSwitch:
            result.append((y,x))
        else:
            result.append((x,y))
        error += dError
        if error >= 0.5:
            y += yStep
            error -= 1
    return result

class game(Mode):
    def appStarted(mode):
        mode.sand = [] # a list to keep track of all particle objects
        mode.timerDelay = 5 # put this at 5 when not debugging
        mode.mouseMovedDelay = 5 # put this at 1 for line drawing purposes
        mode.mouseX, mode.mouseY = 0, 0 # keep track of current mouse coordinates
        mode.oldMouseX, mode.oldMouseY = 0, 0 # keep track of old mouse coordinates
        mode.spaceIsPressed = False # boolean flag: is the mouse being held?
        mode.effectiveAppWidth = mode.width # for experimentation purposes: make the window smaller
        mode.effectiveAppHeight = mode.height # for experimentation purposes: make the window smaller
        mode.sandGrainSize = 2 # for experimenation purposes: make the sand actually visible
        mode.sandX = 25 # where is the sand being dispensed from?
        mode.sandY = 25 # see above
        mode.gameBackground = mode.loadImage('whiteBackground.png')
        mode.timerIsRunning = True # for debugging: run timer/don't by pressing 0
        mode.shouldContinue = True # this is NOT for debugging! DO NOT DELETE
        mode.canDraw = True

    def mousePressed(mode, event):
        mode.mouseX, mode.mouseY = event.x, event.y

    def mouseDragged(mode, event):
        if mode.canDraw:
            mode.oldMouseX, mode.oldMouseY = mode.mouseX, mode.mouseY
            mode.mouseX, mode.mouseY = event.x, event.y
            linePoints = getLinePoints(mode.oldMouseX, mode.oldMouseY, mode.mouseX, mode.mouseY)
            for x, y in linePoints:
                for horizontal in range(x-1, x+2):
                    for vertical in range(y-1, y+2):
                        mode.gameBackground.putpixel((horizontal,vertical),(0,0,0))

    def changePixelsGivenCell(mode, row, col, color):
        x0,y0,x1,y1 = mode.getCellBounds(row, col)
        for x in range(x0, x1):
            for y in range(y0, y1):
                mode.gameBackground.putpixel((x,y), color)

    # when the mouse is pressed, create a shower of sand emerging from the point
    # modify here for testing purposes if a single grain is needed instead of a shower
    def addParticles(mode, x, y):
        sandGrainNumber = int(random.triangular(5, 10, 5))
        for i in range(sandGrainNumber):
            colorVar = int(random.triangular(0, 15, 1)) * random.choice([-1, 1])
            signFlip = random.choice([-1, 1])
            xVelocity = int(random.triangular(0, 3, 0.5)) * signFlip
            yVelocity = int(random.random() * 8)
            newParticle = Particle(i, x, y, xVelocity, yVelocity, 
                            (100, 100, 255), (colorVar,colorVar,colorVar), 
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
                            image=ImageTk.PhotoImage(mode.gameBackground))
        mode.drawSand(canvas)

    # create the particles
    def timerFired(mode):
        # when space is pressed, dispense the particles
        if mode.spaceIsPressed:
            mode.addParticles(mode.sandX, mode.sandY)
        mode.doStep()

    def keyPressed(mode, event):
        if event.key == 'Space':
            mode.spaceIsPressed = not mode.spaceIsPressed
            mode.canDraw = False
        elif event.key == 'Enter':
            mode.app.setActiveMode(mode.app.splashscreenMode)
        elif event.key == '0':
            mode.timerIsRunning = not mode.timerIsRunning
        elif event.key == 's':
            mode.doStep()

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
        return mode.gameBackground.getpixel((x0+g,y1-g)) != (255,255,255)

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