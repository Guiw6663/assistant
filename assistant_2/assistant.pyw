#assitant 2
#On 20210914

#List of tasks which will be killed

import time
import os


#Get timetables from the file
def getTimetable(r):
    t = open('lists/' + r + '/' + str(time.localtime().tm_wday + 1) + '.txt').readlines()
    for i in range(len(t)):
        t[i] = (int(t[i]) // 100, int(t[i]) % 100)
    return t

#Get timetables from the file
def getList(li):
    t = open('lists/' + li).readlines()
    for i in range(len(t)):
        t[i] = t[i].strip()
    return t

#Read files
S = open('switch.txt')
if S.read() == '0':
    os._exit(0)
S.close()

TKT = getTimetable('tktable')    #Time to shutdown
SDT = getTimetable('sdtable')    #Time to shutdown
TKL = getList('tklist.txt')     #Get timetables from the file


#Task killing and shuting down
class Executor:
    def __init__(self):
        print('Taskkiller Enabled.')
    
    def taskKill(self):
        #Kill all tasks on TKL
        for i in range(len(TKL)):
            os.system('TASKKILL /F /PID ' + TKL[i])
            print(TKL[i] + ' got killed successfully.')

    def shutdown(self):
        #Shutdown the computer
        os.system('SHUTDOWN -S -T 300')
    
    def timeCheck(self):
        #Get local time
        h = time.localtime().tm_hour
        mi = time.localtime().tm_min

        for i in range(len(TKT)):
            if (h, mi) == TKT[i]:
                self.taskKill()
        for i in range(len(SDT)):
            if h == SDT[0] and mi == SDT[1] - 5:
                self.shutdown()

#Init executor
exer = Executor()

#Main loop
while True:
    #Check time
    exer.timeCheck()

    #Delay
    time.sleep(30)

    #print(time.clock())
