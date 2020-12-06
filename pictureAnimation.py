#####################################
# computer animation mode
#####################################

from cmu_112_graphics import *
import random
import time
import string
from particleClass import *

class animationMode(Mode):
    def appStarted(mode):
        mode.sand = [] # a list to keep track of all particle objects
        mode.timerDelay = 5 # put this at 5 when not debugging
        mode.effectiveAppWidth = mode.width # for experimentation purposes: make the window smaller
        mode.effectiveAppHeight = mode.height # for experimentation purposes: make the window smaller
        mode.sandGrainSize = 2 # for experimenation purposes: make the sand actually visible
        mode.currentX = 0 # the x position of sand dispensing spot
        mode.currentY = mode.effectiveAppHeight // mode.sandGrainSize - 20 # the y position of sand dispensing spot
        # keep track of the highest sand grain particle per column:
        mode.maxValuesPerCol = [mode.effectiveAppHeight // mode.sandGrainSize-1] * (mode.effectiveAppWidth // mode.sandGrainSize)
        # sand grains that are no longer objects and have become part of the background
        mode.screenBackground = mode.loadImage('whiteBackground.png') # start with a blank screen
        mode.targetImage = mode.loadImage(mode.app.imageName) # the desired image to recreate
        mode.direction = 1 # is the computer going left --> right, or right --> left?
        mode.dispenseSand = True # once arrived at the top, don't dispense sand anymore
        mode.sandColor = (0,0,0) # keep track of sand color
        mode.timerIsRunning = True

    # create a shower of sand emerging from the point
    # modify here for testing purposes if a single grain is needed instead of a shower
    def addParticles(mode, x, y):
        sandGrainNumber = int(random.triangular(5, 7, 5))
        for i in range(sandGrainNumber):
            colorVar = int(random.triangular(0, 10, 1)) * random.choice([-1, 1])
            signFlip = random.choice([-1, 1])
            xVelocity = int(random.triangular(0, 2, 0)) * signFlip
            yVelocity = int(random.random() * 8)
            newParticle = Particle(i, x, y, xVelocity, yVelocity, 
                            mode.sandColor, (colorVar,colorVar,colorVar), 
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
                            image=ImageTk.PhotoImage(mode.screenBackground))
        canvas.create_rectangle(0, 0, mode.effectiveAppWidth, mode.effectiveAppHeight, outline='white')
        mode.drawSand(canvas)

    # given a certain cell, change the background pixels in that cell to be a color
    def changePixelsGivenCell(mode, row, col, color):
        x0,y0,x1,y1 = mode.getCellBounds(row, col)
        for x in range(x0, x1):
            for y in range(y0, y1):
                mode.screenBackground.putpixel((x,y), color)

    # create the particles
    def timerFired(mode):
        # create shower of particles from the dispensing spot
        if mode.timerIsRunning:
            mode.doStep()
        # go through each active particle and move it accordingly

    def keyPressed(mode, event):
        if event.key == '0':
            mode.timerIsRunning = not mode.timerIsRunning
        elif event.key == 's':
            mode.doStep()
        elif event.key == 'Enter':
            mode.app.setActiveMode(mode.app.splashscreenMode)

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
    
    def collisionDetected(mode, particle):
        nextY, nextX = particle.getMovePosition()
        if nextX >= mode.effectiveAppWidth // mode.sandGrainSize:
            nextX = mode.effectiveAppWidth // mode.sandGrainSize - 1
        elif nextX < 0:
            nextX = 0
        if nextY > mode.maxValuesPerCol[nextX]: 
            nextY = mode.maxValuesPerCol[nextX]
        x0,y0,x1,y1 = mode.getCellBounds(nextY, nextX)
        return mode.screenBackground.getpixel((x0,y1)) != (255,255,255) and not particle.canSlide
    
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
        if (nextLX >= 0 and mode.screenBackground.getpixel((lx0+g,ly1-g)) == (255,255,255) and 
            nextSY <= mode.maxValuesPerCol[nextLX]):
            directions.append((nextSY, nextLX))
        # slide right
        if (nextRX < mode.effectiveAppWidth // mode.sandGrainSize and 
            mode.screenBackground.getpixel((rx0+g,ry1-g)) == (255,255,255) and
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
        g = mode.sandGrainSize // 2
        if mode.dispenseSand:
            print(f'currentX: {mode.currentX}')
            x0,y0,x1,y1 = mode.getCellBounds(mode.maxValuesPerCol[mode.currentX-1], mode.currentX)
            print(f'x0,y0,x1,y1: {x0}, {y0}, {x1}, {y1}')
            mode.sandColor = mode.targetImage.getpixel((x0+g, y1-g))    
            mode.addParticles(mode.currentX, mode.currentY) #######################################
            mode.currentX += 2 * mode.direction
            if mode.currentX >= mode.effectiveAppWidth // mode.sandGrainSize:
                mode.currentX = mode.effectiveAppWidth // mode.sandGrainSize - 1
                mode.currentY -= 3
                mode.direction = -1 * mode.direction
            elif mode.currentX < 0:
                mode.currentX = 0
                mode.currentY -= 3
                mode.direction = -1 * mode.direction
            if mode.currentY < 0:
                mode.currentY = 0

        if min(mode.maxValuesPerCol) < 2:
            mode.dispenseSand = False
        
        # sand related things:
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