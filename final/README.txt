112-term-project
  _   _     _     _           _                       _ 
 | | | |   (_)   (_)         | |                     | |
 | |_| |__  _ ___ _ ___ _ __ | |_ ___  __ _ _ __   __| |
 | __| '_ \| / __| / __| '_ \| __/ __|/ _` | '_ \ / _` |
 | |_| | | | \__ \ \__ \ | | | |_\__ \ (_| | | | | (_| |
  \__|_| |_|_|___/_|___/_| |_|\__|___/\__,_|_| |_|\__,_|
                                                                                     
~~About the project~~
thisisntsand is a sand art generator, with a couple spicy quirks. Deriving inspiration from thisissand.com and Sugar, Sugar, the project features three modes: a sandbox mode, a picture mode, and a game mode. In sandbox mode, the user is free to pick different colors and pile sand to create art. In picture mode, the user uploads a picture and has the option to watch the computer recreate and sand-ify the image, or they may choose to recreate the picture with sand, after which the computer will score their effort. In game mode, the user must direct a flow of sand from a starting point to an end point by drawing lines for the sand to slide on and avoiding the obstacles in the way.

~~How to play~~
Open and run thisisntsand.py to begin. No modules necessary outside of 112 course notes PIL/Pillow. Use window size 600 x 400 (default in the code). 

11/23 tp0 update:
- Open the file named sandbox.py to run the program
- gradientTest is irrelevant for now; that is where the future color picking feature will reside

11/29 tp1 update:
- Open the file named thisisntsand.py to run the program
- When running sandbox mode, press space to bring up the gradient selection screen! Press with mouse which color you'd like to select; then press space again to go back to drawing sand.

12/5 tp2 update:
- All 3 modes work!

12/9 tp3 update:
- Added a couple quality of life features
- Now featuring: Gradients! And multi-colored game mode sand!

~~Controls~~
Home screen:
- Press space to bring up help menu.

Help screen:
- Press space to return to home screen.

Sandbox mode:
- Press space to bring up gradient picker.
- Press Enter to return to home screen.
- Press R to reset the canvas to blank.

Game mode:
- Press space to begin letting sand fall. Note that drawing is disabled when new sand is being added.
- Press enter to return to home screen.
- Press R to regenerate a level.

Picture mode:
- Press space to enter a different file name.
- Press space to bring up and dismiss gradient picker in recreation mode.
- Press enter to return to home screen.
- Press S to score the level.

~~Shortcuts~~
In any mode besides animation, pressing 0 will pause the timer and pressing s steps through one timerFired call at a time.

~~Citations~~
- cmu-112-graphics from https://www.cs.cmu.edu/~112/
- Gradient picture from thisissand.com
- Bob Ross winter painting demo by Bob Ross
- Andrew for bucket art

Inspiration for the project comes from thisissand.com and sugar, sugar
