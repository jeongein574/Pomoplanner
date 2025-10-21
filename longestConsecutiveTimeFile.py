from cmu_graphics import *
import datetime
import calendar
import copy
import json

currentTime = datetime.datetime.now()
currentTimehour = f'0{currentTime.hour}' if currentTime.hour < 10 else str(currentTime.hour)
currentTimeminute = f'0{currentTime.minute}' if currentTime.minute < 10 else str(currentTime.minute)

year = currentTime.year
month = currentTime.month 

class LongestConsecutiveTimePage:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.labels = ['00', '30']
        self.positions = []
        for x in range(-100, 51, 150):
            self.positions.append((self.width/2+x, self.height/2-50))

    def draw(self, app):
        drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
        drawRect(app.width/2, app.height/2, 450, 300, fill = 'white', align = 'center')
        drawLabel('H    M', app.width/2+30, app.height/2-50, size = 50, font ='monospace', bold = True)
        drawLabel('Longest Consecutive Worktime:', app.width/2, app.height/2-120, size = 20, bold = True, font ='monospace')
        drawLabel('This function allows the app to',  app.width/2, app.height/2+30, size = 17, align = 'top', font ='monospace')
        drawLabel('make optimized study plan for you.',  app.width/2, app.height/2+55, size = 17, align = 'top', font ='monospace')
        drawLabel('A single task exceeding this time will',  app.width/2, app.height/2+80, size = 17, align = 'top', font ='monospace')
        drawLabel('be allotted at multiple time periods.', app.width/2, app.height/2+105, size = 17, align = 'top', font ='monospace')

        for i in range(2):
                x, y = self.positions[i]
                drawRect(x, y, 70, 60, fill=gradient(rgb(250, 250, 250), rgb(220, 220, 220), start='top'),
                          border = rgb(220, 220, 220), borderWidth = 1, align = 'center')
                drawLabel(self.labels[i], x, y, size = 50, bold = True, font = 'monospace')
    
    def press(self, app, mouseX, mouseY):
        for i in range(2):
            buttonX, buttonY = self.positions[i]
            if buttonX - 35 <= mouseX <= buttonX + 35 and buttonY - 35 <= mouseY <= buttonY + 35:
                while True:
                    userinput = app.getTextInput('Enter a number between 0 and 60, in 15 minutes interval:')
                    if i == 0 and userinput.isdigit() and 0 <= int(userinput) <= 60:
                        if int(userinput) < 10:
                            self.labels[i] = f'0{userinput}'
                        else:
                            self.labels[i] = f'{userinput}'
                        break
                    elif i == 1 and userinput.isdigit() and int(userinput) in (0, 15, 30, 45, 60):
                        if int(userinput) == 0:
                            self.labels[i] = f'0{userinput}'
                        else:
                            self.labels[i] = f'{userinput}'
                        break
                    else:
                        userinput = app.getTextInput('Invalid input. Enter a number between 0 and 60, in 15 minutes interval:')
