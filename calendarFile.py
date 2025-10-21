from cmu_graphics import *
import datetime
import calendar
import copy
import json
import os

currentTime = datetime.datetime.now()
currentTimehour = f'0{currentTime.hour}' if currentTime.hour < 10 else str(currentTime.hour)
currentTimeminute = f'0{currentTime.minute}' if currentTime.minute < 10 else str(currentTime.minute)

year = currentTime.year
month = currentTime.month 

class CalendarPage:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.longestConsecutiveTime = False
        self.taskAdd = False
        self.schedule = []
        self.todayList = []
        self.taskAddTime = 0
        self.taskAddHour, self.taskAddMinute = 0, 0
        self.invalidTask = False
        self.count = 0
        self.selectedDay = currentTime.day
        self.currentDate = f'{currentTime.month}/{currentTime.day}/{currentTime.year}'
        self.lastVisibleTask = 7

    def saveSchedule(self):
        date = f'{currentTime.month}/{currentTime.day}/{currentTime.year}'
        data = {"date": date, "tasks": self.schedule}
        if not os.path.exists("saveTasks.json"):
            with open("saveTasks.json", "w") as f:
                json.dump([], f)

        with open("saveTasks.json", "r+") as f:
            try:
                existingData = json.load(f)
            except json.JSONDecodeError:
                existingData = []

            index = next((i for i, entry in enumerate(existingData) if entry.get("date") == date), None)

            if index is not None:
                existingData[index] = data
            else:
                existingData.append(data)

            f.seek(0)
            f.truncate()
            json.dump(existingData, f, indent=2)
    
    def loadSchedule(self, app):
        try:
            with open("saveTasks.json", "r") as f:
                data = json.load(f)
                for tasks in data:
                    date = tasks['date']
                    task = tasks['tasks']
                    if date == self.currentDate:
                        self.schedule = task
                        break
                    else:
                        self.schedule = []    
        except FileNotFoundError:
            self.schedule = []

    def draw(self, app):
        drawRect(0, 330, app.width, app.height-330, fill='white')
        drawLine(app.width/2, 340, app.width/2, app.height-30, fill = rgb(200, 200, 200))

        #calendar
        calendarView = calendar.month(year, month)
        lines = calendarView.split('\n')
        title = lines[0].strip()
        dayName = lines[1].strip()
        drawRect(428, 540, 310, 360, fill = None, border = rgb(200, 200, 200), align = 'center')  
        drawRect(428, app.height/2-10, 300, 50, fill=gradient(rgb(250, 250, 250), rgb(220, 220, 220), start='top'), 
                 border = rgb(220, 220, 220), borderWidth = 1, align = 'center')
        drawLabel(title, 428, app.height/2-10, font = 'monospace', size = 20, italic = True)
        drawLabel(dayName, 428, app.height/2+40, font = 'monospace', size = 22)
        drawRegularPolygon(328, app.height/2-10, 5, 3, rotateAngle = -90, align = 'center', fill = 'dimGray')
        drawRegularPolygon(528, app.height/2-10, 5, 3, rotateAngle = 90, align = 'center', fill = 'dimGray')

        cellWidth = 40
        cellHeight = 40
        gridX = 288
        gridY = app.height / 2 + 25

        for i in range(2, len(lines)):
            dayLine = lines[i].split()
            if i == 2 and len(dayLine) < 7:
                dayLine = ["0"] * (7 - len(dayLine)) + dayLine
            for j, day in enumerate(dayLine):
                if day.isdigit():
                    cellX = gridX + j * cellWidth
                    cellY = gridY + (i - 1) * cellHeight
                    if int(day) == self.selectedDay:
                        drawRect(cellX, cellY, cellWidth, cellHeight, fill=gradient('tomato', 'coral', 'lightSalmon', 'seashell', 'white'), opacity = 40, border=None)
                    else:
                        drawRect(cellX, cellY, cellWidth, cellHeight, fill=None, border=None)
                    
                    if day != "0":
                        drawLabel(day, cellX + cellWidth / 2, cellY + cellHeight / 2, font='monospace', size=18)
        
        #longestConsecutiveTime
        for i in range(3):
            buttonX = app.width-70
            buttonY = app.height-120+5*i
            drawLine(buttonX, buttonY, buttonX+20, buttonY, fill = rgb(200, 200, 200))

        #taskAdd
        drawCircle(app.width-60, app.height-60, 20, fill=gradient('brown', 'tomato', 'coral', 'lightSalmon', 'seashell', start='right-bottom'))
        drawLabel('+', app.width-60, app.height-57, size = 60, fill = 'white', align = 'center')

        #task display
        deleteX = app.width/2+60
        schedule = [task for task in self.schedule if task[5] == True]
        for task in schedule:
            taskTitle, startTime, endTime, visibility = task[0], task[2], task[3], task[5]
            index = schedule.index(task)
            location = 380 + 40*index

            if visibility:
                drawLabel(taskTitle, app.width/2+120, location, font = 'monospace', size = 18, align = 'left')
                drawLabel(f'{startTime} - {endTime}', app.width-120, location, font = 'monospace', size = 18, align = 'right')
                drawRect(deleteX, location, 14, 14, fill = rgb(246, 246, 246), border = 'tomato', borderWidth = 0.5, align = 'center')
                drawLabel('X', deleteX, location, size = 12, fill = 'tomato')

        #save button
        drawRect(app.width/2+60, app.height-60, 60, 30, fill=gradient(rgb(250, 250, 250), rgb(220, 220, 220), start='top'), 
                 border = rgb(220, 220, 220), borderWidth = 1, align = 'center')
        drawLabel('Save', app.width/2+60, app.height-60, font = 'monospace', size = 18)

        #invalidTask
        if self.invalidTask == True:
            drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
            drawRect(app.width/2, app.height/2, 200, 100, fill = 'white', align = 'center', border = 'tomato')
            drawLabel('Task is not valid.', app.width/2, app.height/2-10, size = 15, font ='monospace', fill = 'tomato', bold = True)
            drawLabel('Cannot be added.', app.width/2, app.height/2+10, size = 15, font ='monospace', fill = 'tomato', bold = True)

        #scroll bar
        scrollX = app.width-60
        drawRect(scrollX, 390, 10, 230, fill=rgb(200, 200, 200), align='top')
        drawRegularPolygon(scrollX, 380, 7, 3, fill = rgb(200, 200, 200), align = 'center')        
        drawRegularPolygon(scrollX, 630, 7, 3, rotateAngle = 180, fill = rgb(200, 200, 200), align = 'center')        

    def calendarClick(self, app, mouseX, mouseY):
        cellWidth = 40
        cellHeight = 40
        gridX = 288
        gridY = app.height / 2 + 25

        calendarView = calendar.month(year, month)
        lines = calendarView.split('\n')

        for i in range(1, len(lines)):
            dayLine = lines[i].split()
            if i == 2 and len(dayLine) < 7:
                dayLine = ["0"] * (7 - len(dayLine)) + dayLine
            for j, day in enumerate(dayLine):
                if day.isdigit():
                    cellX = gridX + j * cellWidth
                    cellY = gridY + (i - 1) * cellHeight
                    if (cellX <= mouseX <= cellX + cellWidth and
                            cellY <= mouseY <= cellY + cellHeight):
                        if day != "0":
                            clickedDay = int(day)
                            clickedMonth = month
                            clickedYear = year
                            self.selectedDay = clickedDay
                            self.currentDate = f'{clickedMonth}/{clickedDay}/{clickedYear}'
                            self.loadSchedule(app)
                            break
    
    def press(self, app, mouseX, mouseY):
        global month, year

        #calendar shift
        calendarLeftX, calendarRightX, calendarY = 328, 528, 390
        if calendarLeftX-10 <= mouseX <= calendarLeftX+10 and calendarY-10 <= mouseY <= calendarY+10:
            if month != 1:
                month -= 1
            else:
                month = 12
                year -= 1

        if calendarRightX-10 <= mouseX <= calendarRightX+10 and calendarY-10 <= mouseY <= calendarY+10:
            if month != 12:
                month += 1
            else:
                month = 1
                year += 1
        
        # calendar current date
        self.currentDate = f'{currentTime.month}/{currentTime.day}/{currentTime.year}'

        if self.longestConsecutiveTime == True:
            app.MainPage.timer, app.MainPage.report, app.MainPage.calendar = False, False, True
            if not (app.width/2-225 <= mouseX <= app.width/2+225 and 
                    app.height/2-150 <= mouseY <= app.height+150):
                self.longestConsecutiveTime = False
        if self.longestConsecutiveTime == False and (app.width-70 <= mouseX <= app.width-50 
                                             and app.height-120 <= mouseY <= app.height-110):
            self.longestConsecutiveTime = True

        if self.taskAdd == True:
            app.MainPage.timer, app.MainPage.report, app.MainPage.calendar = False, False, True
            if not (app.width/2-225 <= mouseX <= app.width/2+225
                    and app.height/2-225 <= mouseY <= app.height/2+225):
                self.taskAdd = False
                
                self.taskAddHour = currentTime.hour
                self.taskAddMinute = currentTime.minute
                self.taskAddTime = int(self.taskAddHour)*60 + int(self.taskAddMinute)
                self.taskAddTime = self.taskAddTime + 15 - (self.taskAddTime % 15)
                for i in range(0, 1440-self.taskAddTime, 15): # 1440 = minute of 24:00 (= 24*60)
                    self.todayList.append(0)

                if app.TaskAddPage.optimize == True and app.TaskAddPage.optimizeTime != '00:00':
                    hour, minute = int(app.TaskAddPage.optimizeTime[:2]), int(app.TaskAddPage.optimizeTime[3:])
                    if (hour*60+minute)//15 <= len(self.todayList):
                        if self.schedule:
                            lastMinute = self.schedule[-1][3]
                            lastMinute = int(lastMinute[:2])*60 + int(lastMinute[3:])
                            if lastMinute + hour*60+minute < 1440:
                                    self.schedule.append((app.TaskAddPage.title, True, app.TaskAddPage.optimizeTime, None, app.TaskAddPage.importance, True))                                    
                            else:
                                self.invalidTask = True
                        else:
                            self.schedule.append((app.TaskAddPage.title, True, app.TaskAddPage.optimizeTime, None, app.TaskAddPage.importance, True))
                    else:
                        self.invalidTask = True
                elif app.TaskAddPage.optimize == False and app.TaskAddPage.startTime != '00:00' and app.TaskAddPage.endTime != '00:00':
                    if ((int(app.TaskAddPage.endTime[:2]) > int(app.TaskAddPage.startTime[:2])) or 
                        (int(app.TaskAddPage.endTime[:2]) == int(app.TaskAddPage.startTime[:2]) and (int(app.TaskAddPage.endTime[3:]) > int(app.TaskAddPage.startTime[3:])))):
                        self.schedule.append((app.TaskAddPage.title, False, app.TaskAddPage.startTime, app.TaskAddPage.endTime, None, True))
                    else:
                        self.invalidTask = True                    
                
                self.optimizeTask(app) 
                    
                for idx, task in enumerate(self.schedule):
                    if self.lastVisibleTask - 7 <= idx <= self.lastVisibleTask:
                        task = list(task)
                        task[5] = True
                        task = tuple(task)
                        self.schedule[idx] = task

                    else:
                        task = list(task)
                        task[5] = False
                        task = tuple(task)
                        self.schedule[idx] = task

        if self.taskAdd == False and (app.width-80 < mouseX < app.width-40 and app.height-80 < mouseY < app.height-40):
            self.taskAdd = True
            app.TaskAddPage.startTime = '00:00'
            app.TaskAddPage.endTime = '00:00'
            app.TaskAddPage.optimizeTime = '00:00'
            app.TaskAddPage.importanceBar = [0]*10
            app.TaskAddPage.title = ''
            app.TaskAddPage.optimize = False
        
        # save schedule
        saveX, saveY = app.width/2+60, app.height-60
        if (saveX-30 < mouseX < saveX+30 and saveY-15 < mouseY < saveY+15):
            self.saveSchedule()

        # delete task
        for task in self.schedule:
            index = self.schedule.index(task)
            location = 380 + 40*index
            deleteX = app.width/2+60
            if (deleteX-7 <= mouseX <= deleteX+7 and location-7 <= mouseY <= location+7):
                self.deleteTasks(index)
                break

        self.calendarClick(app, mouseX, mouseY)
          
    def optimizeTask(self, app):
        optimizeTaskList = []
        noOptimizeTaskList = []

        for task in self.schedule:
            if task[1] == True: 
                optimizeTaskList.append(task)
            elif task[1] == False:
                noOptimizeTaskList.append(task)

        self.schedule = []
        optimizeTaskList = [task for task in optimizeTaskList if len(task) >= 5]
        optimizeTaskList.sort(key=lambda x: (-x[4], x[0])) # importance, or alphabetical
        noOptimizeTaskList.sort(key=lambda x: x[2]) # startTime
        
        newOptimizeTaskList = []
        for task in optimizeTaskList:
            if task[3] is not None:
                task = list(task)
                startTime = int(task[2][:2])*60 + int(task[2][3:])
                endTime = int(task[3][:2])*60 + int(task[3][3:])
                duration = endTime - startTime
                task[2] = f'{duration // 60:02}:{duration % 60:02}'
                task[3] = None
                task = tuple(task)
            taskTitle, optimizeTime, importance = task[0], task[2], task[4]
            workMinute = int(optimizeTime[:2])*60 + int(optimizeTime[3:])
            longestWorkTime = app.LongestConsecutiveTimePage.labels
            longestMinute = int(longestWorkTime[0])*60 + int(longestWorkTime[1])

            if workMinute >= longestMinute:
                while workMinute >= longestMinute:
                    optimizeTime = f'{longestMinute // 60:02}:{longestMinute % 60:02}'
                    newTask = (taskTitle, True, optimizeTime, None, importance, True)
                    newOptimizeTaskList.append(newTask)
                    workMinute -= longestMinute

            else:
                newOptimizeTaskList.append(task)
                task = (taskTitle, True, optimizeTime, None, importance, True)
                self.schedule.append(task)

        sol = self.backtrack(newOptimizeTaskList)
        if sol is None:
            self.invalidTask = True
        
        for task in noOptimizeTaskList:
            taskTitle, startTime, endTime = task[0], task[2], task[3]
            startMinute = int(startTime[:2])*60 + int(startTime[3:])
            endMinute = int(endTime[:2])*60 + int(endTime[3:])
            startIndex = (startMinute - self.taskAddTime)//15
            endIndex = (endMinute - self.taskAddTime)//15
            
            for i in range(startIndex, endIndex+1):
                self.todayList[i] = 1
                
        self.schedule = [task for task in self.schedule if task[3] is not None]
        self.schedule.extend(noOptimizeTaskList)
        self.schedule.sort(key=lambda x: x[2]) # startTime
    
    def findZeroLengths(self, todayList, index):
        zeroLengths = []
        currentLength = 0
        for value in todayList:
            if value == 0:
                currentLength += 1
            elif value == 1 and currentLength > 0:
                zeroLengths.append(currentLength)
                currentLength = 0
        if currentLength > 0:
            zeroLengths.append(currentLength)
        if zeroLengths == []:
            zeroLengths.append(len(todayList))
        return zeroLengths
    
    def findTaskLengths(self, optimizeTasks, index):
        taskLengths = []
        for task in optimizeTasks:
            timeTaken = task[2]
            timeTakenMinute = int(timeTaken[:2])*60 + int(timeTaken[3:])
            breakMinute = 15
            taskLengths.append((timeTakenMinute + breakMinute)//15)
        return taskLengths

    def isLegal(self, currTaskLength, zeroLengths):
        for length in zeroLengths:
            if length >= currTaskLength:
                return True
                   
        return False
    
    def backtrack(self, optimizeTasks):
            
        def backTrackHelper(schedule, todayList, index):
            zeroLengths = self.findZeroLengths(todayList, index)
            taskLengths = self.findTaskLengths(optimizeTasks, index)

            if index == len(taskLengths):
                self.schedule = schedule 
                return schedule
            elif index < len(taskLengths): 
                currTaskLength = taskLengths[index]
                if self.isLegal(currTaskLength, zeroLengths):
                    for i in range(len(todayList) - currTaskLength + 1):
                        validPosition = True
                        for j in range(currTaskLength):
                            if todayList[i + j] != 0:
                                validPosition = False
                                break
                        if validPosition:
                            newTodayList = todayList[:]
                            for j in range(currTaskLength):
                                newTodayList[i + j] = 1

                            newTask = optimizeTasks[index]

                            baseTime = self.taskAddHour * 60 + 15 * (self.taskAddMinute // 15 + 1)
                            startminute = 15*i + baseTime
                            newSH, newSM = divmod(startminute, 60)
                            newTaskStartTime = f'{newSH:02}:{newSM:02}'

                            endminute = 15* (i + currTaskLength - 1) + baseTime
                            newEH, newEM = divmod(endminute, 60)
                            newTaskEndTime = f'{newEH:02}:{newEM:02}'

                            newSchedule = schedule.copy()
                            newSchedule.append((newTask[0], True, newTaskStartTime, newTaskEndTime, newTask[4], True))

                            result = backTrackHelper(newSchedule, newTodayList, index + 1)
                            if result:
                                return result
                if schedule != []:
                    schedule.pop(index)
                return None
        
        return backTrackHelper(self.schedule, self.todayList, 0)

    def deleteTasks(self, index):
        if 0 <= index < len(self.schedule):
            del self.schedule[index]
            for idx, task in enumerate(self.schedule):
                if self.lastVisibleTask - 7 <= idx <= self.lastVisibleTask:
                    task = list(task)
                    task[5] = True
                    task = tuple(task)
                    self.schedule[idx] = task

                else:
                    task = list(task)
                    task[5] = False
                    task = tuple(task)
                    self.schedule[idx] = task