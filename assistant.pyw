#assitant 3
#On 20211019

#List of tasks which will be killed

import tkinter
import time
import os

#Constants
DELAY = 5
SDDELAY = 300
WINSTAY = 3

OF = 0
TK = 1
SD = 2

#Init GUI
root = tkinter.Tk()
root.title('提示')

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

#OK
def doOK():
    root.withdraw()
    for i in TKL:
        os.system('TASKKILL /F /PID ' + i)
        print(i + ' got killed successfully.')
#Cancel
def doCancel():
    root.withdraw()

#Read files
OFT = getTimetable('oftable')   #Time to open file
TKT = getTimetable('tktable')   #Time to taskkill
SDT = getTimetable('sdtable')   #Time to shutdown

OFL = getList('oflist.txt')     #Get oflist from the file
TKL = getList('tklist.txt')     #Get tklist from the file


class Executor:
    '''Task killing and shutting down'''
    start = False
    processed = {OF : False, TK : False, SD : False}
    def __init__(self):
        print('Executor Enabled.')

    def openFile(self):
        #Open files on OFL
        for i in OFL:
            os.system(i)
            print(i + ' has been successfully opened.')
    
    def taskKill(self):
        #Kill tasks on TKL
        root.deiconify()
        self.start = time.localtime()
        if self.start.tm_min + WINSTAY < 60:
            hint['text'] = '是否关闭所有课件？\n（' + str(self.start.tm_hour) + '时' + str(self.start.tm_min + WINSTAY) + '分自动取消）'
        else:
            hint['text'] = '是否关闭所有课件？\n（' + str(self.start.tm_hour + 1) + '时' + str(self.start.tm_min + WINSTAY - 60) + '分自动取消）'

    def shutdown(self):
        #Shutdown the computer
        os.system('SHUTDOWN -S -T ' + str(SDDELAY))
    
    def timeCheck(self):
        #Get local time
        h = time.localtime().tm_hour
        mi = time.localtime().tm_min
        #OF
        flag = True
        for i in OFT:
            if (h, mi) == i:
                flag = False
                if not self.processed[OF]:
                    self.openFile()
        if flag:
            self.processed[OF] = False
        else:
            self.processed[OF] = True
        #TK
        flag = True
        for i in TKT:
            if (h, mi) == i:
                flag = False
                if not self.processed[TK]:
                    self.taskKill()
        if flag:
            self.processed[TK] = False
        else:
            self.processed[TK] = True
        #Check time
        if self.start:
            if time.localtime().tm_min - self.start.tm_min == WINSTAY or time.localtime().tm_min + 60 - self.start.tm_min == WINSTAY:
                doCancel()
        #SD
        flag = True
        for i in SDT:
            if h == i[0] and mi == i[1] - SDDELAY // 60:
                flag = False
                if not self.processed[SD]:
                    self.shutdown()
        if flag:
            self.processed[SD] = False
        else:
            self.processed[SD] = True

#Init executor
exer = Executor()

#Main loop
def main():
    #Check the switch
    S = open('switch.txt')
    if S.read() == '0':
        os._exit(0)
    S.close()
    #Check time
    exer.timeCheck()
    #Do loops
    root.after(DELAY * 1000, main)

#Init components
hint = tkinter.Label(root, font = ('微软雅黑', 24), height = 2, width = 30, text = '启动中……')
ok = tkinter.Button(root, font = ('微软雅黑', 36, 'bold'), height = 1, width = 20, text = '确认', command = doOK)
cancel  = tkinter.Button(root, bg = 'red', font = ('微软雅黑', 36, 'bold'), height = 1, width = 20, text = '取消', command = doCancel)
#Pack components
hint.pack()
ok.pack()
cancel.pack()
#Start running
root.withdraw()
root.after(0, main)
root.mainloop()
