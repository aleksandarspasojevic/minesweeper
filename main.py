import numpy as np
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import random

root = tk.Tk()

canvas_width = 560
canvas_height = 560
r = canvas_height//16

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.config(bg='#%02x%02x%02x' % (100, 100, 100))
canvas.pack()

matrix = np.arange(16*16).reshape(16, 16)
visited = np.arange(16*16).reshape(16, 16)
buttons = np.arange(16*16).reshape(16, 16)
flags = np.empty(16*16, dtype=object).reshape(16, 16)
flags[:] = None

image = Image.open('bomb.png')
image = image.resize((r-10, r-10), Image.ANTIALIAS)
img = ImageTk.PhotoImage(image)

image1 = Image.open('flag.png')
image1 = image1.resize((r-10, r-10), Image.ANTIALIAS)
flagImg = ImageTk.PhotoImage(image1)
gameOver = False

def plantMines(numMines):
    global matrix
    while(numMines>0):
        r= random.randint(0,15)
        c= random.randint(0,15)
        if(not matrix[r][c]):
            numMines-=1
            matrix[r][c]=-1


def clearMatrix():
    global matrix
    for i in range(0, 16):
        for j in range(0, 16):
            matrix[i][j]=0
            visited[i][j]=False


def constrain(num, low, high):
    num1 = num if num>=low else low
    num1 = num1 if num1<=high else high
    return num1

def setFields():
    global matrix

    for i in range(0, 16):
        for j in range(0, 16):
            if(matrix[i][j]!=-1):
                cntMines=0
                for c in range(constrain(i-1, 0, 16), constrain(i+2, 0, 16)):
                    for d in range(constrain(j-1, 0, 16), constrain(j+2, 0,16)):
                        if(matrix[c][d]==-1):
                            cntMines+=1
                matrix[i][j]=cntMines

def openField(i, j):
    i=constrain(i, 0, 15)
    j=constrain(j, 0, 15)
    if not matrix[i][j] == 0:
        canvas.itemconfig(buttons[i][j], fill='grey')
        mylabel = canvas.create_text((i * r + r / 2, j * r + r / 2), text=matrix[i][j], font=("Courier", 15),
                                     fill='white')

def openFields(i, j):
    global matrix
    global visited
    visited[i][j]=True
    canvas.itemconfig(buttons[i][j], fill='grey')
    openField(i + 1, j)
    openField(i + 1, j + 1)
    openField(i + 1, j - 1)

    openField(i - 1, j)
    openField(i - 1, j - 1)
    openField(i - 1, j + 1)

    openField(i, j - 1)
    openField(i, j + 1)

    if matrix[constrain(i - 1, 0, 15)][j] == 0 and not visited[constrain(i - 1, 0, 15)][j]:
        openFields(constrain(i-1, 0, 15), j)
    if matrix[i][constrain(j+1, 0, 15)] == 0 and not visited[i][constrain(j + 1, 0, 15)]:
        openFields(i, constrain(j+1, 0, 15))
    if matrix[constrain(i+1, 0, 15)][j] == 0 and not visited[constrain(i + 1, 0, 15)][j]:
        openFields(constrain(i+1, 0, 15), j)
    if matrix[i][constrain(j-1, 0, 15)] == 0 and not visited[i][constrain(j - 1, 0, 15)]:
        openFields(i, constrain(j-1, 0, 15))

    if matrix[constrain(i - 1, 0, 15)][constrain(j+1, 0,15)] == 0 and not visited[constrain(i - 1, 0, 15)][constrain(j+1, 0,15)]:
        openFields(constrain(i-1, 0, 15), j+1)
    if matrix[constrain(i+1, 0,15)][constrain(j+1, 0, 15)] == 0 and not visited[constrain(i+1, 0,15)][constrain(j + 1, 0, 15)]:
        openFields(constrain(i+1, 0,15), constrain(j+1, 0, 15))
    if matrix[constrain(i+1, 0, 15)][constrain(j-1, 0,15)] == 0 and not visited[constrain(i + 1, 0, 15)][constrain(j-1, 0,15)]:
        openFields(constrain(i+1, 0, 15), constrain(j-1, 0,15))
    if matrix[i-1][constrain(j-1, 0, 15)] == 0 and not visited[i-1][constrain(j - 1, 0, 15)]:
        openFields(constrain(i-1, 0,15), constrain(j-1, 0, 15))

def pickField(event):
    global visited, gameOver, flags
    row = event.x // r
    col = event.y // r

    if event.num==1:
        if not visited[row][col]:
            visited[row][col] = True
            if (matrix[row][col] == 0):
                openFields(row, col)
            elif matrix[row][col] == -1:
                print("GAME OVER")
                gameOver = True
                canvas.itemconfig(buttons[row][col], fill='red')
                canvas.create_image(row * r + 5, col * r + 5, anchor=NW, image=img)
                # canvas.itemconfig(buttons[row][col], fill='red')

            else:
                canvas.itemconfig(buttons[row][col], fill='grey')
                mylabel = canvas.create_text((row * r + r / 2, col * r + r / 2), text=matrix[row][col],
                                             font=("Courier", 15), fill='white')

        if gameOver:
            for i in range(0, 16):
                for j in range(0, 16):
                    if matrix[i][j] == -1:
                        canvas.create_image(i * r + 5, j * r + 5, anchor=NW, image=img)
            root.unbind("<Button>")

        canvas.update()

    elif event.num == 3:
        if flags[row][col] is None:
            canvas.itemconfig(buttons[row][col], fill='grey')
            flags[row][col] = canvas.create_image(row * r + 5, col * r + 5, anchor=NW, image=flagImg)
        else:
            canvas.delete(flags[row][col])
            canvas.itemconfig(buttons[row][col], fill='#%02x%02x%02x' % (100, 100, 100))
            flags[row][col]= None





if __name__ == '__main__':
   clearMatrix()
   plantMines(40)
   setFields()

   root.bind("<Button>", pickField)

   for i in range(0, 16):
       for j in range(0, 16):
           ob=canvas.create_rectangle(i*r, j*r, (i+1)*r, (j+1)*r)
           buttons[i][j]=(ob)


   root.mainloop()


