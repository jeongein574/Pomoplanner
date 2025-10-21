from cmu_graphics import *
import datetime
import calendar
import copy
import json
from PIL import Image
import os, pathlib

currentTime = datetime.datetime.now()
currentTimehour = f'0{currentTime.hour}' if currentTime.hour < 10 else str(currentTime.hour)
currentTimeminute = f'0{currentTime.minute}' if currentTime.minute < 10 else str(currentTime.minute)

year = currentTime.year
month = currentTime.month 

class MainPage:
    def __init__(self, width, height, FocusTimePage):
        self.width, self.height = width, height
        self.timer = True
        self.report = False
        self.calendar = False
        self.focus = False 
        self.taskAdd = False
        self.studyLabelNum = '00:25:00'
        self.studyLabel = 'Focus Time'
        self.mainColor = rgb(246, 246, 246)
        self.pomodoroList = []
        self.countOne = False
        self.startTime = 0
        self.Labels = [
            '00', '25', '00',  # study
            '00', '05', '00',  # short
            '00', '10', '00'   # long
        ]

    def timerLabel(self, app):
        studyLabelIndex = app.FocusTimePage.studyIndex
        hour, minute, second = self.Labels[int(studyLabelIndex)*3 : int(studyLabelIndex)*3 + 3]
        studyLabels = ['Focus Time', 'Short Break', 'Long Break']

        if app.TimerPage.focusTimerRun or app.TimerPage.shortTimerRun or app.TimerPage.longTimerRun:
            hour, minute, second = int(hour), int(minute), int(second)
            second -= 1
            if second <= 0 and minute <= 0 and hour <= 0:
                second, minute, hour = 0, 0, 0
            if second < 0:
                second = 59
                minute -= 1
            if minute < 0:
                minute = 59
                hour -= 1
            if hour < 0:
                hour = 0
            
            if hour < 10: timerH = f'0{str(hour)}'
            else: timerH = str(hour)
            if minute < 10: timerM = f'0{str(minute)}'
            else: timerM = str(minute)
            if second < 10: timerS = f'0{str(second)}'
            else: timerS = str(second)

            self.Labels[int(studyLabelIndex)*3] = timerH
            self.Labels[int(studyLabelIndex)*3+1] = timerM
            self.Labels[int(studyLabelIndex)*3+2] = timerS
            self.studyLabelNum = f'{timerH}:{timerM}:{timerS}'
            self.studyLabel = studyLabels[studyLabelIndex]

        if self.studyLabel == 'Focus Time' and self.studyLabelNum == '00:00:00':
            app.TimerPage.endTimerSound.play()
            self.countOne = True
            self.pomodoroList.append('Focus Time')
            if len(self.pomodoroList) == 4: 
                app.TimerPage.focusTimerRun, app.TimerPage.shortTimerRun, app.TimerPage.longTimerRun = False, False, True
                self.pomodoroList = []   
                app.FocusTimePage.studyIndex = 2
                self.Labels = copy.deepcopy(app.FocusTimePage.labels)
            else:
                app.TimerPage.focusTimerRun, app.TimerPage.shortTimerRun, app.TimerPage.longTimerRun = False, True, False
                app.FocusTimePage.studyIndex = 1
                self.Labels = copy.deepcopy(app.FocusTimePage.labels)
        elif (self.studyLabel == 'Short Break' or self.studyLabel == 'Long Break') and self.studyLabelNum == '00:00:00':
            app.TimerPage.endTimerSound.play()
            app.TimerPage.focusTimerRun, app.TimerPage.shortTimerRun, app.TimerPage.longTimerRun = False, False, False 
            self.Labels = copy.deepcopy(app.FocusTimePage.labels)
            self.studyLabel = studyLabels[0] 
            self.studyLabelNum = f'{self.Labels[0]}:{self.Labels[1]}:{self.Labels[2]}'
            
        if app.TimerPage.focusTimerRun: self.mainColor = rgb(252, 242, 239)
        elif app.TimerPage.shortTimerRun: self.mainColor = rgb(248, 247, 221)
        elif app.TimerPage.longTimerRun: self.mainColor = rgb(231, 243, 232)
        else: self.mainColor = rgb(246, 246, 246)

    def draw(self, app):
        drawRect(app.width/2, 0, app.width, app.height//3, align = 'top', fill = self.mainColor)
        drawLine(0, 330, app.width, 330, fill = rgb(200, 200, 200))
        drawLabel(f'{currentTime.month}/{currentTime.day}/{currentTime.year}', app.width//2, 50, size = 22, font ='monospace')
        drawLabel(self.studyLabel, app.width*2/3, 100, size = 18, bold = True, font = 'monospace')
        drawLabel(self.studyLabelNum, app.width*2/3, 140, size = 40, bold = True, font = 'monospace')
        drawLabel(f'Now   {currentTimehour}:{currentTimeminute}', app.width*2/3, 180, size = 14, font = 'monospace')
        drawRegularPolygon(app.width*2/3-10, 180, 5, 3, rotateAngle = 90, align = 'center')

        drawLabel('Timer', app.width/4, 300, size = 20, bold = self.timer, font = 'monospace')
        drawLabel('Report', app.width/2, 300, size = 20, bold = self.report, font = 'monospace')
        drawLabel('Calendar', app.width*3/4, 300, size = 20, bold = self.calendar, font = 'monospace')

    def press(self, app, mouseX, mouseY):
        if 335 <= mouseX <= 435 and 270 <= mouseY <= 330:
            self.timer, self.report, self.calendar = True, False, False
        if 720 <= mouseX <= 820 and 270 <= mouseY <= 330:
            self.timer, self.report, self.calendar = False, True, False
        if 1105 <= mouseX <= 1205 and 270 <= mouseY <= 330:
            self.timer, self.report, self.calendar = False, False, True
        if self.focus == True:
            self.timer, self.report, self.calendar = True, False, False
            if not (app.width/2-225 <= mouseX <= app.width/2+225
                    and app.height/2-225 <= mouseY <= app.height/2+225):
                self.Labels = copy.deepcopy(app.FocusTimePage.labels)
                self.studyLabelNum = f'{app.FocusTimePage.labels[0]}:{app.FocusTimePage.labels[1]}:{app.FocusTimePage.labels[2]}'
                self.focus = False
        if self.focus == False and (930 < mouseX < 1140 and 100 < mouseY < 180):
            self.focus = True
        if app.TimerPage.subjectAddPage == True:
            self.timer, self.report, self.calendar = True, False, False
        if app.CalendarPage.longestConsecutiveTime == True:
            self.timer, self.report, self.calendar = False, False, True 