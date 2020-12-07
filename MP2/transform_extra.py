
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.
    
        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """
    num_of_dimensions = arm.getNumArmLinks()
    allangles = arm.getArmLimit()
    offset = [0] * 3
    dimensions = [1] * 3
    for n in range(num_of_dimensions):
        dimensions[n] = int((allangles[n][1] - allangles[n][0]) / granularity) + 1
        offset[n] = allangles[n][0]
    
    alpha_min, beta_min, gamma_min = idxToAngle((0,0,0), offset, granularity)

    angles = arm.getArmAngle().copy()
    input_map = []

    input_map = [[[WALL_CHAR] * dimensions[2] for j in range(dimensions[1])]for i in range(dimensions[0])]

    for alpha in range(alpha_min, allangles[0][1] + granularity, granularity):
        arm.setArmAngle([alpha, beta_min, gamma_min])
        ArmPosDist = arm.getArmPosDist()
        index = angleToIdx((alpha, beta_min, gamma_min), offset, granularity)

        if not isArmWithinWindow([ArmPosDist[0]], window):
            continue
        if doesArmTouchObjects([ArmPosDist[0]], obstacles, False):
            continue

        if num_of_dimensions == 1:
            if doesArmTipTouchGoals(arm.getEnd(), goals):
                    input_map[index[0]][index[1]][index[2]] = OBJECTIVE_CHAR
                    continue
            elif doesArmTouchObjects([ArmPosDist[0]],goals, True):
                    continue
            else:
                input_map[index[0]][index[1]][index[2]] = SPACE_CHAR
                continue
        else:
            if doesArmTouchObjects([ArmPosDist[0]], goals, True):
                continue
            for beta in range(beta_min, allangles[1][1] + granularity, granularity):
                arm.setArmAngle([alpha, beta, gamma_min])
                ArmPosDist = arm.getArmPosDist()
                index = angleToIdx((alpha, beta, gamma_min), offset, granularity)
                if not isArmWithinWindow([ArmPosDist[1]],window):
                    continue
                if doesArmTouchObjects([ArmPosDist[1]], obstacles, False):
                    continue
                if num_of_dimensions == 2:
                    if doesArmTipTouchGoals(arm.getEnd(), goals):
                        input_map[index[0]][index[1]][index[2]] = OBJECTIVE_CHAR
                        continue
                    elif doesArmTouchObjects([ArmPosDist[1]], goals, True):
                        continue
                    else:
                        input_map[index[0]][index[1]][index[2]] = SPACE_CHAR
                        continue
                else:
                    if doesArmTouchObjects([ArmPosDist[1]], goals, True):
                        continue
                    for gamma in range(gamma_min, allangles[2][1] + granularity, granularity):
                        arm.setArmAngle([alpha, beta, gamma])
                        ArmPosDist = arm.getArmPosDist()
                        index = angleToIdx((alpha, beta, gamma), offset, granularity)
                        if not isArmWithinWindow([ArmPosDist[2]],window):
                            continue
                        if doesArmTouchObjects([ArmPosDist[2]], obstacles, False):
                            continue
                        if num_of_dimensions == 3:
                            if doesArmTipTouchGoals(arm.getEnd(), goals):
                                input_map[index[0]][index[1]][index[2]] = OBJECTIVE_CHAR
                                continue
                            elif doesArmTouchObjects([ArmPosDist[2]], goals, True):
                                continue
                            else:
                                input_map[index[0]][index[1]][index[2]] = SPACE_CHAR
                                continue
    # print(maze_goals)
    # print(maze_walls)
    arm.setArmAngle(angles)
    while len(angles) < 3:
        angles.append(0)
    starting_point = angleToIdx(angles, offset, granularity)
    input_map[starting_point[0]][starting_point[1]][starting_point[2]] = START_CHAR
    # print(input_map)
    transformed = Maze(input_map, offset, granularity)
    transformed.saveToFile("transformed_maze.txt")
    return transformed



