from math import * 

def direction(target_lat,target_long,ship_lat,ship_long,heading):
    # direction = "Main Ship:",ship_lat,ship_long,"\nHeading wrt to True North : ",-ship_heading+90)
    direction = ''
    heading=-1 * heading + 90
    delta_target_long = target_long-ship_long
    delta_target_lat= target_lat-ship_lat
    true_bearing = degrees(atan2(delta_target_long,delta_target_lat)) - 90
    distance = (sqrt((delta_target_lat)**2 + (delta_target_long)**2))/0.016666666
    # print(degree1)
    relative_bearing = (heading + true_bearing)%360
    #print('Bearings: ',relative_bearing)
    # print(relative_bearing)
    if relative_bearing>=5 and relative_bearing<=30:    
        direction = "Fine on Starboard Bow"
        priority = 9
    elif relative_bearing>=31 and relative_bearing<=60:    
        direction = "Broad on Starboard Bow"
        priority = 9
    elif relative_bearing>=61 and relative_bearing<=89:    
        direction = "Forward on Starboard Beam"
        priority = 9
    elif relative_bearing>89 and relative_bearing<91:    
        direction = "On Starboard Beam"
        priority = 9
    elif relative_bearing>=91 and relative_bearing<=120:
        direction = "Abaft Starboard Beam"
        priority = 7
    elif relative_bearing>=121 and relative_bearing <=150:
        direction = "On Starboard Quarter"
        priority = 6
    elif relative_bearing>=151 and relative_bearing<=179:
        direction = "Fine on Starboard Stern"
        priority = 5.5
    elif relative_bearing>179 and relative_bearing <181:
        direction = "Astern"
        priority = 4
    elif relative_bearing>=181 and relative_bearing<=210:    
        direction = "Fine on Port Stern"
        priority = 4
    elif relative_bearing>=211 and relative_bearing<=240:    
        direction = "On Port Quarter"
        priority = 4
    elif relative_bearing>=241 and relative_bearing<=269:    
        direction = "Abaft on port beam"
        priority = 4
    elif relative_bearing>269 and relative_bearing<271:
        direction = "On Port Beam"
        priority = 4
    elif relative_bearing>=271 and relative_bearing <=300:
        direction = "Forward on Port Beam"
        priority = 4
    elif relative_bearing>=301 and relative_bearing<=330:
        direction = "Broad on Port Bow"
        priority = 4
    elif relative_bearing>=331 and relative_bearing<=355:
        direction = "Fine on the Port Bow"
        priority = 6.5
    elif relative_bearing>355 or relative_bearing <5:
        direction = "Ahead"
        priority = 9
    else :
        direction = "Ship is out of bounds"
        priority = 0
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@",relative_bearing)
    return direction,priority,relative_bearing,distance