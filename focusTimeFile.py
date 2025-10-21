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

class FocusTimePage:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.labels = [
            '00', '25', '00',  # study
            '00', '05', '00',  # short
            '00', '10', '00'   # long
        ]
        
        self.studyIndex = 0
        self.buttonPositions = []

        for y in range(-140, 141, 140):
            for x in range(-140, 141, 140):
                self.buttonPositions.append((self.width/2 + x, self.height/2 + y))

    def draw(self, app):
        drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
        drawRect(app.width/2, app.height/2, 450, 450, fill = 'white', align = 'center')
        drawLabel('Focus Time', app.width/2-150, app.height/2-200, size = 16, font ='monospace')
        drawLabel('Short Break', app.width/2-150, app.height/2-60, size = 16, font ='monospace')
        drawLabel('Long Break', app.width/2-150, app.height/2+80, size = 16, font ='monospace')
        drawLabel(':   :', app.width/2, app.height/2-140, size = 60, font ='monospace')
        drawLabel(':   :', app.width/2, app.height/2, size = 60, font ='monospace')
        drawLabel(':   :', app.width/2, app.height/2+140, size = 60, font ='monospace')

        for x, y in self.buttonPositions:
            drawRect(x, y, 70, 70, fill=rgb(246, 246, 246), align='center')

        for i in range(len(self.labels)):
            drawLabel(self.labels[i], app.width/2+(i % 3-1)*140, app.height/2+(i // 3)*140-140, size=50, bold=True, font='monospace')

    def press(self, app, mouseX, mouseY):
        for i in range(len(self.buttonPositions)):
            buttonX, buttonY = self.buttonPositions[i]
            if buttonX - 35 <= mouseX <= buttonX + 35 and buttonY - 35 <= mouseY <= buttonY + 35:
                while True:
                    userinput = app.getTextInput('Enter a number between 0 and 59:')
                    if userinput.isdigit() and 0 <= int(userinput) <= 59:
                        if int(userinput) < 10:
                            if len(str(userinput)) == 1:
                                self.labels[i] = f'0{userinput}'
                            elif len(str(userinput)) > 1:
                                userinput = str(userinput)[-2:]
                                self.labels[i] = userinput
                        else:
                            self.labels[i] = f'{userinput}'
                        break
                    else:
                        userinput = app.getTextInput('Invalid input. Enter a number between 0 and 60:')
