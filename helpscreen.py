from cmu_112_graphics import *

class helpScreen(Mode):
    def appStarted(mode):
        mode.helpBackground = mode.loadImage('samplesandbackground.png')

    def redrawAll(mode, canvas):
        canvas.create_text(mode.width/2, mode.height/8, text='how to play', 
                            font=("Avenir", 28, 'bold'))
        canvas.create_text(mode.width/14, mode.height/32 * 7, text='sandbox mode', 
                            font=("Avenir", 20, 'bold'), anchor = 'w')
        canvas.create_text(mode.width/14, mode.height/32 * 9, 
                            text='drag the mouse to dispense sand, press space to select colors', 
                            font=("Avenir", 16), anchor = 'w')
        canvas.create_text(mode.width/14, mode.height/32 * 12, text='picture mode', 
                            font=("Avenir", 20, 'bold'), anchor = 'w')
        canvas.create_text(mode.width/14, mode.height/32 * 14, 
                            text='upload an image and recreate it, or animate a sand recreation', 
                            font=("Avenir", 16), anchor = 'w')
        canvas.create_text(mode.width/14, mode.height/32 * 17, text='game mode', 
                            font=("Avenir", 20, 'bold'), anchor = 'w')
        canvas.create_text(mode.width/14, mode.height/32 * 19, 
                            text='direct sand to its destination, toggle flow with space', 
                            font=("Avenir", 16), anchor = 'w')
        canvas.create_text(mode.width/2, mode.height/32 * 23, 
                            text='press space to return home', 
                            font=("Avenir", 20, 'bold'))
        canvas.create_image(mode.width/2, mode.height, anchor='s', 
                            image=ImageTk.PhotoImage(mode.helpBackground))
    
    def keyPressed(mode, event):
        if event.key == 'Space':
            mode.app.setActiveMode(mode.app.splashscreenMode)
