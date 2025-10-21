from cmu_graphics import *
import datetime
import calendar
import copy
import json
import os, pathlib

currentTime = datetime.datetime.now()
currentTimehour = f'0{currentTime.hour}' if currentTime.hour < 10 else str(currentTime.hour)
currentTimeminute = f'0{currentTime.minute}' if currentTime.minute < 10 else str(currentTime.minute)

year = currentTime.year
month = currentTime.month 

class TimerPage:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.subjectList = []
        self.subjectAddPage = False
        self.focusTimerRun = False
        self.shortTimerRun = False
        self.longTimerRun = False
        self.activeSubjectIndex = None
        self.lastVisible = 4
        self.startTimerSound = self.loadSound("sounds\\startTimer.mp3")
        self.endTimerSound = self.loadSound("sounds\\endTimer.mp3")

    def draw(self, app):
        drawRect(0, 330, app.width, app.height-330, fill='white')
        subjectList = [subject for subject in self.subjectList if subject[4] == True]
        for index, subjectSubList in enumerate(subjectList):
            subject, color, studyTime, location = subjectSubList[0], subjectSubList[1], subjectSubList[2], subjectSubList[3]

            location += 50*index
            deleteX = app.width*5/6

            drawLabel(subject, app.width/4, location, font = 'monospace', size = 18, align = 'left')
            drawLabel(studyTime, app.width*3/4, location, font = 'monospace', size = 18, align = 'left')
            drawCircle(app.width/5, location, 20, fill = color)
            drawRect(deleteX, location, 14, 14, fill = rgb(246, 246, 246), border = 'tomato', borderWidth = 0.5, align = 'center')
            drawLabel('X', deleteX, location, size = 12, fill = 'tomato')
            if self.focusTimerRun and index == self.activeSubjectIndex:
                drawRect(app.width/5, location, 12, 12, fill = 'white', align = 'center')
                drawRect(app.width/5, location, 3, 12, fill = color, align = 'center')
            elif self.focusTimerRun == False or index != self.activeSubjectIndex:
                drawRegularPolygon(app.width/5, location, 10, 3, rotateAngle = 90, fill = 'white', align = 'center')        

        drawRect(app.width/5, 400, 150, 40, fill=gradient(rgb(250, 250, 250), rgb(220, 220, 220), start='top'), border = rgb(220, 220, 220), borderWidth = 1, align='center')
        drawLabel('+ Subject', app.width/5, 400, font='monospace', size=18)

        #scroll bar
        scrollX = app.width*9/10
        drawRect(scrollX, 570, 10, 200, fill=rgb(200, 200, 200), align='center')
        drawRegularPolygon(scrollX, 460, 7, 3, fill = rgb(200, 200, 200), align = 'center')        
        drawRegularPolygon(scrollX, 680, 7, 3, rotateAngle = 180, fill = rgb(200, 200, 200), align = 'center')        

    def press(self, app, mouseX, mouseY):
        if self.subjectAddPage == True:
            if not (app.width/2-225 <= mouseX <= app.width/2+225 and 
                    app.height/2-150 <= mouseY <= app.height/2+150):
                self.subjectAddPage = False

        
        if self.subjectAddPage == False and (app.width/5 - 75 <= mouseX <= app.width/5 + 75 
                                           and 380 <= mouseY <= 420):
            self.subjectAddPage = True

        subjectList = [subject for subject in self.subjectList if subject[4] == True]
        for subjectSubList in subjectList:
            location = subjectSubList[3]
            index = subjectList.index(subjectSubList)
            location += 50*index
            subjectX, subjectY = app.width/5, location
            deleteX = app.width*5/6
            if (subjectX - 20 <= mouseX <= subjectX + 20 and
                    subjectY - 20 <= mouseY <= subjectY + 20):
                if self.focusTimerRun or (self.activeSubjectIndex is not None and self.activeSubjectIndex != index):
                    self.stopTimer() 
                else:
                    self.startTimer(app)
                self.activeSubjectIndex = index
                break

            if (deleteX-7 <= mouseX <= deleteX+7 and location-7 <= mouseY <= location+7):
                self.deleteSubjects(index)
                break

    def startTimer(self, app):
        self.startTimerSound.play()
        self.focusTimerRun, self.shortTimerRun, self.longTimerRun = True, False, False
        app.FocusTimePage.studyIndex = 0

    def stopTimer(self):
        self.focusTimerRun = False

    def saveSubjects(self):
        for subjectSubList in self.subjectList:
            subjectSubList[2] = '00:00:00'
        with open("saveSubject.json", "w") as f:
            json.dump(self.subjectList, f)
    
    def loadSubjects(self):
        try:
            with open("saveSubject.json", "r") as f:
                temp = []
                for idx, subject in enumerate(json.load(f)):
                    subject[4] = idx <= 4
                    temp.append(subject)
                self.subjectList = temp
        except FileNotFoundError:
            self.subjectList = []

    def deleteSubjects(self, index):
        if 0 <= index < len(self.subjectList):
            del self.subjectList[index]
            for subjectSubList in self.subjectList[:5]:
                subjectSubList[4] = True
            for subjectSubList in self.subjectList[6:]:
                subjectSubList[4] = False
            self.saveSubjects()

    def loadSound(self, relativePath):
        absolutePath = os.path.abspath(relativePath)
        url = pathlib.Path(absolutePath).as_uri()
        return Sound(url)
