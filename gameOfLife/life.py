"""Python implementation of Conway's Game of Life

Somewhat inspired by Jack Diederich's talk `Stop Writing Classes`
http://pyvideo.org/video/880/stop-writing-classes

Ironically, as I extended the functionality of this module it seems obvious
that the next step would be to refactor board into a class with advance and
constrain as methods and print_board as __str__.
"""

import sys
import time
import json
from collections import OrderedDict

# JSON file usage
# 1. top left is origin
# 2. key     ==> y
# 3. value   ==> array of x
# 4. y: [x1,xy2, ...]
# for example see data.json

def getJSON(pathname):
 
     # open the config from the provided JSON file
    with open(pathname, 'r') as data_file:    
        seed = json.load(data_file)

    seed = OrderedDict(sorted(seed.items()))
    # print(seed['0'])
    print(seed['steps'], seed['size'], seed['time_interval'])

    steps = size = time = 0

    print("TO use Default settin,press(Y/n)")
    choiceSetting = input()
    if choiceSetting is 'Y' or choiceSetting is 'yes' or choiceSetting is 'Yes' or choiceSetting is '':
        steps, size, time = int(seed['steps']), int(seed['size']), float(seed['time_interval'])
    elif choiceSetting is 'n' or choiceSetting is 'N' or choiceSetting is 'no' or choiceSetting is 'No':
        print("THe current settings will be  set as default.")
        print("Enter the number steps you want (integer)")
        steps = int(input())
        print("Enter the size of square world you want (integer)")
        size = int(input())
        print("Enter the time interval you want between 2 steps (integer)")
        time = float(input())
    else:
        print("Invalid choice")
        return

    # set the current supplied data as new Default
    seed["steps"] = steps
    seed["size"] = size
    seed["time_interval"] = time

    with open(pathname, "w") as jsonFile:
        json.dump(seed, jsonFile,  indent=4, separators=(', ', ': '))


    # to store settings and points data
    data = []

    # for choices in seed:
    print("Enter choice for the world between 1 and ", len(seed.items()) - 3)
    choices = int(input()) - 1
    # print(seed[str(choices)])
        # print(seed[choices])
    # set to store the xy coordinates
    world_JSON_points = set()
    for y in seed[str(choices)]:
        # print(seed[choices][y])
        for x in seed[str(choices)][y]:
            point = (int(y), int(x))
            world_JSON_points.add(point)

    data.append(world_JSON_points)
    data.append(steps)
    data.append(size)
    data.append(time)

    return(data)



def neighbors(cell, distance=1):
    """Return the neighbors of cell."""
    x, y = cell
    r = range(0 - distance, 1 + distance)
    return ((x + i, y + j) # new cell offset from center
        for i in r for j in r # iterate over range in 2d
        if not i == j == 0  ) # exclude the center cell


def advance(board):
    """Advance the board one step and return it."""
    new_board = set()
    for cell in board:
        cell_neighbors = set(neighbors(cell))
        # test if live cell dies
        if len(board & cell_neighbors) in [2, 3]:
            new_board.add(cell)
        # test dead neighbors to see if alive
        for n in cell_neighbors:
            if len(board & set(neighbors(n))) is 3:
                new_board.add(n)
    return new_board


def print_board(board, size=None):
    sizex = sizey = size or 0
    for x, y in board:
        sizex = x if x > sizex else sizex
        sizey = y if y > sizey else sizey
    for i in range(0, sizex ):
        for j in range(0, sizey):
            sys.stdout.write(' x ' if (i, j) in board else ' . ')
        print()


def constrain(board, size):
    return set(cell for cell in board if cell[0] <= size and cell[1] <= size)


def main(pathname="data.json", steps=175, size=25):
    settings_data = getJSON(pathname)
    board = settings_data[0]
    steps = settings_data[1]
    size = settings_data[2]
    timep = settings_data[3]
    # print(board)
    for i in range(1, steps + 1):
        # move to the top of the screen
        sys.stdout.write('\033[H')
        # clear the screen
        sys.stdout.write('\033[J')
        # step number
        print('step:'+ str(i)+ '/' + str(steps))
        print_board(board, size)
        time.sleep(timep)
        board = constrain(advance(board), size)


if __name__ == '__main__':
    main()