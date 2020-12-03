from cmu_112_graphics import *
import random

class Goal:
    def __init__ (self, x, y):
        self.counter = 100
        self.x = x
        self.y = y
    def decreaseCounter(self):
        self.counter -= 1

def appStarted(app):
    app.background = app.loadImage('whiteBackground.png')
    app.goalImages = [app.loadImage('pinkbucket.png')]
    app.goalNumber = 1
    app.goals = []
    addGoals(app)
    
def addGoals(app):
    for goal in range(app.goalNumber):
        app.goals.append(Goal(150, 150))
        # drawRectangle(app, app.goals[goal].x-25, app.goals[goal].y-25, 
        #                 app.goals[goal].x+25, app.goals[goal].y+25, app.goals[goal].color)

def mousePressed(app, event):
    x, y = event.x, event.y
    if findGoalIndex(app, x, y) != None:
        # find which goal it hit
        goal = findGoalIndex(app, x, y)
        app.goals[goal].decreaseCounter()

def findGoalIndex(app, x, y):
    for goal in range(len(app.goals)):
        if (app.goals[goal].x - 25 < x < app.goals[goal].x + 25 and
            app.goals[goal].y - 25 < y < app.goals[goal].y + 25):
            print(goal)
            return goal
    return None

def drawRectangle(app, x0, y0, x1, y1, color):
    for x in range(x0, x1+1):
        for y in range(y0, y1+1):
            app.background.putpixel((x,y), color)

def timerFired(app):
    pass
    # addGoals(app)

def drawGoals(app, canvas):
    for goal in range(len(app.goals)):
        print(goal)
        canvas.create_image(app.goals[goal].x, app.goals[goal].y, 
                            image=ImageTk.PhotoImage(app.goalImages[goal]))
        canvas.create_text(app.goals[goal].x, app.goals[goal].y, text=app.goals[goal].counter,
                            fill='white', font='Comic-Sans 24')

def redrawAll(app, canvas):
    canvas.create_image(app.width/2, app.height/2,  
                            image=ImageTk.PhotoImage(app.background))
    drawGoals(app, canvas)
    canvas.create_polygon((125,125), (175,125), (170, 175), (130, 175), fill='', width=2,outline='black')

runApp(width=600, height=400)