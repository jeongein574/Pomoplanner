from cmu_graphics import *
import random

def onAppStart(app):
    app.scrollX = 0
    app.scrollMargin = 800
    app.playerX = app.width//2 # player's center
    app.dots = [(random.randrange(app.width),
                  random.randrange(60, app.height)) for _ in range(50)]

def makePlayerVisible(app):
    # scroll to make player visible as needed
    if (app.playerX < app.scrollMargin):
        app.scrollX = app.playerX - app.scrollMargin
    if (app.playerX > app.scrollX + app.width - app.scrollMargin):
        app.scrollX = app.playerX - app.width + app.scrollMargin

def movePlayer(app, dx, dy):
    app.playerX += dx
    makePlayerVisible(app)

def keyPressed(app, event):
    if (event.key == "Left"):    movePlayer(app, -5, 0)
    elif (event.key == "Right"): movePlayer(app, +5, 0)

def redrawAll(app, canvas):
    # draw the player, shifted by the scrollX offset
    cx, cy, r = app.playerX, app.height/2, 10
    cx -= app.scrollX # <-- This is where we scroll the player!!!
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill='cyan')

    # draw the dots, shifted by the scrollX offset
    for (cx, cy) in app.dots:
        cx -= app.scrollX  # <-- This is where we scroll each dot!!!
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill='lightGreen')

    # draw the x and y axes
    x = app.width/2 - app.scrollX # <-- This is where we scroll the axis!
    y = app.height/2
    canvas.create_line(x, 0, x, app.height)
    canvas.create_line(0, y, app.width, y)

    # draw the instructions and the current scrollX
    x = app.width/2
    canvas.create_text(x, 20, text='Use arrows to move left or right',
                       fill='black')
    canvas.create_text(x, 40, text=f'app.scrollX = {app.scrollX}',
                       fill='black')

def onKeyPress(app, key):
    if key == 'Down':
        pass
    elif key == 'Up':
        pass

runApp(width=300, height=300)