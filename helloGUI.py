#!/usr/bin/env python3.8
# helloGUI.py

import PySimpleGUI as sg
from qm import *

gc = [n ^ n>>1 for n in range(16)]

KMapL = lambda imps: [['1' if gc[o] in imps else '0'\
        for o in range(*[[n,n+4,1],[n+3,n-1,-1]][(n//4)%2])] for n in range(0,len(gc),4)]

'''
layout = [[sg.Text("Hello from PySimpleGUI")],
        [sg.Button("0", size=(4, 2)),sg.Button("1", size=(4, 2)),sg.Button("3", size=(4, 2)),sg.Button("2", size=(4, 2))],
        [sg.Button("4", size=(4, 2)),sg.Button("5", size=(4, 2)),sg.Button("7", size=(4, 2)),sg.Button("6", size=(4, 2))],
        [sg.Button("12", size=(4, 2)),sg.Button("13", size=(4, 2)),sg.Button("15", size=(4, 2)),sg.Button("14", size=(4, 2))],
        [sg.Button("8", size=(4, 2)),sg.Button("9", size=(4, 2)),sg.Button("11", size=(4, 2)),sg.Button("10", size=(4, 2))],
        [sg.Button("OK")]]
'''

bc = [0 for n in range(16)]
bcolors = [('white', 'green'), ('white', 'red'), ('white', 'blue')]

def getImps(bc):
    return [n for n in range(16) if bc[n] == 1]

def getDontCares(bc):
    return [n for n in range(16) if bc[n] == 2]

#-Button Layout------------------------------------------------------------------------------------
KM = [["0", "1", "3", "2"], ["4", "5", "7", "6"], ["12", "13", "15", "14"], ["8", "9", "11", "10"]]
layout = [[sg.Text("Hello from PySimpleGUI")]]

bL = []
for r in KM:
    R = []
    for c in r:
        R.append(sg.Button(c, size=(4, 2), button_color=bcolors[0], font='Any 18'))
    bL.append(R)

layout = layout + bL

layout.append([sg.Output(size=(34, 10), key="-out-")])

layout.append([sg.Button("OK")])

#-End Button Layout--------------------------------------------------------------------------------


# print(layout)

# Create the window
window = sg.Window("Demo", layout)

# Create an event loop
while True:
    event, values = window.read()
    # print(event, values)
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break
    if event in [str(n) for n in range(16)]:
        bc[int(event)] = (bc[int(event)] + 1) % 3
        window[event].update(button_color = bcolors[bc[int(event)]])
        window['-out-'].update('')
#        print("Imps:        ", getImps(bc))
        print("Unsimplified: ")
        print(tt2usop(getImps(bc)))
#        print("Don't Cares: ", getDontCares(bc))
        print(" ")
        print("Simplified: ")
        print(tt2ssop(getImps(bc), getDontCares(bc)))

window.close()
