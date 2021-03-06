###################################
# particle class
###################################

def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

class Particle:
    GRAVITY = 1.5
    MAX_VELOCITY = 15
    HEIGHT = 0
    WIDTH = 0
    TOTAL_PARTICLES = 0
    PARTICLE_SIZE = 2
    def __init__(self, particleNumber, col, row, xVelocity, yVelocity, intendedColor, 
                colorVariation, height, width, particleSize=2):
        self.particleNumber = particleNumber
        self.col = col
        self.row = row
        self.yVelocity = yVelocity
        self.time = 0
        self.xVelocity = xVelocity
        self.R = int(intendedColor[0]) + colorVariation[0]
        self.G = int(intendedColor[1]) + colorVariation[1]
        self.B = int(intendedColor[2]) + colorVariation[2]
        if self.R > 254: self.R = 254
        elif self.R < 1: self.R = 1
        if self.G > 254: self.G = 254
        elif self.G < 1: self.G = 1
        if self.B > 254: self.B = 254
        elif self.B < 1: self.B = 1
        self.color = rgbString(self.R, self.G, self.B)
        self.canSlide = False
        Particle.HEIGHT = height
        Particle.WIDTH = width
        Particle.TOTAL_PARTICLES += 1
        Particle.PARTICLE_SIZE = particleSize

    def getMovePosition(self):
        row, col =  int(self.row + self.yVelocity), int(self.col + self.xVelocity)
        return (row, col)
    
    # drops the sand particle
    def drop(self):
        self.row += int(self.yVelocity)
        self.yVelocity += int(Particle.GRAVITY * self.time)
        self.time += 1
        self.col += int(self.xVelocity)
        self.checkLegalMove()

    # check if the proposed move would put a grain inside another one, or move
    # off the screen; if so, undoes the move
    def checkLegalMove(self):
        if self.yVelocity >= Particle.MAX_VELOCITY:
            self.yVelocity = Particle.MAX_VELOCITY
        if self.row >= Particle.HEIGHT // Particle.PARTICLE_SIZE:
            self.row = Particle.HEIGHT // Particle.PARTICLE_SIZE - 1
            self.yVelocity = 0
        # revisit once sand piling starts:
        if self.col >= Particle.WIDTH // Particle.PARTICLE_SIZE:
            self.col = Particle.WIDTH // Particle.PARTICLE_SIZE - 1
            self.xVelocity = 0
        elif self.col < 0:
            self.col = 0
            self.xVelocity = 0