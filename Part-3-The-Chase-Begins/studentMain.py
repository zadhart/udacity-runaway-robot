# ----------
# Part Three
#
# Now you'll actually track down and recover the runaway Traxbot. 
# In this step, your speed will be about twice as fast the runaway bot,
# which means that your bot's distance parameter will be about twice that
# of the runaway. You can move less than this parameter if you'd 
# like to slow down your bot near the end of the chase. 
#
# ----------
# YOUR JOB
#
# Complete the next_move function. This function will give you access to 
# the position and heading of your bot (the hunter); the most recent 
# measurement received from the runaway bot (the target), the max distance
# your bot can move in a given timestep, and another variable, called 
# OTHER, which you can use to keep track of information.
# 
# Your function will return the amount you want your bot to turn, the 
# distance you want your bot to move, and the OTHER variable, with any
# information you want to keep track of.
# 
# ----------
# GRADING
# 
# We will make repeated calls to your next_move function. After
# each call, we will move the hunter bot according to your instructions
# and compare its position to the target bot's true position
# As soon as the hunter is within 0.01 stepsizes of the target,
# you will be marked correct and we will tell you how many steps it took
# before your function successfully located the target bot. 
#
# As an added challenge, try to get to the target bot as quickly as 
# possible. 

from robot import *
from math import *
from matrix import *
import random

def next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER = None):
    # This function will be called after each time the target moves. 

    # The OTHER variable is a place for you to store any historical information about
    # the progress of the hunt (or maybe some localization information). Your return format
    # must be as follows in order to be graded properly.

    if OTHER is None:
        xy_estimate = target_measurement
        angle = 0
        
        measurements_num = 0
        step_total = 0
        angle_step_total = 0
        
        turning = atan2(xy_estimate[1] - hunter_position[1], xy_estimate[0] - hunter_position[0])

        current_turning = turning
        distance = distance_between(hunter_position, xy_estimate)

    else:
        measurements_num_old = OTHER[0]
        target_measurement_old = OTHER[1]
        angle_old = OTHER[2]
        step_total = OTHER[3]
        angle_step_total = OTHER[4]
        turning_old = OTHER[5]

        measurements_num = measurements_num_old + 1

        step_size = distance_between(target_measurement, target_measurement_old)
        step_total += step_size
        average_step = step_total / measurements_num


        angle = atan2(target_measurement[1]-target_measurement_old[1],target_measurement[0]-target_measurement_old[0])
        angle_step = angle - angle_old
        
        
        angle_step_total += angle_trunc(angle_step)
        average_angle_step = angle_step_total / measurements_num

        new_angle = angle + average_angle_step

        x_estimate = target_measurement[0]+ average_step*cos(new_angle)
        y_estimate = target_measurement[1]+ average_step*sin(new_angle)
        xy_estimate = (x_estimate,y_estimate)

        next_positions = [xy_estimate]

        next_n = 5
        prev_n_angle = new_angle

        min_distance_to_hunter = distance_between(hunter_position, xy_estimate)
        min_position = 0

        
        for n in range(1,next_n):
            prev_n_angle += average_angle_step
            
            nx_estimate = next_positions[n-1][0]+ average_step*cos(prev_n_angle)
            ny_estimate = next_positions[n-1][1]+ average_step*sin(prev_n_angle)
            
            next_positions.append((nx_estimate,ny_estimate))

            distance = distance_between(hunter_position, [nx_estimate,ny_estimate])# / (1+0.3*n)

            if distance < min_distance_to_hunter:
                min_distance_to_hunter = distance
                min_position = n

        print "min_pos", min_position


        distance = min_distance_to_hunter
        
        heading_to_target = get_heading(hunter_position, next_positions[min_position])
        turning = heading_to_target - hunter_heading

        if distance > max_distance:
            distance is max_distance

        
    OTHER = [measurements_num, target_measurement, angle, step_total, angle_step_total, turning]

    return turning, distance, OTHER


def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""

    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi

def get_heading(hunter_position, target_position):
    """Returns the angle, in radians, between the target and hunter positions"""
    hunter_x, hunter_y = hunter_position
    target_x, target_y = target_position
    heading = atan2(target_y - hunter_y, target_x - hunter_x)
    heading = angle_trunc(heading)
    return heading

def naive_next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER):
    """This strategy always tries to steer the hunter directly towards where the target last
    said it was and then moves forwards at full speed. This strategy also keeps track of all 
    the target measurements, hunter positions, and hunter headings over time, but it doesn't 
    do anything with that information."""
    if not OTHER: # first time calling this function, set up my OTHER variables.
        measurements = [target_measurement]
        hunter_positions = [hunter_position]
        hunter_headings = [hunter_heading]
        OTHER = (measurements, hunter_positions, hunter_headings) # now I can keep track of history
    else: # not the first time, update my history
        OTHER[0].append(target_measurement)
        OTHER[1].append(hunter_position)
        OTHER[2].append(hunter_heading)
        measurements, hunter_positions, hunter_headings = OTHER # now I can always refer to these variables
    
    heading_to_target = get_heading(hunter_position, target_measurement)
    heading_difference = heading_to_target - hunter_heading
    turning =  heading_difference # turn towards the target
    distance = max_distance # full speed ahead!
    return turning, distance, OTHER
