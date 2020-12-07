
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
    alpha_min = arm.getArmLimit()[0][0]
    alpha_max = arm.getArmLimit()[0][1]
    beta_min = arm.getArmLimit()[1][0]
    beta_max = arm.getArmLimit()[1][1]
    row = int((alpha_max - alpha_min) / granularity) + 1
    column = int((beta_max - beta_min) / granularity) + 1
    offset = []
    offset.extend([alpha_min,beta_min])
    starting_point = angleToIdx(arm.getArmAngle(), offset, granularity)
    maze_goals = []
    maze_walls = []

    for alpha in range(alpha_min, alpha_max + granularity, granularity):
        for beta in range(beta_min, beta_max + granularity, granularity):
            index = angleToIdx((alpha, beta), offset, granularity)
            arm.setArmAngle((alpha, beta))
            if doesArmTipTouchGoals(arm.getEnd(), goals):
                maze_goals.append(index)
                continue
            elif doesArmTouchObjects(arm.getArmPosDist(),obstacles, False):
                maze_walls.append(index)
                continue
            elif doesArmTouchObjects(arm.getArmPosDist(),goals, True):
                maze_walls.append(index)
                continue
            elif not isArmWithinWindow(arm.getArmPos(), window):
                maze_walls.append(index)
                continue
    
    input_map = []
    for r in range(row):
        input_map.append([])
        for c in range(column):
            input_map[r].append(SPACE_CHAR)
    # print(maze_goals)
    # print(maze_walls)
    for r in range(row):
        for c in range(column):
            if (r,c) in maze_walls:
                input_map[r][c] = WALL_CHAR
            if (r,c) in maze_goals:
                # print("has goals")
                input_map[r][c] = OBJECTIVE_CHAR
            if (r,c) == starting_point:
                # print("has start")
                input_map[r][c] = START_CHAR
    
    # print(input_map)
    transformed = Maze(input_map, offset, granularity)
    transformed.saveToFile("transformed_maze.txt")
    return transformed



