# ----------
# Part Two
#
# Now we'll make the scenario a bit more realistic. Now Traxbot's
# sensor measurements are a bit noisy (though its motions are still
# completetly noise-free and it still moves in an almost-circle).
# You'll have to write a function that takes as input the next
# noisy (x, y) sensor measurement and outputs the best guess 
# for the robot's next position.
#
# ----------
# YOUR JOB
#
# Complete the function estimate_next_pos. You will be considered 
# correct if your estimate is within 0.01 stepsizes of Traxbot's next
# true position. 
#
# ----------
# GRADING
# 
# We will make repeated calls to your estimate_next_pos function. After
# each call, we will compare your estimated position to the robot's true
# position. As soon as you are within 0.01 stepsizes of the true position,
# you will be marked correct and we will tell you how many steps it took
# before your function successfully located the target bot.

# These import steps give you access to libraries which you may (or may
# not) want to use.
from robot import *  # Check the robot.py tab to see how this works.
from math import *
from matrix import * # Check the matrix.py tab to see how this works.
import random

# This is the function you have to write. Note that measurement is a 
# single (x, y) point. This function will have to be called multiple
# times before you have enough information to accurately predict the
# next position. The OTHER variable that your function returns will be 
# passed back to your function the next time it is called. You can use
# this to keep track of important information over time.
def estimate_next_pos(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""

    if OTHER is None:
        xy_estimate = measurement
        angle = 0
        
        measurements_num = 0
        
        step_total = 0
        
        angle_step_total = 0

        
    else:
        measurements_num_old = OTHER[0]
        measurement_old = OTHER[1]
        angle_old = OTHER[2]
        step_total = OTHER[3]
        angle_step_total = OTHER[4]

        measurements_num = measurements_num_old + 1

        step_length = distance_between(measurement, measurement_old)
        step_total += step_length
        step_average = step_total / measurements_num


        angle = atan2(measurement[1]-measurement_old[1],measurement[0]-measurement_old[0])
        angle_step = angle - angle_old
        print "Angle step", angle_step, (angle_step%(2*pi)), angle_trunc(angle_step)
        
        angle_step_total += angle_trunc(angle_step)
        average_angle_step = angle_step_total / measurements_num

        new_angle = angle + average_angle_step

        x_estimate = measurement[0]+ step_average*cos(new_angle)
        y_estimate = measurement[1]+ step_average*sin(new_angle)

        xy_estimate = (x_estimate,y_estimate)


        
    OTHER = [measurements_num, measurement, angle, step_total, angle_step_total]

    return xy_estimate, OTHER

# A helper function you may find useful.
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# This is a demo for what a strategy could look like. This one isn't very good.
def naive_next_pos(measurement, OTHER = None):
    """This strategy records the first reported position of the target and
    assumes that eventually the target bot will eventually return to that 
    position, so it always guesses that the first position will be the next."""
    if not OTHER: # this is the first measurement
        OTHER = measurement
    xy_estimate = OTHER 
    return xy_estimate, OTHER
