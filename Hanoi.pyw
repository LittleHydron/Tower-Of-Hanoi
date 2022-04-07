from tkinter import *
import tkinter.messagebox
import time

## Global Constants
NumberOfDisks = 0
HeightOfDisk = 20
UnitOfDiskWidth = 50
StepOfDisk = UnitOfDiskWidth / 10
SleepTime = 0.01
## ---------------

## Asking a number:
root = Tk()
root.title('HTS')
root.resizable(0, 0)
btn = Button(root, text = 'Ок')
entry = Entry(root)
lbl = Label(root, text = 'Введіть кількість дисків (натуральне число, менше 10)')
lbl.pack()
entry.pack()
btn.pack()

def Try(event = None):
    n = entry.get()
    if not n.isdigit() or int(n) > 9:
        tkinter.messagebox.showerror("Блін...", "Треба написати натуральне число, менше 10")
        return
    global NumberOfDisks
    NumberOfDisks = int(n)
    root.destroy()

btn['command'] = Try
entry.bind_all('<KeyPress-Return>', Try)

root.mainloop()
## ------------------------------------------------

## Drawing a main window:

root = Tk()
root.title('Hanoi Tower Solver')

ScreenHeight = int(NumberOfDisks * HeightOfDisk + 100)
ScreenWidth = int(NumberOfDisks * UnitOfDiskWidth * 3)

root.geometry(str(ScreenWidth) + 'x' + str(ScreenHeight) + '+' + str(int(683 - ScreenWidth/2)) + '+' + str(int(384 - ScreenHeight/2)))

root.resizable(0, 0)

canvas = Canvas(root)
canvas.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)

class Rod:
    def __init__(self, canvas, number):
        global NumberOfDisks, HeightOfDisk, UnitOfDiskWidth, ScreenHeight, ScreenWidth
        self.canvas = canvas
        self.horizontalWidth = (NumberOfDisks) * UnitOfDiskWidth
        self.horizontalX = (number-1) * self.horizontalWidth
        self.horizontalY = ScreenHeight - HeightOfDisk
        self.horizontal = self.canvas.create_rectangle(self.horizontalX, self.horizontalY, self.horizontalX + self.horizontalWidth, self.horizontalY + HeightOfDisk, fill = 'brown')
        self.verticalX = self.horizontalX + self.horizontalWidth/2 - HeightOfDisk/2
        self.verticalHeight = (0.5 + NumberOfDisks) * HeightOfDisk
        self.verticalY = self.horizontalY - (self.verticalHeight)
        self.countDisks = 0
        self.vertical = self.canvas.create_rectangle(self.verticalX, self.verticalY, self.verticalX + HeightOfDisk, self.verticalY + self.verticalHeight, fill = 'brown')

Rods = [Rod(canvas, 1), Rod(canvas, 2), Rod(canvas, 3)]
Rods[0].countDisks = NumberOfDisks

Disks = list()
color = ['blue', 'red', 'yellow', 'green', 'purple', 'azure','silver', 'orange', 'beige']

class Disk:
    def __init__(self, canvas, number):
        global Rods, UnitOfDiskWidth, HeightOfDisk, NumberOfDisks, color
        self.number = number
        self.canvas = canvas
        self.xpos = Rods[0].horizontalX + number * UnitOfDiskWidth / 2
        self.ypos = Rods[0].horizontalY - (number + 1) * HeightOfDisk
        self.id = self.canvas.create_rectangle(self.xpos, self.ypos, self.xpos + (NumberOfDisks - number)*UnitOfDiskWidth, self.ypos + HeightOfDisk, fill = color[number])

    def Move(self, a, c):
        global HeightOfDisk, Rods, StepOfDisk, NumberOfDisks, SleepTime, root
        print(f"{NumberOfDisks - self.number}: {a} -> {c}")
        while self.ypos - HeightOfDisk >= Rods[a-1].verticalY - 2*HeightOfDisk:
            self.ypos -= StepOfDisk
            self.canvas.move(self.id, 0, - StepOfDisk)
            time.sleep(SleepTime)
            root.update_idletasks()
        requiredX = Rods[c-1].horizontalX + self.number * UnitOfDiskWidth / 2
        
        while self.xpos < requiredX:
            self.xpos += StepOfDisk
            self.canvas.move(self.id, StepOfDisk, 0)
            time.sleep(SleepTime)
            root.update_idletasks()

        while self.xpos > requiredX:
            self.xpos -= StepOfDisk
            self.canvas.move(self.id, -StepOfDisk, 0)
            time.sleep(SleepTime)
            root.update_idletasks()

        while self.ypos < Rods[c-1].horizontalY - (Rods[c-1].countDisks + 1) * HeightOfDisk:
            self.ypos += StepOfDisk
            self.canvas.move(self.id, 0, StepOfDisk)
            time.sleep(SleepTime)
            root.update_idletasks()
        Rods[a-1].countDisks -= 1
        Rods[c-1].countDisks += 1

for i in range(0, NumberOfDisks):
    Disks.append(Disk(canvas, i))

def MoveDisk(size, a, c):
    global Disks, NumberOfDisks
    numberOfDisk = NumberOfDisks - size
    Disks[numberOfDisk].Move(a, c)

def solve(n, a, b, c):
    if n == 0: return
    solve(n-1, a, c, b)
    MoveDisk(n, a, c)
    solve(n-1, b, a, c)

def Solve():
    global NumberOfDisks, Stop, root
    solve(NumberOfDisks, 1, 2, 3)
    tkinter.messagebox.showinfo(title='Вітаю!', message='Магія відбулася успішно!')
    root.destroy()

btn = Button(root, text='Почати магію', command = Solve)
btn.pack()
root.mainloop()
## --------------------------------------------------
