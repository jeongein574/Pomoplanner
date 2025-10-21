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

class ReportPage:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.totalTime = 0

    def draw(self, app):
        drawRect(0, 330, app.width, app.height-330, fill='white')

        # total study time
        hour = self.totalTime // 3600
        minute = (self.totalTime - hour*3600)//60
        second = self.totalTime - hour*3600 - minute*60

        drawRect(app.width/2, app.height-50, 200, 10, fill = 'tomato', opacity = 20, align = 'center')
        drawLabel(f'Today: {hour:02}:{minute:02}:{second:02}', app.width/2, app.height-60, size = 20, font ='monospace')


        # leaderboard
        lineWidth = app.width/6
        lineX, lineY = app.width/4, app.height-130
        for i in range(3):
            if i == 1:
                lineY = app.height - 155
            drawLine(lineX, lineY, lineX + lineWidth, lineY, fill = rgb(200, 200, 200))
            lineX += app.width/6
            lineY += 50
        drawLine(lineX - lineWidth*2, lineY-100, lineX - lineWidth*2, lineY-75, fill = rgb(200, 200, 200))
        drawLine(lineX - lineWidth, lineY-100, lineX - lineWidth, lineY-50, fill = rgb(200, 200, 200))

        leaderboard = []
        subjectComparison = []

        for subjectSubList in app.TimerPage.subjectList:
            subjectSecond = int(subjectSubList[2][6:])
            subjectMinute = int(subjectSubList[2][3:5])
            subjectHour = int(subjectSubList[2][0:2])

            subjectDuration = subjectSecond + subjectMinute*60 + subjectHour*3600

            subjectComparison.append((subjectDuration, subjectSubList))
        
        subjectComparison.sort(reverse = True)
        leaderboard = subjectComparison[:3]

        radius = [120, 80, 50]
        cx = [lineX - lineWidth*3/2, lineX - lineWidth*5/2, lineX - lineWidth/2]
        cy = [lineY-270, lineY-205, lineY-150]
        for index, (subjectDuration, subjectSubList) in enumerate(leaderboard):
            subject, color, studyTime = subjectSubList[0], subjectSubList[1], subjectSubList[2]

            x = cx[index]
            y = cy[index]
            r = radius[index]

            drawCircle(x, y, r, fill = color)
            drawCircle(x+3, y+3, r, fill = None, border = rgb(130, 130, 130))
            drawCircle(x, y-3, r, fill = None, border = rgb(130, 130, 130))
            drawCircle(x-3, y, r, fill = None, border = rgb(130, 130, 130))
            drawLabel(index+1, x, y, size = 100-index*20, font = 'monospace', fill = 'white', bold = True)
            drawLabel(studyTime, x, lineY-75+25*index, size = 15, font ='monospace', bold = True, fill = rgb(100, 100, 100))
            drawLabel(subject, x, lineY-125+25*index, size = 20, font ='monospace', bold = True, fill = rgb(100, 100, 100))