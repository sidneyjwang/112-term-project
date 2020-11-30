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
        mode.sandX = 0 # where is the sand being dispensed from?
        mode.sandY = 0 # see above
        # keep track of the highest sand grain particle per column:
        mode.maxValuesPerCol = [mode.effectiveAppHeight // mode.sandGrainSize-1] * (mode.effectiveAppWidth // mode.sandGrainSize)
        # sand grains that are no longer objects and have become part of the background
        mode.gameBackground = mode.loadImage('whiteBackground.png')
        mode.canDraw = True

    def mousePressed(mode, event):
        mode.mouseX, mode.mouseY = event.x, event.y

    def mouseDragged(mode, event):
        if mode.canDraw:
            mode.oldMouseX, mode.oldMouseY = mode.mouseX, mode.mouseY
            mode.mouseX, mode.mouseY = event.x, event.y
            linePoints = getLinePoints(mode.oldMouseX, mode.oldMouseY, mode.mouseX, mode.mouseY)
            for x, y in linePoints:
                row, col = mode.getCell(x,y)
                currentMax = mode.maxValuesPerCol[col]
                if row < currentMax:
                    mode.maxValuesPerCol[col] = row
                print(f'row, col: {row}, {col}')
                print(f'col, maxRowValue: {col}, {mode.maxValuesPerCol[col]}')
                for horizontal in range(x-1, x+2):
                    for vertical in range(y-1, y+2):
                        mode.gameBackground.putpixel((horizontal,vertical),(0,0,0))

    # when the mouse is pressed, create a shower of sand emerging from the point
    # modify here for testing purposes if a single grain is needed instead of a shower
    def addParticles(mode, x, y):
        sandGrainNumber = int(random.triangular(3, 5, 3))
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

    # given a certain cell, change the background pixels in that cell to be a color
    def changePixelsGivenCell(mode, row, col, color):
        x0,y0,x1,y1 = mode.getCellBounds(row, col)
        for x in range(x0, x1):
            for y in range(y0, y1):
                mode.gameBackground.putpixel((x,y), color)

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

    def doStep(mode):
        i = 0
        while i < len(mode.sand):
            particle = mode.sand[i]
            shouldContinue = True
            nextX, nextY = particle.getMovePosition()
            if nextX >= mode.effectiveAppWidth // mode.sandGrainSize:
                nextX = mode.effectiveAppWidth // mode.sandGrainSize - 1
            elif nextX < 0:
                nextX = 0
            if nextY > mode.maxValuesPerCol[nextX]: 
                nextY = mode.maxValuesPerCol[nextX]
            x0,y0,x1,y1 = mode.getCellBounds(nextY, nextX)
            # the sand hit the bottom! remove the particle and color the background
            if nextY >= mode.effectiveAppHeight // mode.sandGrainSize - 1:
                mode.sand.remove(particle)
                shouldContinue = False
                mode.changePixelsGivenCell(mode.effectiveAppHeight // mode.sandGrainSize - 1, 
                        nextX, (particle.R, particle.G, particle.B))
                mode.maxValuesPerCol[nextX] -= 1
                continue
            
            # the sand hit other sand! it's okay to slide now
            elif mode.gameBackground.getpixel((x0,y1)) != (255,255,255) and particle.canSlide == False: 
                particle.canSlide = True
            # the particle is able to slide
            if particle.canSlide:
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
                if (nextLX >= 0 and mode.gameBackground.getpixel((lx0+g,ly1-g)) == (255,255,255) and 
                    nextSY <= mode.maxValuesPerCol[nextLX]):
                    directions.append((nextSY, nextLX))
                # slide right
                if (nextRX < mode.effectiveAppWidth // mode.sandGrainSize and 
                    mode.gameBackground.getpixel((rx0+g,ry1-g)) == (255,255,255) and
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
            # didn't hit anything; just go ahead and keep moving
            if not particle.canSlide:
                particle.drop()
            if shouldContinue:
                i += 1