###################################
# game mode
###################################

from cmu_112_graphics import *
import random
import string
from particleClass import *
from goalClass import *

def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

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

def distance(x0,y0,x1,y1):
    return ((x0-x1)**2 + (y0-y1)**2) ** 0.5

class game(Mode):
    def appStarted(mode):
        mode.sand = [] # a list to keep track of all particle objects
        mode.timerDelay = 5 # put this at 5 when not debugging
        mode.mouseMovedDelay = 10 # put this at 1 for line drawing purposes
        mode.mouseX, mode.mouseY = 0, 0 # keep track of current mouse coordinates
        mode.oldMouseX, mode.oldMouseY = 0, 0 # keep track of old mouse coordinates
        mode.effectiveAppWidth = mode.width # for experimentation purposes: make the window smaller
        mode.effectiveAppHeight = mode.height # for experimentation purposes: make the window smaller
        mode.sandGrainSize = 2 # for experimenation purposes: make the sand actually visible
        mode.gameBackground = mode.loadImage('whiteBackground.png')
        mode.timerIsRunning = True # for debugging: run timer/don't by pressing 0
        mode.shouldContinue = True # this is NOT for debugging! DO NOT DELETE
        mode.goalImages = [mode.loadImage('bluebucket.png'), mode.loadImage('pinkbucket.png'),
                            mode.loadImage('purplebucket.png')] # load bucket pngs
        mode.funnel = mode.loadImage('funnel.png') # load funnel image
        mode.resetAll()

    def resetAll(mode):
        mode.sand = [] # reset the sand
        # reset the background to be white
        for x in range(mode.width):
            for y in range(mode.height):
                if mode.gameBackground.getpixel((x,y)) != (255,255,255):
                    mode.gameBackground.putpixel((x,y), (255,255,255))
        mode.offset = random.randint(25, 300)
        mode.sandX = mode.offset # where is the sand being dispensed from?
        mode.sandY = 60 # see above
        mode.goals = [Goal(mode.offset + 200, 375)] # create at least one goal
        mode.gameWon = False # has the game been won?
        mode.extraGoals = random.randint(0,2) # how many extra goals should there be?
        # assign the extra goals positions
        for goal in range(mode.extraGoals):
            nextX = 0
            nextY = 0
            # choose a position for the bucket that's not going to overlap
            while True:
                shouldContinue = False
                nextX = random.randint(25, 575)
                nextY = random.randint(275, 375)
                for goal in mode.goals:
                    if distance(goal.x, goal.y, nextX, nextY) < 75:
                        print('this happened')
                        # a position that overlapped was picked; try again
                        shouldContinue = True
                        break
                    else: 
                        shouldContinue = False
                if shouldContinue:
                    continue
                # found a good position!
                break
            mode.goals.append(Goal(nextX, nextY))
        mode.obstacles = [(mode.offset + 100, random.randint(100,250), random.randint(20,50))] #x0, y0, length
        for obstacle in range(random.randint(2, 4)):
            length = random.randint(50, 100)
            x = 0
            y = 0
            goalYPos = []
            for goal in mode.goals:
                goalYPos.append(goal.y)
            # space out the obstacles a bit
            while True:
                shouldContinue = False
                x = random.randint(0, mode.width - length)
                y = random.randint(100, min(goalYPos) - 50)
                for x0,y0,length0 in mode.obstacles:
                    if distance(x,y,x0,y0) < 60:
                        break
                        shouldContinue = True
                    else:
                        shouldContinue = False
                if shouldContinue:
                    continue
                break
            mode.obstacles.append((x, y, length))
        mode.canDraw = True # can the user create lines?
        mode.spaceIsPressed = False
        print(mode.canDraw)


    # draw all of the obstacles
    def drawObstacles(mode):
        for index in range(len(mode.obstacles)):
            for x in range(mode.obstacles[index][0], mode.obstacles[index][0] + mode.obstacles[index][2]):
                for y in range(mode.obstacles[index][1], mode.obstacles[index][1] + 10):
                    mode.gameBackground.putpixel((x,y), (0,0,0))
    
    # detects if a sand grain hit a bucket
    def collidedWithBucket(mode, particle):
        nextRow, nextCol = particle.getMovePosition()
        rightMostCol = mode.effectiveAppWidth // mode.sandGrainSize - 1
        if nextCol > rightMostCol:
            nextCol = rightMostCol
        elif nextCol < 0:
            nextCol = 0
        x0,y0,x1,y1 = mode.getCellBounds(nextRow, nextCol)
        pointx, pointy = (x0 + x1) // 2, y1
        for goal in mode.goals:
            left = goal.x - 30
            right = goal.x + 30
            top = goal.y - 20
            bottom = goal.y + 25
            if left <= pointx <= right and top <= pointy <= bottom:
                return True
        return False

    # given an x,y position known to be part of a goal, find which goal it's part of 
    def findGoalIndex(mode, x, y):
        for goal in range(len(mode.goals)):
            if (mode.goals[goal].x - 30 <= x <= mode.goals[goal].x + 30 and
                mode.goals[goal].y - 20 <= y <= mode.goals[goal].y + 25):
                return goal

    # draw the buckets
    def drawGoals(mode, canvas):
        for goal in range(len(mode.goals)):
            canvas.create_image(mode.goals[goal].x, mode.goals[goal].y, 
                                image=ImageTk.PhotoImage(mode.goalImages[goal]))
            canvas.create_text(mode.goals[goal].x, mode.goals[goal].y, text=mode.goals[goal].counter,
                                fill='white', font=("Avenir", 18))

    # check if all the buckets are 0
    def checkForWin(mode):
        for goal in mode.goals:
            if goal.counter != 0:
                return
        mode.gameWon = True
        mode.spaceIsPressed = False
    
    # display win message... yay!
    def drawGameWon(mode, canvas):
        canvas.create_text(mode.width // 2, mode.height // 2, text='You won! :)',
                            font=("Avenir", 24), 
                            fill=rgbString(random.randint(1,254),random.randint(1,254),random.randint(1,254)))

    ####################################
    # sand and mouse stuff
    ####################################
    
    def mousePressed(mode, event):
        mode.mouseX, mode.mouseY = event.x, event.y

    # draw lines
    def mouseDragged(mode, event):
        g = mode.sandGrainSize // 2
        if mode.canDraw:
            mode.oldMouseX, mode.oldMouseY = mode.mouseX, mode.mouseY
            mode.mouseX, mode.mouseY = event.x, event.y
            linePoints = getLinePoints(mode.oldMouseX, mode.oldMouseY, mode.mouseX, mode.mouseY)
            for x, y in linePoints:
                if mode.gameBackground.getpixel((x+g,y-g)) == (255,255,255):
                    # give the lines some thickness
                    for horizontal in range(x-2, x+3):
                        for vertical in range(y-2, y+3):
                            mode.gameBackground.putpixel((horizontal,vertical),(0,0,0))

    def changePixelsGivenCell(mode, row, col, color):
        x0,y0,x1,y1 = mode.getCellBounds(row, col)
        for x in range(x0, x1):
            for y in range(y0, y1):
                mode.gameBackground.putpixel((x,y), color)

    def addParticles(mode, x, y):
        sandGrainNumber = int(random.triangular(7, 15, 10))
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
        mode.drawGoals(canvas)
        canvas.create_image(mode.sandX, mode.sandY, image=ImageTk.PhotoImage(mode.funnel),
                            anchor='s')
        if mode.gameWon:
            mode.drawGameWon(canvas)

    # create the particles
    def timerFired(mode):
        # when space is pressed, dispense the particles
        if mode.spaceIsPressed:
            mode.addParticles(mode.sandX // mode.sandGrainSize, mode.sandY // mode.sandGrainSize)
        mode.doStep()
        mode.checkForWin()
        mode.drawObstacles()

    def keyPressed(mode, event):
        if event.key == 'Space':
            mode.spaceIsPressed = not mode.spaceIsPressed
            mode.canDraw = not mode.canDraw
        elif event.key == 'Enter':
            mode.app.setActiveMode(mode.app.splashscreenMode)
        elif event.key == '0':
            mode.timerIsRunning = not mode.timerIsRunning
        elif event.key == 's':
            mode.doStep()
        elif event.key == 'r':
            mode.resetAll()

    #####################################
    # sand behavior
    #####################################    
    
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
        return nextRow >= maxRowValue

    def getMaxRowValue(mode, startRowValue, col):
        maxRowValue = startRowValue
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

            # check if the sand is sitting on top of something. if it is, call the slide function:
                # slide: slides the sand if it can slide, if not, colors the background 
            if mode.sandIsOnOtherSand(particle):
                mode.slide(particle)
            
            # did it hit the bottom?
            elif mode.hitBottom(particle):
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

            # if it's going to collide with a bucket, remove the sand and decrease the counter
            elif mode.collidedWithBucket(particle):
                nextRow, nextCol = particle.getMovePosition()
                x0,y0,x1,y1 = mode.getCellBounds(nextRow, nextCol)
                goalNumber = mode.findGoalIndex((x0+x1) // 2, y1)
                mode.goals[goalNumber].decreaseCounter()
                mode.sand.remove(particle)
            
            # if it's going to collide with something or reaches the bottom, sit at a legal spot
            elif mode.collisionDetected(particle):
                nextRow, nextCol = particle.getMovePosition()
                if nextCol >= mode.effectiveAppWidth // mode.sandGrainSize:
                    nextCol = mode.effectiveAppWidth // mode.sandGrainSize - 1
                maxRow = mode.getMaxRowValue(particle.row, nextCol)
                particle.row = maxRow
                particle.col = nextCol
            
            # otherwise, just keep moving
            else:
                particle.drop()

            if mode.shouldContinue:
                i += 1