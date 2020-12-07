# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,astar)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze

from collections import deque
from heapq import heappop, heappush

def search(maze, searchMethod):
    return {
        "bfs": bfs,
    }.get(searchMethod, [])(maze)

def bfs(maze):
    # Write your code here
    """
    This function returns optimal path in a list, which contains start and objective.
    If no path found, return None. 
    """
    start = maze.getStart()
    queue = [(start,-1)]
    visited = set()
    visited.add(start)
    path = []
    track = 0
    track2 = 1
    found = False
    while track < track2 and found == False:
        start = queue[track][0]
        for neighbour in maze.getNeighbors(*start):
            if maze.isObjective(*neighbour):
                path.append(neighbour)
                found = True
                break
            elif neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, track))
                track2 = track2 + 1
        if not found:        
            track = track + 1
    if len(path) != 0:
        while track != -1:
            path.append(queue[track][0])
            track = queue[track][1]
        path.reverse()
        return path
    return None
