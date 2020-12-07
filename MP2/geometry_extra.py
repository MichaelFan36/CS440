# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains geometry functions that relate with Part1 in MP2.
"""

import math
import numpy as np
from const import *

def computeCoordinate(start, length, angle):
    """Compute the end cooridinate based on the given start position, length and angle.

        Args:
            start (tuple): base of the arm link. (x-coordinate, y-coordinate)
            length (int): length of the arm link
            angle (int): degree of the arm link from x-axis to couter-clockwise

        Return:
            End position (int,int):of the arm link, (x-coordinate, y-coordinate)
    """
    return (start[0] + int(length * math.cos(angle / 180 * np.pi)), start[1] + int(length * math.sin(angle  / 180 * np.pi) * -1))

def chord_distance_discard(point1, point2, chord):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]

    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1
    return np.abs((chord[0] * a + chord[1] * b + c) / np.sqrt(a**2 + b**2))

def chord_distance(point1, point2, chord):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    x = chord[0]
    y = chord[1]
   
    cross = (x2 - x1) * (x - x1) + (y2 - y1) * (y - y1)
    if (cross <= 0):
        return np.sqrt((x - x1) * (x - x1) + (y - y1) * (y - y1))
  
    d2 = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)
    if (cross >= d2):
        return np.sqrt((x - x2) * (x - x2) + (y - y2) * (y - y2))
  
    r = cross / d2
    px = x1 + (x2 - x1) * r
    py = y1 + (y2 - y1) * r
    return np.sqrt((x - px) * (x - px) + (py - y) * (py - y))

def chord_distance_discard2(point1, point2, chord):
    """ Algorithm Got From StackOverFlow
        website:https://stackoverflow.com/questions/849211/shortest-distance-between-a-point-and-a-line-segment
    """
    x_reach = chord[0] - point1[0]
    y_reach = chord[1] - point1[1]
    x_diff = point2[0] - point1[0]
    y_diff = point2[1] - point1[1]

    dot = x_reach * x_diff + y_reach * y_diff
    length_squared = x_diff**2 + y_diff**2

    param = -1

    if length_squared != 0:
        param = dot / length_squared
    
    xx = 0
    yy = 0

    if param < 0:
        xx = point1[0]
        yy = point1[1]
    elif param > 1:
        xx = point2[0]
        yy = point2[1]
    else:
        xx = point1[0] + param * x_diff
        yy = point1[1] + param * y_diff
    
    dx = chord[0] - xx
    dy = chord[1] - yy
    dist = np.sqrt(dx*dx+dy*dy)
    return dist

def doesArmTouchObjects(armPosDist, objects, isGoal=False):
    """Determine whether the given arm links touch any obstacle or goal

        Args:
            armPosDist (list): start and end position and padding distance of all arm links [(start, end, distance)]
            objects (list): x-, y- coordinate and radius of object (obstacles or goals) [(x, y, r)]
            isGoal (bool): True if the object is a goal and False if the object is an obstacle.
                           When the object is an obstacle, consider padding distance.
                           When the object is a goal, no need to consider padding distance.
        Return:
            True if touched. False if not.
    """
    for o in objects:
        for a in armPosDist:
            point1 = a[0]
            point2 = a[1]
            chord = (o[0],o[1])
            if not isGoal:
                if chord_distance(point1, point2, chord) <= (o[2] + a[2]):
                    return True
            if isGoal:
                if chord_distance(point1, point2, chord) <= o[2]:
                    return True
    return False

def doesArmTipTouchGoals(armEnd, goals):
    """Determine whether the given arm tip touch goals

        Args:
            armEnd (tuple): the arm tip position, (x-coordinate, y-coordinate)
            goals (list): x-, y- coordinate and radius of goals [(x, y, r)]. There can be more than one goal.
        Return:
            True if arm tick touches any goal. False if not.
    """
    for g in goals:
        dist = np.sqrt((g[0] - armEnd[0]) ** 2 + (g[1] - armEnd[1]) ** 2)
        if dist <= g[2]:
            return True
    return False


def isArmWithinWindow(armPos, window):
    """Determine whether the given arm stays in the window

        Args:
            armPos (list): start and end positions of all arm links [(start, end)]
            window (tuple): (width, height) of the window

        Return:
            True if all parts are in the window. False if not.
    """
    for a in armPos:
        if a[0][0] < 0 or a[0][0] > window[0] or a[1][0] < 0 or a[1][0] > window[0] or a[0][1] < 0 or a[0][1] > window[1] or a[1][1] < 0 or a[1][1] > window[1]:
            return False
    return True


if __name__ == '__main__':
    computeCoordinateParameters = [((150, 190),100,20), ((150, 190),100,40), ((150, 190),100,60), ((150, 190),100,160)]
    resultComputeCoordinate = [(243, 156), (226, 126), (200, 104), (57, 156)]
    testRestuls = [computeCoordinate(start, length, angle) for start, length, angle in computeCoordinateParameters]
    assert testRestuls == resultComputeCoordinate

    testArmPosDists = [((100,100), (135, 110), 4), ((135, 110), (150, 150), 5)]
    testObstacles = [[(120, 100, 5)], [(110, 110, 20)], [(160, 160, 5)], [(130, 105, 10)]]
    resultDoesArmTouchObjects = [
        True, True, False, True, False, True, False, True,
        False, True, False, True, False, False, False, True
    ]

    testResults = []
    for testArmPosDist in testArmPosDists:
        for testObstacle in testObstacles:
            testResults.append(doesArmTouchObjects([testArmPosDist], testObstacle))
            # print(testArmPosDist)
            # print(doesArmTouchObjects([testArmPosDist], testObstacle))

    print("\n")
    for testArmPosDist in testArmPosDists:
        for testObstacle in testObstacles:
            testResults.append(doesArmTouchObjects([testArmPosDist], testObstacle, isGoal=True))
            # print(testArmPosDist)
            # print(doesArmTouchObjects([testArmPosDist], testObstacle, isGoal=True))

    assert resultDoesArmTouchObjects == testResults

    testArmEnds = [(100, 100), (95, 95), (90, 90)]
    testGoal = [(100, 100, 10)]
    resultDoesArmTouchGoals = [True, True, False]

    testResults = [doesArmTipTouchGoals(testArmEnd, testGoal) for testArmEnd in testArmEnds]
    assert resultDoesArmTouchGoals == testResults

    testArmPoss = [((100,100), (135, 110)), ((135, 110), (150, 150))]
    testWindows = [(160, 130), (130, 170), (200, 200)]
    resultIsArmWithinWindow = [True, False, True, False, False, True]
    testResults = []
    for testArmPos in testArmPoss:
        for testWindow in testWindows:
            testResults.append(isArmWithinWindow([testArmPos], testWindow))
    assert resultIsArmWithinWindow == testResults

    print("Test passed\n")
