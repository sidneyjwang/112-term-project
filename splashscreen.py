from cmu_112_graphics import *

# this project uses cmu-112-graphics, which was taken from
# https://www.cs.cmu.edu/~112/

# from the 112 course website:
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def appStarted(app):
    app.mouseX, app.mouseY = 0, 0
    app.background = app.loadImage('samplesandbackground.png')
    app.center = app.width / 2
    app.titlePositionY = app.height/4
    app.textHeight = 20
    app.sandboxTextY = app.height/16*7
    app.sandboxWidth = 80
    app.sandboxColor = rgbString(0,0,0)
    app.pictureTextY = app.height/16*9
    app.pictureWidth = 70
    app.pictureColor = rgbString(0,0,0)
    app.gameTextY = app.height/16*11
    app.gameWidth = 60
    app.gameColor = rgbString(0,0,0)

def mouseMoved(app, event):
    app.mouseX, app.mouseY = event.x, event.y

def mousePressed(app, event):
    if (app.center-app.sandboxWidth < app.mouseX < app.center+app.sandboxWidth and
    app.sandboxTextY-app.textHeight < app.mouseY < app.sandboxTextY+app.textHeight):
        # replace with sandbox mode
        print('sandbox!')
    elif (app.center-app.pictureWidth < app.mouseX < app.center+app.pictureWidth and
    app.pictureTextY-app.textHeight < app.mouseY < app.pictureTextY+app.textHeight):
        # replace with picture mode
        print('picture!')
    elif (app.center-app.gameWidth < app.mouseX < app.center+app.gameWidth and
    app.gameTextY-app.textHeight < app.mouseY < app.gameTextY+app.textHeight):
        # replace with game mode
        print('game!')

def timerFired(app):
    if (app.center-app.sandboxWidth < app.mouseX < app.center+app.sandboxWidth and
    app.sandboxTextY-app.textHeight < app.mouseY < app.sandboxTextY+app.textHeight):
        app.sandboxColor = rgbString(160,160,160)
        app.pictureColor, app.gameColor = rgbString(0,0,0), rgbString(0,0,0)
    elif (app.center-app.pictureWidth < app.mouseX < app.center+app.pictureWidth and
    app.pictureTextY-app.textHeight < app.mouseY < app.pictureTextY+app.textHeight):
        app.pictureColor = rgbString(160,160,160)
        app.sandboxColor, app.gameColor = rgbString(0,0,0), rgbString(0,0,0)
    elif (app.center-app.gameWidth < app.mouseX < app.center+app.gameWidth and
    app.gameTextY-app.textHeight < app.mouseY < app.gameTextY+app.textHeight):
        app.gameColor = rgbString(160,160,160)
        app.sandboxColor, app.pictureColor = rgbString(0,0,0), rgbString(0,0,0)
    else:
        app.pictureColor = rgbString(0,0,0)
        app.sandboxColor = rgbString(0,0,0)
        app.gameColor = rgbString(0,0,0)

def redrawAll(app, canvas):
    # insert background image here
    canvas.create_image(app.width / 2, app.height, 
                        image=ImageTk.PhotoImage(app.background), anchor='s')
    canvas.create_text(app.center, app.titlePositionY, 
                        text='THISISNTSAND', font=("Avenir", 32))
    canvas.create_text(app.center, app.sandboxTextY, text='SANDBOX  >',
                        font=("Avenir", 24), fill=app.sandboxColor)
    canvas.create_text(app.center, app.pictureTextY, text='PICTURE  >',
                        font=("Avenir", 24), fill=app.pictureColor)
    canvas.create_text(app.center, app.gameTextY, text='GAME  >',
                        font=("Avenir", 24), fill=app.gameColor)

def main():
    runApp(width=600, height=400)

if __name__ == '__main__':
    main()