from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
matplotlib.use('TkAgg')
import pandas as pd

def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

sg.change_look_and_feel('Reddit')

tab1_layout = [[sg.Text('Type',size=(25,1)),sg.InputText()],
               [sg.Text('Date',size=(25,1)),sg.CalendarButton(button_text='..',tooltip='Select Date in Calendar')],
               [sg.Text('Amount',size=(25,1)),sg.InputText()],
               [sg.Button('Submit',tooltip='Submit Entry'),sg.Button('Exit',tooltip='Close')],
              ]

tab2_layout =  [[sg.Button('Show Expenses')],[sg.Output(size=(60,20),text_color='blue')]]

tab3_layout = [[sg.Button('Plot',tooltip='Show graph')],
               [sg.Canvas(key='canvas')],
              ]

layout2 = [[sg.TabGroup([[sg.Tab('Home',tab1_layout),sg.Tab('My Expenses',tab2_layout),sg.Tab('Analytics',tab3_layout)]])]]
window = sg.Window('Expense Tracker',layout2).Finalize()
str1=''
exp = []
act = False
i=0
cnt=0
a = []
b = []
cost = 0
temp = []
while True:
    event,values = window.read()
    if event is None or event=='Exit':
        break
    elif event=='Submit':
        exp.append([values[0],values['..'],int(values[1])])
        cnt = cnt+1
    elif event=='Show Expenses':
            for i in range(0,cnt):
                str1 = str1+' Date: '+str(exp[i][1].day)+'/'+str(exp[i][1].month)+'/'+str(exp[i][1].year)+'    |  Type: '+exp[i][0]+'    Amount: '+str(exp[i][2])+'\n--------------------------------------------------------------------------------------\n'
            print(str1)
            str1=''
    elif event=='Plot':
        tp = pd.DataFrame(exp)
        for i in range(0,tp.last_valid_index()+1):
            cost = tp[2][i]
            temp = []
            for j in range(i+1,tp.last_valid_index()+1):
                if j<=tp.last_valid_index():
                    if tp[0][j]==tp[0][i]:
                        cost = cost + tp[2][j]
                        temp.append(j)
            if b.count(i)<1:
                a.append([tp[0][i],cost])
                b.append(temp)
        df = pd.DataFrame(a)
        plt.bar(df[:][0],df[:][1])
        plt.ylabel('Amount in Rs')
        fig = plt.gcf()
        fig_canvas_agg = draw_figure(window['canvas'].TKCanvas, fig)
window.close()