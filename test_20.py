import numpy as np
from math import *

def distance_calc(xo, yo, xt, yt):
    xot = radians(xt) - radians(xo)
    yot = radians(yt) - radians(yo)
    a = sin(xot/2)**2 + cos(radians(yo)) * cos(radians(yt)) * sin(yot/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))           #cartesian distance
    d = c * 3440.064773 #6371000 * c * 0.0005399568              #distance in nautical miles
    return d


def risk_calc(target, main):        #target = [mmsi, lattitude, longitude, heading, speed]  main = [lattitude, longitude, heading, speed]
    #d =  sqrt((target[2] - main[1]) **  2 + (target[1] - main[0]) ** 2)       #absolute distance betn ships
    main[3] *= 0.0166667
    target[4] *= 0.0166667
    # print(main[3], target[4])
    x_vel_o = main[3] * sin(radians(main[2]))                    #our ship velocity along x/lon axis
    x_vel_t = target[4] * sin(radians(target[3]))                #target ship velocity along x/lon axis
    y_vel_o = main[3] * cos(radians(main[2]))                    #our ship velocity along y/lat axis
    y_vel_t = target[4] * cos(radians(target[3]))                #target ship velocity along y/lat axis

    x_vel = (x_vel_t - x_vel_o)         #relative velocity along x axis / lon
    y_vel = (y_vel_t - y_vel_o)         #relative velocity along y axis / lat

    xot = radians(target[2]) - radians(main[1])      #relative distance along x/lon
    yot = radians(target[1]) - radians(main[0])      #relative distance along y/lat
    # print(x_vel_o,x_vel_t,y_vel_o,y_vel_t)
    # print(x_vel, y_vel)
    # a = sin(xot/2)**2 + cos(radians(main[0])) * cos(radians(target[1])) * sin(yot/2)**2
    # c = 2 * atan2(sqrt(a), sqrt(1-a))           #cartesian distance
    # d = 6371000 * c * 0.0005399568              #distance in nautical miles
    d = distance_calc(target[1], target[2], main[0], main[1])
    vel_ot = sqrt(x_vel ** 2 + y_vel ** 2)      #relative velocity

    if d == 0:
        d = 0.0000000000001
    if vel_ot == 0:
        vel_ot = 0.0000000000001
    
    #th_ot is direction of resultant relative velocity wrt north
    if x_vel >= 0:
        if y_vel >= 0:
            th_ot = atan2(x_vel, y_vel)
        elif y_vel < 0:
            th_ot = atan2(x_vel, y_vel) + pi
    elif  x_vel < 0:
        if y_vel >= 0:
            th_ot = atan2(x_vel, y_vel) + 2 * pi
        elif y_vel < 0:
            th_ot = atan2(x_vel, y_vel) + pi
    
    #alph_t is bearing angle wrt north
    if xot >= 0:
        if yot >= 0:
            alph_t = atan2(xot, yot)
        elif yot < 0:
            alph_t = atan2(xot, yot) + pi
    elif  xot < 0: 
        if yot >= 0:
            alph_t = atan2(xot, yot) + 2 * pi
        elif yot < 0:
            alph_t = atan2(xot, yot) + pi

    alph_ot = (alph_t - radians(main[2]) + 2 * pi ) % (2 * pi)
    # print(target[0], main[2])
    # print(d, alph_ot, d * cos(alph_ot), d * sin(alph_ot))

    #Calculate the dot product of the relative position vector and the relative velocity vector:
    #dot_product = Rx * Vx + Ry * Vy
    # dot_product = xot * x_vel + yot * y_vel
    # dot_product = cos(radians(target[4])) * cos(radians(main[3])) + sin(radians(target[4])) * sin(radians(main[3]))
    dot_product = x_vel_o * x_vel_t + y_vel_o * y_vel_t
    # print(target[0], dot_product)
    
    ########################### risk factor calculation  ###########################
    dcpa = d * sin(th_ot - alph_t - pi)                 #th_OT is target heading alph_T is bearing wrt north
    tcpa = (d * cos(th_ot - alph_t - pi)) / vel_ot      #vel_OT is relative velocity between target and main ship
    # roc = vel_ot / d
    # roc = target[4]*cos(alph_ot - radians(target[3])) - main[3]*cos(alph_ot - radians(main[2]))
    roc = target[4]*(target[3] - main[2])
    # print(target[0], roc)    
    
    f_y_o = radians(main[0]) + abs(tcpa) * y_vel_o / 3600
    f_x_o = radians(main[1]) + abs(tcpa) * x_vel_o / 3600
    f_y_t = radians(target[1]) + abs(tcpa) * y_vel_t / 3600
    f_x_t = radians(target[2]) + abs(tcpa) * x_vel_t / 3600
    # print(degrees(f_y_o), degrees(f_x_o), degrees(f_y_t), degrees(f_x_t))
    f_y_o = round(degrees(f_y_o),7)
    f_x_o = round(degrees(f_x_o),7)
    f_y_t = round(degrees(f_y_t),7)
    f_x_t = round(degrees(f_x_t),7)
    main[3] *= 60
    target[4] *= 60
    return{'cpa' : abs(dcpa), 'tcpa' : abs(tcpa), 'roc' : roc,'dot_product' : dot_product, 'target_future' : [f_y_t, f_x_t], 'main_future' : [f_y_o, f_x_o], 'target_current' : target, 'main_current' : main}