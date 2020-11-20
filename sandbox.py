from cmu_112_graphics import *
import random

####################################
# ~what is life~
####################################

# from the 112 course website
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

class Particle:
    GRAVITY = 2
    MAX_VELOCITY = 20
    HEIGHT = 0
    def __init__(self, xPos, yPos, height):
        self.xPos = xPos
        self.yPos = yPos
        self.velocity = 0
        self.time = 0
        self.color = rgbString(255, 0, 100)
        Particle.HEIGHT = height
    def move(self):
        self.yPos += self.velocity
        self.velocity += Particle.GRAVITY * self.time
        self.time += 1
        if self.velocity >= Particle.MAX_VELOCITY:
            self.velocity = Particle.MAX_VELOCITY
        if self.yPos > Particle.HEIGHT:
            self.yPos = Particle.HEIGHT

def appStarted(app):
    app.sand = [] # a list to keep track of all particle objects
    app.timerDelay = 1


def mouseDragged(app, event):
    app.sand.append(Particle(event.x, event.y, 800))

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