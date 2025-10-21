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

class TaskAddPage:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.startTime = '00:00'
        self.endTime = '00:00'
        self.optimizeTime = '00:00'
        self.title = ''
        self.optimize = False
        self.importance = 5
        self.importanceBar = [0]*10

    def draw(self, app):
        drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
        drawRect(app.width/2, app.height/2, 450, 450, fill = 'white', align = 'center')

        #title
        drawRect(app.width/2, app.height/2-160, 400, 70, fill=gradient(rgb(250, 250, 250), rgb(220, 220, 220), start='top'), 
                 border = rgb(220, 220, 220), borderWidth = 1, align = 'center')
        drawLabel('Title:', app.width/2-160, app.height/2-160, size = 16, font ='monospace', bold = True, fill = rgb(80, 80, 80))
        drawLabel(self.title, app.width/2-100, app.height/2-160, font = 'monospace', align = 'left', size = 16)

        #checkbox
        drawRect(app.width/2, app.height/2-80, 400, 50, fill=gradient(rgb(250, 250, 250), rgb(220, 220, 220), start='top'), 
                 border = rgb(220, 220, 220), borderWidth = 1, align = 'center')
        drawLabel('Let the app decide the task time?', app.width/2-180, app.height/2-80, size = 16, font ='monospace', align = 'left', bold = True, fill = rgb(80, 80, 80))
        drawRect(app.width/2+170, app.height/2-78, 18, 18, fill = 'white', border = rgb(150, 150, 150), borderWidth = 1, align = 'center')
        if self.optimize == True:
            drawLabel('V', app.width/2+170, app.height/2-80, size = 18, bold = True, fill = 'tomato')

        # optimize & no optimize
        if self.optimize == False: noOptimizeColor, optimizeColor = rgb(80, 80, 80), rgb(200, 200, 200)
        else: noOptimizeColor, optimizeColor = rgb(200, 200, 200), rgb(80, 80, 80)     
        drawLabel(f'Start Time:', app.width/2-200, app.height/2-30, size = 16, font ='monospace', align = 'left', fill = noOptimizeColor, bold = True)
        drawRect(app.width/2+160, app.height/2-30, 80, 30, align = 'center', fill=gradient(rgb(250, 250, 250), rgb(220, 220, 220), start='top'),
                  border = rgb(220, 220, 220), borderWidth = 1)
        drawLabel(self.startTime, app.width/2+160, app.height/2-30, size = 16, font ='monospace', fill = noOptimizeColor)
        drawLabel(f'End Time:', app.width/2-200, app.height/2+10, size = 16, font ='monospace', align = 'left', fill = noOptimizeColor, bold = True)
        drawRect(app.width/2+160, app.height/2+10, 80, 30, align = 'center', fill=gradient(rgb(250, 250, 250), rgb(220, 220, 220), start='top'), 
                 border = rgb(220, 220, 220), borderWidth = 1)
        drawLabel(self.endTime, app.width/2+160, app.height/2+10, size = 16, font ='monospace', fill = noOptimizeColor)
        drawLabel(f'Estimated Time to Finish:', app.width/2-200, app.height/2+50, size = 16, font ='monospace', align = 'left', fill = optimizeColor, bold = True)     
        drawRect(app.width/2+160, app.height/2+50, 80, 30, align = 'center', fill=gradient(rgb(250, 250, 250), rgb(220, 220, 220), start='top'), 
                 border = rgb(220, 220, 220), borderWidth = 1)
        drawLabel(self.optimizeTime, app.width/2+160, app.height/2+50, size = 16, font ='monospace', fill = optimizeColor)
        
        # instruction
        if self.optimize == False: 
            instruction1 = 'Start time should be earlier' 
            instruction2 = 'than end time, and start time'
            instruction3 = 'should be later than the time now'

        else: 
            instruction1 = 'Estimated time to finish should' 
            instruction2 = 'be lesser than the amount of time'
            instruction3 = 'you have left until midnight'

        drawLabel(instruction1, app.width/2, app.height/2+150, size = 16, font ='monospace')
        drawLabel(instruction2, app.width/2, app.height/2+170, size = 16, font ='monospace')
        drawLabel(instruction3, app.width/2, app.height/2+190, size = 16, font ='monospace')

        # importance
        drawLabel('importance: ', app.width/2-200, app.height/2+90, size = 16, font ='monospace', align = 'left', fill = optimizeColor, bold = True)
        drawLabel('1  2  3  4  5  6  7  8  9  10', app.width/2+208, app.height/2+110, size = 11, font = 'monospace', align = 'right', fill = optimizeColor)
        barSize = 20
        for i in range(10):
            x = app.width / 2 + 10 + i * barSize
            y = app.height / 2 + 90
            color = gradient(rgb(250, 250, 250), rgb(220, 220, 220), start='right-bottom')
            if self.importanceBar[i]:
                color = gradient('brown', 'tomato', 'coral', 'lightSalmon', 'seashell', start='right-bottom')
            drawRect(x, y, barSize, 20, fill=color, border=rgb(200, 200, 200), borderWidth = 1, align='center')
            
    def press(self, app, mouseX, mouseY):
        if app.width/2 - 200 <= mouseX <= app.width/2 + 200 and app.height/2 - 195 <= mouseY <= app.height/2 -125:
            self.title = app.getTextInput('Task Title: ')
        if app.width/2+160 <= mouseX <= app.width/2+180 and app.height/2-90 <= mouseY <= app.height/2-70:
            self.optimize = not self.optimize
        if app.width/2+120 <= mouseX <= app.width/2+200 and app.height/2-45 <= mouseY <= app.height/2-15:
            while True:
                userInput = app.getTextInput('Write in the format of "00:00" (e.g. 14:30), in 15 minutes interval:')
                if self.isValid(userInput):
                    if int(userInput[0:2]) > int(currentTimehour) or (int(userInput[0:2]) == int(currentTimehour) and int(userInput[3:]) > int(currentTimeminute)):
                        self.startTime = userInput
                        break
        if app.width/2+120 <= mouseX <= app.width/2+200 and app.height/2-5 <= mouseY <= app.height/2+25:
            while True:
                userInput = app.getTextInput('Write in the format of "00:00" (e.g. 17:30), in 15 minutes interval:')
                if self.isValid(userInput):
                    self.endTime = userInput
                    break
        if app.width/2+120 <= mouseX <= app.width/2+200 and app.height/2+35 <= mouseY <= app.height/2+65:
            while True:
                userInput = app.getTextInput('Write in the format of "00:00" (hour:minute), in 15 minutes interval:')
                if self.isValid(userInput):
                    self.optimizeTime = userInput
                    break
        if app.width/2+10 <= mouseX <= app.width/2+210 and app.height/2+90 <= mouseY <= app.height/2+110:
            barIndex = int((mouseX - (app.width/2+10)) / 20)
            self.importanceBar = [0]*10
            for i in range(barIndex + 1):
                self.importanceBar[i] = 1
                self.importance = i

    def isValid(self, userInput):
        if len(userInput) != 5:
            return False
        if not (userInput[0].isdigit() and userInput[1].isdigit() and userInput[3].isdigit() and userInput[4].isdigit()):
            return False
        if not (0 <= int(userInput[0:2]) <= 23 and 0 <= int(userInput[3:]) <= 59):
            return False
        if userInput[2] != ':':
            return False
        if int(userInput[3:]) not in (0, 15, 30, 45):
            return False
        return True