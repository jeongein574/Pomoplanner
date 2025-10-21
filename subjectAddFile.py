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

class SubjectAddPage:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.colorPalette = ['lightSalmon', 'powderBlue', 'thistle', 'moccasin', 'paleGreen', 'mediumAquamarine', 'rosyBrown', 'pink', 'lightSteelBlue', 'tan']
        self.subject = ''

    def draw(self, app):
        drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
        drawRect(app.width/2, app.height/2, 450, 300, fill = 'white', align = 'center')
        drawRect(app.width/2, app.height/2-100, 350, 50, fill = rgb(246, 246, 246), align = 'center')
        drawLabel('Subject Name:', app.width/2 - 100, app.height/2-100, font = 'monospace', size = 16)
        drawLabel(self.subject, app.width/2, app.height/2-100, font = 'monospace', align = 'left', size = 16)

        paletteX, paletteY = app.width / 2 - 160, app.height / 2
        paletteSize = 30
        for color in self.colorPalette[:5]:
            drawCircle(paletteX, paletteY, paletteSize, fill=color)
            paletteX += 80

        paletteX, paletteY = app.width / 2 - 160, app.height / 2 + 80
        for color in self.colorPalette[5:]:
            drawCircle(paletteX, paletteY, paletteSize, fill=color)
            paletteX += 80

    def press(self,app,mouseX, mouseY):
        selectedColor = None
        if app.width/2 - 175 <= mouseX <= app.width/2 + 175 and app.height/2 - 125 <= mouseY <= app.height/2 -75:
            self.subject = app.getTextInput('e.g. CS, Math, History...')
 
        paletteX, paletteY = app.width/2 - 160, app.height/2
        paletteSize = 30
        for color in self.colorPalette:
            if (paletteX - paletteSize <= mouseX <= paletteX + paletteSize and
                    paletteY - paletteSize <= mouseY <= paletteY + paletteSize):
                selectedColor = color
                break
            paletteX += 80
            if paletteX > app.width/2 + 160:
                paletteX = app.width/2 - 160
                paletteY += 80
        
        subjectExist = False
        for subjectSubList in app.TimerPage.subjectList:
            if self.subject == subjectSubList[0]:
                subjectExist = True
                break
        
        if self.subject != '' and selectedColor != None and subjectExist == False:
            if len(app.TimerPage.subjectList) >= 5:
                app.TimerPage.subjectList.append([self.subject, selectedColor, '00:00:00', 470, False])
            else:
                app.TimerPage.subjectList.append([self.subject, selectedColor, '00:00:00', 470, True])
            self.subject, color = '', None
            app.TimerPage.subjectAddPage = False
            app.TimerPage.saveSubjects()