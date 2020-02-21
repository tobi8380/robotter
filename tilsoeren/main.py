import matplotlib.pyplot as plt
from ur_programmer import UR_programmer
import numpy as np
from math import *
import random as rd


v_list = [0.01 * v for v in range(1,1000)]

def x(t):
    return A * cos(w1 * t + phi) + k1

def y(t):
    return B * sin(w2 * t) + k2

def minmax(x_list, y_list, limits):
    x_list = np.array(x_list)
    y_list = np.array(y_list)

    x_list -= x_list.min()
    y_list -= y_list.min()

    dy = y_list.max() - y_list.min()
    dx = x_list.max() - x_list.min()

    if dy < dx:
        scale = (limits[2]-limits[0])/x_list.max()
        print("dx")
    elif dx < dy:
        scale = (limits[3]-limits[1])/y_list.max()
        print("dy")

    x_limits = x_list * scale + limits[0]
    #print(x_limits)
    y_limits = y_list * scale + limits[1]
    #print(y_limits)
    return [x_limits,y_limits]


prog = UR_programmer("10.130.58.11", simulate=True)
prog.tegnehojde = 0.057
prog.tegne_limits = [-0.500, -0.500, -0.350, -0.350] # [x_min, y_min, x_max, y_max]

plt.gca().set_aspect('equal', adjustable='box') # sætter aspect ratio til at være 1:1

 # Her indlæses textfilen med xy koordinater
with open('path.txt','r') as file:
  filedata = file.read()

filedata = filedata.replace("\n", "")
filedata = filedata.replace(", ", ",")
filedata = filedata.replace(" ", ";")

filedata = filedata.split(",")

image_list = []
for xy in filedata:
    image_list.append(xy.split(";"))

cmd = ""
while True:
    cmd = input("kommando > ")

    if cmd == "home":
        A = 1
        w1 = 1
        phi = 0
        k1 = 0
        B = 2
        w2 = 1
        k2 = 0

        x_list = [x(t) for t in v_list]
        y_list = [y(t) for t in v_list]

        xy_list = minmax(x_list, y_list, prog.tegne_limits)

        # path_list = [[x_list[i], y_list[i]] for i in range(len(v_list))]
        path_list = [[xy_list[0][i], xy_list[1][i]] for i in range(len(v_list))]

    if cmd == "random":
        A = 1
        w1 = rd.uniform(-10,10)
        phi = rd.uniform(0,2*pi)
        k1 = 0
        B = 1
        w2 = rd.uniform(-10,10)
        k2 = 0

        x_list = [x(t) for t in v_list]
        y_list = [y(t) for t in v_list]

        xy_list = minmax(x_list, y_list, prog.tegne_limits)

        # path_list = [[x_list[i], y_list[i]] for i in range(len(v_list))]
        path_list = [[xy_list[0][i], xy_list[1][i]] for i in range(len(v_list))]

    if cmd == "image":
        x_list = [float(coords[0]) for coords in image_list]
        y_list = [float(coords[1]) for coords in image_list]
        print(x_list)

        xy_list = minmax(x_list, y_list, prog.tegne_limits)

        # path_list = [[x_list[i], y_list[i]] for i in range(len(v_list))]
        path_list = [[xy_list[0][i], xy_list[1][i]] for i in range(len(image_list))]


    if cmd == "view":
        plt.plot(xy_list[0],xy_list[1])
        plt.show(block=False)


    if cmd == "draw":
        prog.move_home()
        prog.move_path(path_list)
