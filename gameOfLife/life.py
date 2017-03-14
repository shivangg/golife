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


def get_json(pathname):
    # to store the mentioned values
    yes = ['y', 'yes', 'Yes', 'YES', '']
    no = ['n', 'not', 'No', 'NO']

    # to store settings and points data
    data = []

    # open the config from the provided JSON file
    with open(pathname, 'r') as data_file:
        seed = json.load(data_file)

    # to make the entries in seed stay ordered
    seed = OrderedDict(sorted(seed.items()))

    print("Use the default settings? (Y/n)")
    choice_setting = input()

    if choice_setting in yes:
        steps, size, time_interval = int(seed['steps']), int(seed['size']), float(seed['time_interval'])

    elif choice_setting in no:
        print("The current settings will be  set as default.\nEnter the number steps you want (integer) ")
        steps = int(input())
        print("Enter the size of square world you want (integer)")
        size = int(input())
        print("Enter the time interval you want between 2 steps (integer)")
        time_interval = float(input())

    else:
        print("Invalid choice")
        return

    # set the current supplied data as new default
    seed["steps"] = steps
    seed["size"] = size
    seed["time_interval"] = time_interval

    # write the new default into the JSON file
    with open(pathname, "w") as jsonFile:
        json.dump(seed, jsonFile, indent=4, separators=(', ', ': '))

    # for choices in seed:
    print("Enter choice for the world between 1 and ", len(seed.items()) - 3)
    choices = int(input()) - 1

    # set to store the yx coordinates
    world_json_points = set()
    for y in seed[str(choices)]:
        for x in seed[str(choices)][y]:
            point = (int(y), int(x))
            world_json_points.add(point)

    data.append(world_json_points)
    data.append(steps)
    data.append(size)
    data.append(time_interval)

    return data


def neighbors(cell, distance=1):
    # Return the neighbors at specified distance
    x, y = cell
    r = range(0 - distance, 1 + distance)
    return ((x + i, y + j)  # new cell difference from center
            for i in r for j in r  # iterate over range in 2d
            if not i == j == 0)  # exclude the center cell


def advance(board):
    # Advance the board one generation and return it.
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
    size_x = size_y = size or 0
    for x, y in board:
        size_x = x if x > size_x else size_x
        size_y = y if y > size_y else size_y
    for i in range(0, size_x):
        for j in range(0, size_y):
            sys.stdout.write(' x ' if (i, j) in board else ' . ')
        print()


def constrain(board, size):
    return set(cell for cell in board if cell[0] <= size and cell[1] <= size)


def main(pathname="data.json"):
    settings_data = get_json(pathname)
    board = settings_data[0]
    steps = settings_data[1]
    size = settings_data[2]
    time_interval = settings_data[3]
    # print(board)
    for i in range(1, steps + 1):
        # move to the top of the screen
        sys.stdout.write('\033[H')
        # clear the screen
        sys.stdout.write('\033[J')
        # step number
        print('step:' + str(i) + '/' + str(steps))
        print_board(board, size)
        time.sleep(time_interval)
        board = constrain(advance(board), size)


if __name__ == '__main__':
    main()
