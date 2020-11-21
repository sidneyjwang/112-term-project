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
        if self.R > 255: self.R = 255
        elif self.R < 0: self.R = 0
        if self.G > 255: self.G = 255
        elif self.G < 0: self.G = 0
        if self.B > 255: self.B = 255
        elif self.B < 0: self.B = 0
        self.color = rgbString(self.R, self.G, self.B)
        Particle.HEIGHT = height
    def move(self):
        self.yPos += self.yVelocity
        self.yVelocity += Particle.GRAVITY * self.time
        self.time += 1
        self.xPos += self.xVelocity
        if self.yVelocity >= Particle.MAX_VELOCITY:
            self.yVelocity = Particle.MAX_VELOCITY
        if self.yPos > Particle.HEIGHT:
            self.yPos = Particle.HEIGHT
        # revisit once sand piling starts:
        # if self.xPos < Particle.WIDTH:
        #     self.xPos = Particle.WIDTH
        # elif self.xPos < 0:
        #     self.xPos = 0

def appStarted(app):
    app.sand = [] # a list to keep track of all particle objects
    app.timerDelay = 1 # put this at 1 when not debugging

def mouseDragged(app, event):
    sandGrainNumber = int(random.triangular(7, 15, 10))
    for i in range(sandGrainNumber):
        rVar = int(random.triangular(0, 25, 5)) * random.choice([-1, 1])
        gVar = int(random.triangular(0, 25, 5)) * random.choice([-1, 1])
        bVar = int(random.triangular(0, 25, 5)) * random.choice([-1, 1])
        signFlip = random.choice([-1, 1])
        xVelocity = random.triangular(0, 2, 0) * signFlip
        yVelocity = random.random() * 7.5
        app.sand.append(Particle(event.x, event.y, xVelocity, yVelocity, 
                        (255,100,100), (rVar,gVar,bVar), app.height, app.width))

def drawSand(app, canvas):
    for particle in app.sand:
        canvas.create_rectangle(particle.xPos-1, particle.yPos-1, 
                                particle.xPos+1, particle.yPos+1, 
                                fill=particle.color, width=0)

def redrawAll(app, canvas):
    drawSand(app, canvas)

def timerFired(app):
    for particle in app.sand:
        particle.move()

def main():
    runApp(width=1200, height=800)

if __name__ == '__main__':
    main()