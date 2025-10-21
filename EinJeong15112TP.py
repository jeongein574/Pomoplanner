from cmu_graphics import *
import datetime
import calendar
import copy
import json
from PIL import Image
import os, pathlib

from focusTimeFile import FocusTimePage
from mainFile import MainPage
from calendarFile import CalendarPage
from longestConsecutiveTimeFile import LongestConsecutiveTimePage
from reportFile import ReportPage
from timerFile import TimerPage
from subjectAddFile import SubjectAddPage
from taskAddFile import TaskAddPage

currentTime = datetime.datetime.now()
currentTimehour = f'0{currentTime.hour}' if currentTime.hour < 10 else str(currentTime.hour)
currentTimeminute = f'0{currentTime.minute}' if currentTime.minute < 10 else str(currentTime.minute)

year = currentTime.year
month = currentTime.month        

#---Animation functions---------------------------------
def onAppStart(app):
    app.stepsPerSecond = 1
    app.timerCount = 0
    app.mainDisplay = True
    app.FocusTimePage = FocusTimePage(app.width, app.height)
    app.MainPage = MainPage(app.width, app.height, app.FocusTimePage)
    app.TimerPage = TimerPage(app.width, app.height)
    app.TimerPage.loadSubjects()
    app.ReportPage = ReportPage(app.width, app.height)
    app.CalendarPage = CalendarPage(app.width, app.height)
    app.CalendarPage.loadSchedule(app)
    app.SubjectAddPage = SubjectAddPage(app.width, app.height)
    app.LongestConsecutiveTimePage = LongestConsecutiveTimePage(app.width, app.height)
    app.TaskAddPage = TaskAddPage(app.width, app.height)
    
    app.tomato = Image.open(os.path.join(pathlib.Path(__file__).parent,"Images\\tomato1.png"))
    app.tomatoWidth, app.tomatoHeight = app.tomato.width, app.tomato.height
    app.tomato = CMUImage(app.tomato)

    timerGif = Image.open('Images\\timerGif.gif')
    app.timerSprite = []
    for frame in range(timerGif.n_frames):
        timerGif.seek(frame)
        fr = timerGif.resize((timerGif.size[0]//4, timerGif.size[1]//4))
        fr = CMUImage(fr)
        app.timerSprite.append(fr)
    app.timerSprite.pop(0)
    app.spriteCounter = 0
    app.oneSec = 1

def onMousePress(app, mouseX, mouseY):
    app.MainPage.press(app, mouseX, mouseY)
    if app.MainPage.focus:
        app.FocusTimePage.press(app, mouseX, mouseY)
    if app.MainPage.calendar:
        app.CalendarPage.press(app, mouseX, mouseY)
    if app.CalendarPage.longestConsecutiveTime:
        app.LongestConsecutiveTimePage.press(app, mouseX, mouseY)
    if app.MainPage.timer:
        app.TimerPage.press(app, mouseX, mouseY)
    if app.TimerPage.subjectAddPage:
        app.SubjectAddPage.press(app, mouseX, mouseY)
    if app.MainPage.taskAdd:
        app.TaskAddPage.press(app, mouseX, mouseY)

def onStep(app):
    app.spriteCounter = (app.spriteCounter + 1) % len(app.timerSprite)

    app.MainPage.timerLabel(app)
    global currentTime, currentTimehour, currentTimeminute
    currentTime = datetime.datetime.now()
    currentTimehour = f'0{currentTime.hour}' if currentTime.hour < 10 else str(currentTime.hour)
    currentTimeminute = f'0{currentTime.minute}' if currentTime.minute < 10 else str(currentTime.minute)
    app.MainPage.taskAdd = app.CalendarPage.taskAdd 
        
    if (app.TimerPage.focusTimerRun == True and app.TimerPage.activeSubjectIndex is not None) or app.MainPage.countOne:
        app.MainPage.countOne = False
        subjectList = [subject for subject in app.TimerPage.subjectList if subject[4] == True]
        subjectSubList = subjectList[app.TimerPage.activeSubjectIndex]
        
        subjectSecond = int(subjectSubList[2][6:])
        subjectMinute = int(subjectSubList[2][3:5])
        subjectHour = int(subjectSubList[2][0:2])
        
        subjectSecond += 1 
        if subjectSecond >= 60:
            subjectSecond = 0
            subjectMinute += 1
        if subjectMinute >= 60:
            subjectMinute = 0
            subjectHour += 1

        if subjectHour < 10: studyHour = f'0{str(subjectHour)}'
        else: studyHour = str(subjectHour)
        if subjectMinute < 10: studyMinute = f'0{str(subjectMinute)}'
        else: studyMinute = str(subjectMinute)
        if subjectSecond < 10: studySecond = f'0{str(subjectSecond)}'
        else: studySecond = str(subjectSecond)

        subjectSubList[2] = f'{studyHour}:{studyMinute}:{studySecond}'

        app.ReportPage.totalTime += 1

    if app.CalendarPage.invalidTask == True:
        app.CalendarPage.count += 1
        if app.CalendarPage.count >= 4:
            app.CalendarPage.invalidTask = False
            app.CalendarPage.count = 0

def redrawAll(app):
    app.MainPage.draw(app)
    
    if app.MainPage.timer:
        app.TimerPage.draw(app)

    x, y = app.width/3, 130
    drawImage(app.tomato, x, y, align = 'center', width = app.tomatoWidth//5, height = app.tomatoHeight//5)
    if app.TimerPage.focusTimerRun == True:
        drawImage(app.timerSprite[app.spriteCounter], x, y+10, align = 'center')

    if app.MainPage.report:
        app.ReportPage.draw(app)
    if app.MainPage.calendar:
        app.CalendarPage.draw(app)
    if app.MainPage.focus:
        app.FocusTimePage.draw(app)
    if app.TimerPage.subjectAddPage:
        app.SubjectAddPage.draw(app)
    if app.CalendarPage.longestConsecutiveTime:
        app.LongestConsecutiveTimePage.draw(app)
    if app.MainPage.taskAdd:
        app.TaskAddPage.draw(app)

def onKeyPress(app, key):
    if app.TimerPage:
        if key == 'down':
            app.TimerPage.lastVisible = min(app.TimerPage.lastVisible + 1, len(app.TimerPage.subjectList)-1)
        if key == 'up':
            app.TimerPage.lastVisible = max(app.TimerPage.lastVisible -1, 4)
        for idx, subjectSubList in enumerate(app.TimerPage.subjectList):
            if app.TimerPage.lastVisible - 4 <= idx <= app.TimerPage.lastVisible:
                subjectSubList[4] = True
            else:
                subjectSubList[4] = False

    if app.CalendarPage:
        if key == 'down':
            app.CalendarPage.lastVisibleTask = min(app.CalendarPage.lastVisibleTask + 1, len(app.CalendarPage.schedule)-1)
        if key == 'up':
            app.CalendarPage.lastVisibleTask = max(app.CalendarPage.lastVisibleTask -1, 7)
        for idx, task in enumerate(app.CalendarPage.schedule):
            if app.CalendarPage.lastVisibleTask - 7 <= idx <= app.CalendarPage.lastVisibleTask:
                task = list(task)
                task[5] = True
                task = tuple(task)
                app.CalendarPage.schedule[idx] = task

            else:
                task = list(task)
                task[5] = False
                task = tuple(task)
                app.CalendarPage.schedule[idx] = task

runApp(width = 1540, height = 800)

