####################################
# recreation mode
####################################

from cmu_112_graphics import *
import random
import string
from particleClass import *

class recreationMode(Mode):
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
        mode.Rbackground = mode.loadImage('whiteBackground.png') # for the user
        mode.targetImage = mode.loadImage(mode.app.imageName) # what the user should recreate
        mode.timerIsRunning = True 
        mode.shouldScore = False # display the score?
        mode.scoreNumber = 0 # keep track of the score

    # calculate the score by scoring each cell if not blank and then averaging
    def score(mode):
        result = []
        for row in range(mode.effectiveAppHeight // 20):
            for col in range(mode.effectiveAppWidth // 20):
                if mode.scoreCell(row, col) != None and mode.scoreCell(row, col) < .95:
                    result.append(mode.scoreCell(row, col))
        print(result)
        mode.scoreNumber = sum(result) * 100 // len(result)
        mode.scoreNumber = int(mode.scoreNumber)
    
    # calculate the score for one individual "cell"
    def scoreCell(mode, row, col):
        expectedTotalR, expectedTotalG, expectedTotalB = 0,0,0
        userTotalR, userTotalG, userTotalB = 0,0,0
        startXPixel = col * 20
        startYPixel = row * 20
        # get the expected rgb values
        for x in range(startXPixel, startXPixel + 20):
            for y in range(startYPixel, startYPixel + 20):
                color = mode.targetImage.getpixel((x,y))
                expectedTotalR += color[0]
                expectedTotalG += color[1]
                expectedTotalB += color[2]
        # get the actual rgb values that the user made
        for x in range(startXPixel, startXPixel + 20):
            for y in range(startYPixel, startYPixel + 20):
                color = mode.Rbackground.getpixel((x,y))
                userTotalR += color[0]
                userTotalG += color[1]
                userTotalB += color[2]
        # calculate the difference between expected and actual
        rDiff = abs(userTotalR - expectedTotalR) // (400)
        gDiff = abs(userTotalG - expectedTotalG) // (400)
        bDiff = abs(userTotalB - expectedTotalB) // (400)
        # any blank cells don't count towards the score
        if (expectedTotalR == 0 and expectedTotalG == 0 and expectedTotalB == 0
            and userTotalR == 0 and userTotalG == 0 and userTotalB == 0):
            return None
        print(f'red: {rDiff}, green: {gDiff}, blue:{bDiff}')
        finalAverage = 1 - ((rDiff + gDiff + bDiff) / (400))**2
        return finalAverage

    # display the score once finished
    def drawScore(mode, canvas):
        canvas.create_text(mode.width / 2, mode.height / 2, 
                            text=f'Your score is: {mode.scoreNumber}',
                            font=('Avenir', 30, 'bold'))
                            
    ######################################
    # sand related things
    ######################################

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
                            image=ImageTk.PhotoImage(mode.Rbackground))
        canvas.create_rectangle(0, 0, mode.effectiveAppWidth, mode.effectiveAppHeight, outline='white')
        mode.drawSand(canvas)
        if mode.shouldScore and not mode.mouseIsPressed:
            mode.drawScore(canvas)

    # given a certain cell, change the background pixels in that cell to be a color
    def changePixelsGivenCell(mode, row, col, color):
        x0,y0,x1,y1 = mode.getCellBounds(row, col)
        for x in range(x0, x1):
            for y in range(y0, y1):
                mode.Rbackground.putpixel((x,y), color)

    # create the particles
    def timerFired(mode):
        # when the mouse is pressed, create shower of particles
        if mode.mouseIsPressed:
            mode.addParticles(mode.currentX, mode.currentY)
            mode.shouldScore = False
        if mode.timerIsRunning:
            mode.doStep()
        # go through each active particle and move it accordingly

    def keyPressed(mode, event):
        if event.key == 'Space':
            mode.app.setActiveMode(mode.app.recreationGradientMode)
        elif event.key == '0':
            mode.timerIsRunning = not mode.timerIsRunning
        elif event.key == 'm':
            mode.doStep()
        elif event.key == 'Enter':
            mode.app.setActiveMode(mode.app.splashscreenMode)
        elif event.key == 's':
            mode.score()
            mode.shouldScore = True

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
        return mode.Rbackground.getpixel((x0,y1)) != (255,255,255) and not particle.canSlide
    
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
        if (nextLX >= 0 and mode.Rbackground.getpixel((lx0+g,ly1-g)) == (255,255,255) and 
            nextSY <= mode.maxValuesPerCol[nextLX]):
            directions.append((nextSY, nextLX))
        # slide right
        if (nextRX < mode.effectiveAppWidth // mode.sandGrainSize and 
            mode.Rbackground.getpixel((rx0+g,ry1-g)) == (255,255,255) and
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