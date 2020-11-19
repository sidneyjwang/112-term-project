from cmu_112_graphics import *

####################################
# ~what is life~
####################################

# 11/4: started file. got basic framework done for dropping a single sand, 
# figured out some values that make sand physics work ok. still need to figure out 
# alternative for mousedragged so that pressing and holding also dispenses sand.

class Particle:
    pass

def appStarted(app):
    app.gravity = 2
    app.maxVelocity = 20
    app.sand = [] #(xpos, ypos, velocity, time)
    app.timerDelay = 1


def mouseDragged(app, event):
    app.sand.append([event.x, event.y, 0, app.gravity, 1])

def drawSand(app, canvas):
    for index in range(len(app.sand)):
        canvas.create_oval(app.sand[index][0] - 5, app.sand[index][1] - 5, 
                            app.sand[index][0] + 5, app.sand[index][1] + 5, fill = 'pink')

def redrawAll(app, canvas):
    drawSand(app, canvas)

def timerFired(app):
    for index in range(len(app.sand)):
        app.sand[index][1] += app.sand[index][2]
        app.sand[index][2] += app.gravity * app.sand[index][3]
        app.sand[index][3] += 1
        if app.sand[index][2] >= app.maxVelocity:
            app.sand[index][2] = app.maxVelocity
        if app.sand[index][1] > app.height: app.sand[index][1] = app.height

def main():
    runApp(width=1200, height=800)

if __name__ == '__main__':
    main()