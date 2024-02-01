from tkinter import *
import tkinter as tk
import math

def end(event):
    root.destroy()
    root2.destroy()

def get_a():
    global a
    if str(input_a.get()).isalpha() == False and str(input_a.get()) != "":
        a = float(input_a.get())
        warning_a.place(y=-50,x=120)
    else:
        warning_a.place(y=3,x=115)

def get_tg():
    global scanspeed
    if str(input_tg.get()).isalpha() == False and str(input_tg.get()) != "":
        scanspeed = 46/float(input_tg.get())
        warning_tg.place(y=-50,x=120)
    else:
        warning_tg.place(y=height/4+20,x=width-75)

def get_tw():
    global wavespeed
    if str(input_tw.get()).isalpha() == False and str(input_tw.get()) != "":
        wavespeed = 46/float(input_tw.get())
        warning_tw.place(y=-50,x=120)
    else:
        warning_tw.place(y=59,x=width-75)

def clear():
    for line in line_set:
        canvas_graph.delete(line)
    line_set.clear()
    linex_list.clear()
    liney_list.clear()
    linex_list.append(2)

def activate_wave():
    global waveactivate
    if len(ball_list) > 0 and len(linex_list) >= 2:
        wave_list.append(canvas_wave.create_line(0, 0, 0, 900, width=3))
        waveactivate=True

def morethan_ball(wavelinex_list):
    ball_x = set()
    for ball in ball_list:
        if canvas_wave.coords(ball)[0] < width:
            ball_x.add(canvas_wave.coords(ball)[0])
    if wavelinex_list > max(ball_x):
        return True

def run_wave():
    global waveactivate
    for waveline in wave_list:
        canvas_wave.move(waveline,wavespeed,0)
        for ball in (set(ball_list)-set(moveball_list)):
            if (canvas_wave.coords(ball))[0]-wavespeed/2 <= (canvas_wave.coords(waveline))[0] < (canvas_wave.coords(ball))[0]+wavespeed/2:
                moveball_list.append(ball)
        if canvas_wave.coords(waveline)[0] > width or morethan_ball(canvas_wave.coords(waveline)[0]) == True:
            wave_list.remove(waveline)
            canvas_wave.delete(waveline)
        if len(wave_list) == 0:
            waveactivate = False
    canvas_wave.after(25,run_wave)

def run_ball():
    if len(moveball_list) >= 1:  
        for ball in moveball_list:
            xscan_list[ball_list.index(ball)] += scanspeed
            if len(linex_list) >= 2:
                if xscan_list[ball_list.index(ball)] >= width or xscan_list[ball_list.index(ball)] > max(linex_list):
                    xpos_list[ball_list.index(ball)] = canvas_wave.coords(ball)[0]+1
                    moveball_list.remove(ball)
                    xscan_list[ball_list.index(ball)] = 0
                if xscan_list[ball_list.index(ball)] > 0:
                    canvas_wave.moveto(ball, get_y(xscan_list[ball_list.index(ball)])+xpos_list[ball_list.index(ball)]+1,canvas_wave.coords(ball)[1]-1)
                    
    canvas_wave.after(25,run_ball)

def get_y(x):
    closestx = min(linex_list,key = lambda z: abs(z-x))
    if x > closestx:
        closestx2=linex_list[linex_list.index(closestx)+1]
    elif x <= closestx:
        closestx2=linex_list[linex_list.index(closestx)-1]
    closesty = liney_list[linex_list.index(closestx)]
    closesty2 = liney_list[linex_list.index(closestx2)]
    m = (closesty-closesty2)/(closestx-closestx2)
    c = closesty-m*closestx
    y = m*x+c
    y = 20*(-y + (height/4-25))*a/(height/4-25)
    #y = (a(height-100))/(4*a+height-100)
    return y

def dragball(e):
    closest_ball = canvas_wave.find_closest(e.x+7,e.y+7)
    if math.sqrt(pow(int(e.x)-int(canvas_wave.coords(closest_ball)[0]+7),2)+pow(int(e.y)-int(canvas_wave.coords(closest_ball)[1]+7),2)) <= 14:
        canvas_wave.moveto(closest_ball,e.x-7,e.y-7)
        xpos_list[ball_list.index(closest_ball[0])] = canvas_wave.coords(closest_ball)[0]

def addball(e):
    if waveactivate == False:
        closest_ball = canvas_wave.find_closest(e.x+7,e.y+7)
        try:
            if math.sqrt(pow(int(e.x)-int(canvas_wave.coords(closest_ball)[0]+7),2)+pow(int(e.y)-int(canvas_wave.coords(closest_ball)[1]+7),2)) > 14:
                ball = canvas_wave.create_oval(e.x-7, e.y-7, e.x+7, e.y+7,fill='black')
        except IndexError:
            ball = canvas_wave.create_oval(e.x-7, e.y-7, e.x+7, e.y+7,fill='black')
        try:
            ball_list.append(ball)
            xscan_list.append(0)
            xpos_list.append(canvas_wave.coords(ball)[0])
        except:
            pass

def delball(e):
    if waveactivate == False:
        closest_ball = canvas_wave.find_closest(e.x+7,e.y+7)
        if math.sqrt(pow(int(e.x)-int(canvas_wave.coords(closest_ball)[0]+7),2)+pow(int(e.y)-int(canvas_wave.coords(closest_ball)[1]+7),2)) < 14:
            xpos_list.pop(ball_list.index(closest_ball[0]))
            ball_list.remove(closest_ball[0])
            xscan_list.pop(0)
            canvas_wave.delete(closest_ball)


def activate_paint(e):
    if len(liney_list) == 0:
        liney_list.append(e.y)
    if e.x > linex_list[-1]:
        linex_list.append(e.x)
        liney_list.append(e.y)
        if len(linex_list) > 1:
            line = canvas_graph.create_line((linex_list[-2], liney_list[-2],linex_list[-1], liney_list[-1]), width=2)
            line_set.add(line)

root = Tk()
root2 = Tk()

width = root.winfo_screenwidth() #1536
height = root.winfo_screenheight() #864

#root1 (graph)--------------------------------------------------------------------------------------------
root.title('Draw a graph')
linex_list=[2]
liney_list=[]
line_set = set()
canvas_graph = Canvas(root,bg='#dbdede')
a = 5
graph_list=[]
scanspeed=8
button_c = tk.Button(canvas_graph, text="Clear", command=clear, width=10, height=3)
input_a = tk.Entry(canvas_graph)
button_a = tk.Button(canvas_graph, text="Amplitude",command=get_a, width=8, height=1)
warning_a = tk.Label(canvas_graph, text="*only numbers",font=("Helvetica 8 italic"),bg="#dbdede", fg="#FF5050")
button_tg = tk.Button(canvas_graph,text="Time/s",command=get_tg, width=5, height=1)
input_tg = tk.Entry(canvas_graph)
warning_tg = tk.Label(canvas_graph, text="*only numbers",font=("Helvetica 8 italic"),bg="#dbdede", fg="#FF5050")


#run_graph()
canvas_graph.bind('<1>', activate_paint)
canvas_graph.pack(expand=YES, fill=BOTH)
root.geometry("+0+410")
canvas_graph.create_line(0,height/4-25,width,height/4-25,width=2)
canvas_graph.create_oval(5,height/4-20,13,height/4-8,width=2)
button_c.place(y=height/2-106,x=1)
canvas_graph.create_window(18,14,window=input_a,height=24,width=35)
button_a.place(y=1,x=40)
canvas_graph.create_window(width-20,height/4-25,window=input_tg,height=24,width=35)
button_tg.place(x=width-45,y=height/4-9)
root.maxsize(width,int(height/2-50))
root.minsize(width,int(height/2-50))

#root2 -------------------------------------------------------------------------------------------------------------------
root2.title('Longitudinal Wave')
xscan_list = []
ball_list = []
wave_list = []
moveball_list = []
xpos_list = []
canvas_wave = Canvas(root2,bg='#dbdede')
button_r = tk.Button(canvas_wave, text="Run", command=activate_wave, width=10, height=3)
waveactivate=False
wavespeed=8
button_tw = tk.Button(canvas_wave,text="Time/s",command=get_tw, width=5, height=1)
input_tw = tk.Entry(canvas_wave)
warning_tw = tk.Label(canvas_wave, text="*only numbers",font=("Helvetica 8 italic"),bg="#dbdede", fg="#FF5050")

run_wave()
run_ball()
canvas_wave.bind('<1>',addball)
canvas_wave.bind('<3>',delball)
canvas_wave.pack(expand=YES, fill=BOTH)
canvas_wave.bind('<B1-Motion>', dragball)
button_r.place(x=0,y=0)
root2.geometry("+0+0")
root2.maxsize(width,int(height/2-50))
root2.minsize(width,int(height/2-50))
canvas_wave.create_window(width-20,13,window=input_tw,height=24,width=35)
button_tw.place(x=width-45,y=29)

root.bind('<Escape>', end)
root2.bind('<Escape>', end)
root2.mainloop()
root.mainloop()