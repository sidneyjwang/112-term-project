from cmu_112_graphics import *
import random
import time

####################################
# this isn't sand
####################################

# from the 112 course website
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

class Particle:
    GRAVITY = 1.5
    MAX_VELOCITY = 15
    HEIGHT = 0
    WIDTH = 0
    TOTAL_PARTICLES = 0
    def __init__(self, xPos, yPos, xVelocity, yVelocity, intendedColor, 
                colorVariation, height, width):
        self.xPos = xPos
        self.yPos = yPos
        self.yVelocity = yVelocity
        self.time = 0
        self.xVelocity = xVelocity
        self.R = intendedColor[0] + colorVariation[0]
        self.G = intendedColor[1] + colorVariation[1]
        self.B = intendedColor[1] + colorVariation[2]
        self.canDrop = True
        self.canSlide = True
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
        return (self.xPos + self.xVelocity, self.yPos + self.yVelocity)
    
    # drops the sand particle
    def drop(self):
        self.yPos += self.yVelocity
        self.yVelocity += Particle.GRAVITY * self.time
        self.time += 1
        self.xPos += self.xVelocity
        self.checkLegalMove()

    # check if the proposed move would put a grain inside another one, or move
    # off the screen; if so, undoes the move
    def checkLegalMove(self):
        if self.yVelocity >= Particle.MAX_VELOCITY:
            self.yVelocity = Particle.MAX_VELOCITY
        if self.yPos > Particle.HEIGHT:
            self.yPos = Particle.HEIGHT
            self.yVelocity = 0
        # revisit once sand piling starts:
        if self.xPos > Particle.WIDTH:
            self.xPos = Particle.WIDTH
            self.xVelocity = 0
        elif self.xPos < 0:
            self.xPos = 0
            self.xVelocity = 0

    def slide(self):
        pass

def appStarted(app):
    app.sand = [] # a list to keep track of all particle objects
    app.timerDelay = 10 # put this at 10 when not debugging
    app.currentX = 0 # the x position of the mouse
    app.currentY = 0 # the y position of the mouse
    app.mouseIsPressed = False # boolean flag: is the mouse being held?

# update the mouse's x and y coordinates, and set the boolean to true
def mousePressed(app, event):
    app.mouseIsPressed = True
    app.currentX, app.currentY = event.x, event.y

# set boolean to false
def mouseReleased(app, event):
    app.mouseIsPressed = False

# update the mouse coordinates when moved
def mouseMoved(app, event):
    app.currentX, app.currentY = event.x, event.y

# also update mouse coordinates when dragged
def mouseDragged(app, event):
    app.currentX, app.currentY = event.x, event.y

# when the mouse is pressed, create a shower of sand emerging from the point
def addParticles(app, x, y):
    sandGrainNumber = int(random.triangular(5, 10, 5))
    for i in range(sandGrainNumber):
        rVar = int(random.triangular(0, 25, 5)) * random.choice([-1, 1])
        gVar = int(random.triangular(0, 25, 5)) * random.choice([-1, 1])
        bVar = int(random.triangular(0, 25, 5)) * random.choice([-1, 1])
        signFlip = random.choice([-1, 1])
        xVelocity = random.triangular(0, 2, 0) * signFlip
        yVelocity = random.random() * 7.5
        newParticle = Particle(x, y, xVelocity, yVelocity, 
                        (255,100,100), (rVar,gVar,bVar), app.height-100, app.width-100)
        app.sand.append(newParticle)

# draw all of the sand objects        
def drawSand(app, canvas):
    for particle in app.sand:
        canvas.create_rectangle(particle.xPos-1, particle.yPos-1, 
                                particle.xPos+1, particle.yPos+1, 
                                fill=particle.color, width=0)

def redrawAll(app, canvas):
    drawSand(app, canvas)

# create the particles
def timerFired(app):
    if app.mouseIsPressed:
        addParticles(app, app.currentX, app.currentY)
    for particle in range(len(app.sand)):
        x, y = app.sand[particle].getMovePosition()
        print(f'Particle #{particle}', 'Current position:', f'({app.sand[particle].xPos}, {app.sand[particle].yPos})')
        print(f'Particle #{particle}', 'Next position:', f'({x}, {y})')
        # if canDrop is true:
        if app.sand[particle].canDrop:
            app.sand[particle].drop()
        # if there is a particle at the next anticipated location of the particle: set canMove to false
        # else: set canSlide and canMove to false

def main():
    runApp(width=600, height=400)

if __name__ == '__main__':
    main()