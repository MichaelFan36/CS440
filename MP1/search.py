# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,extra)

from math import *
from itertools import permutations
import heapq as hq
import sys

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "extra": extra,
    }.get(searchMethod)(maze)


def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    start = maze.getStart()
    queue = [start]
    visited = []
    while queue:
        if queue[0] == start:
            path = [queue.pop(0)]
        else:
            path = queue.pop(0)
        current = path[-1]
        if maze.isObjective(current[0], current[1]):
            return path
        else:
            if current not in visited:
                for neighbor in maze.getNeighbors(current[0],current[1]):
                    newPath = list(path)
                    newPath.append(neighbor)
                    queue.append(newPath)
                visited.append(current)
    return []

def heuristic(x,y):
    return sum(abs(dn-dg) for dn,dg in zip(x,y))

def makePath(mazedict, current):
    path = []
    while mazedict[current][0] != None:
        path.insert(0, current)
        current = mazedict[current][0]
    path.insert(0, current)
    return path

def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    start = maze.getStart()
    destination = maze.getObjectives()
    mazeset = set()
    mazeset.add(start)
    mazedict = {
        start: [None, heuristic(start, destination[0]), 0]
    }
    while len(mazeset):
        current = min(mazeset, key=lambda points: mazedict[points][1] + mazedict[points][2])
        # print(current,91)
        if current == destination[0]:
            # print(current,93)
            return makePath(mazedict, current)

        mazeset.remove(current)

        for neighbor in maze.getNeighbors(current[0], current[1]):
            if neighbor not in mazedict:
                mazedict[neighbor] = [current, heuristic(neighbor, destination[0]), mazedict[current][2] + 1]
                # print(neighbor,101)
                mazeset.add(neighbor)
            elif (mazedict[neighbor][1] + mazedict[current][2] + 1) < (mazedict[neighbor][1] + mazedict[neighbor][2]):
                mazedict[neighbor][0] = current
                mazedict[neighbor][2] = mazedict[current][2] + 1
                # print(neighbor, 106)
                if neighbor not in mazeset:    
                    mazeset.add(neighbor)
    return []


def astar_helper(maze, start, destination):
    Permutation_list = list(permutations(maze.getObjectives()))
    Permutation_results = []
    i = 0

    for x in Permutation_list:
        Permutation_results.append([])
        # print ('x is ', x)
        maze_corner_dict = {}
        start = maze.getStart()
        maze_corner_dict = {
                start: [None, heuristic(start, x[0]), 0]
            }
        last_path = []
        j = 0
        last_gone = 0
        for y in x:
            #print ('y is ', y)
            maze_corner_dict = {
                start: [None, heuristic(start, y), 0]
            }
            path = []
            mazeset = set()
            if start not in mazeset:
                mazeset.add(start)
            #print('mazeset is ', mazeset)
            while len(mazeset):
                current = min(mazeset, key=lambda points: maze_corner_dict[points][1] + maze_corner_dict[points][2])
                #print ('current is ', current)
                if current == y:
                    path = makePath(maze_corner_dict, current)

                mazeset.remove(current)

                for neighbor in maze.getNeighbors(current[0], current[1]):
                    if neighbor not in maze_corner_dict:
                        maze_corner_dict[neighbor] = [current, heuristic(neighbor, y), maze_corner_dict[current][2] + 1]
                        mazeset.add(neighbor)
                    elif (maze_corner_dict[neighbor][1] + maze_corner_dict[current][2] + 1) < (maze_corner_dict[neighbor][1] + maze_corner_dict[neighbor][2]):
                        maze_corner_dict[neighbor][0] = current
                        maze_corner_dict[neighbor][2] = maze_corner_dict[current][2] + 1
                        if neighbor not in mazeset:    
                            mazeset.add(neighbor)
            if j != 0:
                path = path[1:]
            #print('last_path is ', last_path)
            Permutation_results[i] = [last_path + path, maze_corner_dict[y][2] + last_gone]
            last_path = Permutation_results[i][0]
            # print('path len is ', len(last_path))
            last_gone = maze_corner_dict[y][2]
            start = y
            j = j + 1
        i = i + 1
    #print('Permutation_results is ', Permutation_results)
    # print(Permutation_results)
    #final_path = min(Permutation_results.items(), key=lambda points: points[1])[1][0]
    
    m = len(Permutation_results[0][0])
    final_path = []
    for res in Permutation_results:
        if (len(res[0])<m):
            final_path=res[0]
            m=len(res[0])
    
    # final_path = min(Permutation_results.items(), key=lambda points: points[1])[1]
    # print ('final_path is ', final_path)
    if len(final_path):
        return final_path
    return []

def Permutation_sum(start, destinations):
    total = heuristic(start, destinations[0])
    for i in range(len(destinations) - 1):
        total = total + heuristic(destinations[i], destinations[i+1])
    return total


def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.
        
    @param maze: The maze to execute the search on.
        
    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here
    finished = False
    pq = []
    path = []
    start = maze.getStart()
    mazedict = {}
    rest = []
    Permutation_list = list(permutations(maze.getObjectives()))
    for lists in Permutation_list:
        mazedict[(start, lists)] = (None, 0)
        hq.heappush(pq, (Permutation_sum(start, lists), start, lists, 0))
    while True:
        current = hq.heappop(pq)
        first_to_find = current[2][0]
        start = current[1]
        rest = current[2]
        new_gone = current[3] + 1
        for neighbor in maze.getNeighbors(start[0],start[1]):
            if(neighbor == first_to_find):
                rest2 = rest[1:]
                if (len(rest) == 1):
                    path.insert(0, neighbor)
                    finished = True
                    break
                elif ((neighbor, rest2) not in mazedict) or (mazedict[(neighbor, rest2)][1] > new_gone):
                    hq.heappush(pq, ((Permutation_sum(neighbor, rest2) + new_gone), neighbor, rest2, new_gone))
                    mazedict[(neighbor,rest2)] = ((start, rest), new_gone)
            elif ((neighbor, rest) not in mazedict) or (mazedict[(neighbor, rest)][1] > new_gone):
                    hq.heappush(pq, ((Permutation_sum(neighbor, rest) + new_gone), neighbor, rest, new_gone))
                    mazedict[(neighbor,rest)] = ((start, rest), new_gone)
        if finished:
            break
    if (finished):
        while mazedict[(start, rest)][0] != None:
            path.insert(0, start)
            k = start
            start = mazedict[(start, rest)][0][0]
            rest = mazedict[(k, rest)][0][1]
        path.insert(0, start)
    return path


distance = {}
muldict = {}
mst = []
def Floyd_Warshall(maze):
    global distance
    x,y = maze.getDimensions()
    Vertices = []
    for i in range(x):
        for j in range(y):
            if (not maze.isWall(i,j)):
                Vertices.append((i,j))
                distance[(i,j)] = {}
    for i in Vertices:
        for j in Vertices:
            if (i != j):
                distance[i][j] = sys.maxsize
            else:
                distance[i][j] = 0
        for neighbor in maze.getNeighbors(i[0], i[1]):
            distance[i][neighbor] = 1
    for i in Vertices:
        for j in Vertices:
            for k in Vertices:
                if (distance[j][k] > distance[j][i] + distance[i][k]):
                    distance[j][k] = distance[j][i] + distance[i][k]
    return

def Prim(start, destinations):
    global muldict
    global mst
    mst[len(destinations) - 1] = 1
    index = 0
    result = 0
    for i in range(len(destinations) - 1):
        muldict[i] = distance[destinations[len(destinations) - 1]][destinations[i]]
        mst[i] = 0
    for i in range(len(destinations) - 1):
        minfound = sys.maxsize
        index = -1
        for j in range(len(destinations) - 1):
            if mst[j] == 0 and minfound > muldict[j]:
                minfound = muldict[j]
                index = j
        mst[index] = 1
        result = result + minfound
        for k in range(len(destinations)):
            muldict[k] = min(muldict[k], distance[destinations[index]][destinations[k]])
    # print(start)
    # print(destinations)
    minfound = distance[start][destinations[0]]
    for destination in destinations:
        if minfound > distance[start][destination]:
            minfound = distance[start][destination]
    return result + minfound


def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    Floyd_Warshall(maze)
    global mst
    global muldict
    mst = [0] * len(maze.getObjectives())
    muldict = [0] * len(maze.getObjectives())
    start = maze.getStart()
    destinations = maze.getObjectives()
    finished = False
    pq = []
    path = []
    mazedict = {}
    rest = []
    raw_result = []
    count = 0
    hq.heappush(pq, (Prim(start, destinations), start, destinations, 0, -1))
    rows, cols = maze.getDimensions()
    for row in range(rows):
        for col in range(cols):
            mazedict[(row,col)] = set()
    while True:
        current = hq.heappop(pq)
        start = current[1]
        parent = current[4]
        rest = current[2]
        new_gone = current[3] + 1
        raw_result.append((start, parent))
        count = count + 1
        for neighbor in maze.getNeighbors(start[0],start[1]):
            if(neighbor in rest):
                # print (rest)
                rest2 = rest.copy()
                # print(neighbor)
                rest2.remove(neighbor)
                # print(rest2)
                if (len(rest) == 1):
                    path.insert(0, neighbor)
                    finished = True
                    count = count - 1
                    break
                else:
                    hq.heappush(pq, ((Prim(neighbor, rest2) + new_gone), neighbor, rest2, new_gone, count - 1))
            elif tuple(rest) not in mazedict[neighbor]:
                    hq.heappush(pq, ((Prim(neighbor, rest) + new_gone), neighbor, rest, new_gone, count - 1))
                    mazedict[neighbor].add(tuple(rest))
        if finished:
            break
    if (finished):
        while raw_result[count][1] != -1:
            # print(start)
            start = raw_result[count][0]
            # print(start)
            path.insert(0, start)
            count = raw_result[count][1]
        start = raw_result[count][0]
        path.insert(0, start)
    # print(path)
    return path


def extra(maze):
    """
    Runs extra credit suggestion.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return [(8, 25), (8, 24), (8, 23), (9, 23), (10, 23), (11, 23), (11, 22), (11, 21), (11, 20), (11, 19), (11, 18), (11, 17), (10, 17), (10, 16), (10, 15), (10, 14), (9, 14), (8, 14), (8, 13), (8, 12), (8, 11), (8, 10), (8, 9), (7, 9), (6, 9), (6, 10), (6, 11), (6, 12), (6, 11), (6, 10), (6, 9), (7, 9), (8, 9), (9, 9), (10, 9), (10, 10), (10, 9), (10, 8), (10, 7), (9, 7), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1), (8, 1), (8, 2), (8, 3), (7, 3), (6, 3), (6, 2), (6, 1), (5, 1), (4, 1), (4, 2), (3, 2), (2, 2), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (4, 4), (4, 5), (4, 6), (3, 6), (4, 6), (4, 7), (4, 8), (4, 9), (3, 9), (2, 9), (1, 9), (1, 8), (1, 7), (1, 6), (1, 7), (1, 8), (1, 9), (2, 9), (3, 9), (3, 10), (3, 11), (4, 11), (4, 12), (4, 13), (4, 14), (3, 14), (4, 14), (4, 15), (5, 15), (6, 15), (6, 16), (6, 17), (6, 18), (6, 19), (6, 20), (6, 21), (6, 20), (5, 20), (4, 20), (4, 19), (4, 18), (4, 19), (4, 20), (4, 21), (4, 22), (4, 23), (5, 23), (5, 24), (5, 25), (5, 26), (5, 27), (5, 28), (5, 29), (5, 30), (5, 31), (5, 32), (5, 33), (5, 32), (4, 32), (3, 32), (2, 32), (1, 32), (2, 32), (2, 33), (2, 34), (3, 34), (3, 35), (3, 36), (4, 36), (5, 36), (6, 36), (7, 36), (8, 36), (8, 35), (8, 34), (8, 33), (7, 33), (7, 32), (7, 33), (8, 33), (8, 34), (8, 35), (8, 36), (9, 36), (9, 37), (9, 38), (9, 39), (9, 40), (9, 41), (9, 42), (9, 43), (9, 42), (9, 41), (9, 40), (8, 40), (7, 40), (6, 40), (5, 40), (4, 40), (3, 40), (3, 41), (3, 42), (2, 42), (3, 42), (3, 41), (3, 40), (4, 40), (5, 40), (5, 41), (6, 41), (7, 41), (7, 42), (7, 43), (6, 43), (6, 44), (6, 45), (7, 45), (8, 45), (9, 45), (9, 46), (9, 47), (10, 47), (11, 47), (11, 46), (11, 45), (11, 44), (11, 43), (11, 42), (11, 41), (11, 40), (11, 39), (11, 38), (11, 37), (11, 36), (11, 35), (10, 35)]
