# region VEXcode Generated Robot Configuration
import math
import random
from vexcode_vr import *

# Brain should be defined by default
brain = Brain()

drivetrain = Drivetrain("drivetrain", 0)
pen = Pen("pen", 8)
pen.set_pen_width(THIN)
left_bumper = Bumper("leftBumper", 2)
right_bumper = Bumper("rightBumper", 3)
front_eye = EyeSensor("frontEye", 4)
down_eye = EyeSensor("downEye", 5)
front_distance = Distance("frontdistance", 6)
distance = front_distance
magnet = Electromagnet("magnet", 7)
location = Location("location", 9)


# endregion VEXcode Generated Robot Configuration
# ------------------------------------------
#
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode VR Python Project
#
# ------------------------------------------

# Add project code in "main"

def main():
    turns = 0
    start_x = location.position(X, MM)
    start_y = location.position(Y, MM)
    locations = [[start_x, start_y]]
    fastest_route = []
    pen.set_pen_color(GREEN)
    drivetrain.set_drive_velocity(100, PERCENT)
    drivetrain.set_turn_velocity(100, PERCENT)

    # Keep looping until robot is on the finish tile

    while down_eye.detect(RED) == False:
        wait(5, MSEC)
        pen.move(DOWN)

        # Checks if a wall is within the next tile infront of robot

        if front_distance.get_distance(MM) > 260:

            # Stops robot driving off the map
            if location.position(X, MM) == start_x and location.position(Y, MM) == start_y and drivetrain.heading(
                    DEGREES) == 180:
                drivetrain.turn_for(LEFT, 90, DEGREES)

            drivetrain.drive_for(FORWARD, 250, MM)

            current_x = location.position(X, MM)
            current_y = location.position(Y, MM)

            # Have to round position to nearest 50 as sometimes the robot shifts a little while moving

            current_x = 50 * round(current_x / 50)
            current_y = 50 * round(current_y / 50)

            # Removes positions from the array that lead to a dead end

            for loc in locations:
                if loc == [current_x, current_y]:
                    index = locations.index([current_x, current_y])
                    del locations[index:]
                    break

            locations.append([current_x, current_y])

            drivetrain.turn_for(RIGHT, 90, DEGREES)
        else:
            drivetrain.turn_for(LEFT, 90, DEGREES)
    brain.print(locations)
    brain.new_line()

    del locations[0]

    # Loops over the xy coordinates and translates it to directions moved

    prev_x = start_x
    prev_y = start_y
    for loc in locations:
        if prev_x > loc[0]:
            fastest_route.append('Left')
        if prev_x < loc[0]:
            fastest_route.append('Right')
        if prev_y > loc[1]:
            fastest_route.append('Down')
        if prev_y < loc[1]:
            fastest_route.append('Up')
        prev_x = loc[0]
        prev_y = loc[1]
    brain.print(fastest_route)
    brain.new_line()

    return_route = []

    # Reverses directions to finish line so it creates a route to the start

    for direction in reversed(fastest_route):
        if direction == 'Left':
            return_route.append('Right')
        if direction == 'Right':
            return_route.append('Left')
        if direction == 'Up':
            return_route.append('Down')
        if direction == 'Down':
            return_route.append('Up')

    brain.print(return_route)

    # Makes robot return to the start tile

    pen.set_pen_color(BLUE)
    wait(5, MSEC)
    for direction in return_route:
        if direction == 'Left':
            drivetrain.turn_to_heading(270, DEGREES)
            drivetrain.drive_for(FORWARD, 250, MM)
        if direction == 'Right':
            drivetrain.turn_to_heading(90, DEGREES)
            drivetrain.drive_for(FORWARD, 250, MM)
        if direction == 'Up':
            drivetrain.turn_to_heading(0, DEGREES)
            drivetrain.drive_for(FORWARD, 250, MM)
        if direction == 'Down':
            drivetrain.turn_to_heading(180, DEGREES)
            drivetrain.drive_for(FORWARD, 250, MM)

    maze_dictionary = []
    prev_heading = 0
    drivetrain.turn_to_heading(0, DEGREES)

    # Starts mapping maze

    while down_eye.detect(RED) == False:
        wait(5, MSEC)
        wall_left = 0
        wall_right = 0
        wall_up = 0
        wall_down = 0
        tile = ''

        # Looks around current position and makes note of walls

        drivetrain.turn_to_heading(0, DEGREES)
        if front_distance.get_distance(MM) < 70:
            wall_up = 1
        drivetrain.turn_to_heading(90, DEGREES)
        wait(5, MSEC)
        if front_distance.get_distance(MM) < 70:
            wall_right = 1
        drivetrain.turn_to_heading(180, DEGREES)
        wait(5, MSEC)
        if front_distance.get_distance(MM) < 70:
            wall_down = 1
        drivetrain.turn_to_heading(270, DEGREES)
        wait(5, MSEC)
        if front_distance.get_distance(MM) < 70:
            wall_left = 1
        wait(5, MSEC)

        # Makes a tile character based off walls

        if wall_left == 1:
            tile = '|' + tile
        if wall_up == 1 and wall_down == 1:
            tile = tile + '⁐'
        if wall_up == 1 and wall_down == 0:
            tile = tile + '⁀'
        if wall_up == 0 and wall_down == 1:
            tile = tile + '‿'
        if wall_up == 0 and wall_down == 0:
            tile = tile + ' '
        if wall_right == 1:
            tile = tile + '|'

        brain.print(tile)
        brain.new_line()

        current_x = location.position(X, MM)
        current_y = location.position(Y, MM)

        current_x = 50 * round(current_x / 50)
        current_y = 50 * round(current_y / 50)

        maze_dictionary.append({'x': current_x, 'y': current_y, 'tile': tile})

        drivetrain.turn_to_heading(prev_heading, DEGREES)

        moved_tile = False
        while moved_tile == False:
            wait(5, MSEC)
            if front_distance.get_distance(MM) > 260:
                if location.position(X, MM) == (50 * round(start_x / 50)) and location.position(Y, MM) == (
                        50 * round(start_y / 50)) and drivetrain.heading(DEGREES) == 180:
                    drivetrain.turn_for(RIGHT, 90, DEGREES)
                drivetrain.drive_for(FORWARD, 250, MM)
                drivetrain.turn_for(RIGHT, 90, DEGREES)
                prev_heading = drivetrain.heading(DEGREES)
                moved_tile = True
            else:
                drivetrain.turn_for(LEFT, 90, DEGREES)
                prev_heading = drivetrain.heading(DEGREES)

    # Grabs unique values

    unique = []
    for val in maze_dictionary:
        if val not in unique:
            unique.append(val)

    brain.print(unique)
    brain.new_line()

    # Prints of the maze to console

    row1 = []
    for val in unique:
        if val['y'] == 850:
            row1.append(val)

    x = -850
    for i in range(8):
        tile_found = False
        for val in row1:
            if val['x'] > x - 100 and val['x'] < x + 100:
                brain.print(val['tile'])
                tile_found = True
        if tile_found == False:
            brain.print('??')
        x = x + 250
    brain.new_line()
    x = -850

    row2 = []
    for val in unique:
        if val['y'] == 600:
            row2.append(val)

    x = -850
    for i in range(8):
        tile_found = False
        for val in row2:
            if val['x'] > x - 100 and val['x'] < x + 100:
                brain.print(val['tile'])
                tile_found = True
        if tile_found == False:
            brain.print('??')
        x = x + 250
    brain.new_line()
    x = -850

    row3 = []
    for val in unique:
        if val['y'] == 350:
            row3.append(val)

    x = -850
    for i in range(8):
        tile_found = False
        for val in row3:
            if val['x'] > x - 100 and val['x'] < x + 100:
                brain.print(val['tile'])
                tile_found = True
        if tile_found == False:
            brain.print('??')
        x = x + 250
    brain.new_line()
    x = -850

    row4 = []
    for val in unique:
        if val['y'] == 100:
            row4.append(val)

    x = -850
    for i in range(8):
        tile_found = False
        for val in row4:
            if val['x'] > x - 100 and val['x'] < x + 100:
                brain.print(val['tile'])
                tile_found = True
        if tile_found == False:
            brain.print('??')
        x = x + 250
    brain.new_line()
    x = -850

    row5 = []
    for val in unique:
        if val['y'] == -150:
            row5.append(val)

    x = -850
    for i in range(8):
        tile_found = False
        for val in row5:
            if val['x'] > x - 100 and val['x'] < x + 100:
                brain.print(val['tile'])
                tile_found = True
        if tile_found == False:
            brain.print('??')
        x = x + 250
    brain.new_line()
    x = -850

    row6 = []
    for val in unique:
        if val['y'] == -400:
            row6.append(val)

    x = -850
    for i in range(8):
        tile_found = False
        for val in row6:
            if val['x'] > x - 100 and val['x'] < x + 100:
                brain.print(val['tile'])
                tile_found = True
        if tile_found == False:
            brain.print('??')
        x = x + 250
    brain.new_line()
    x = -850

    row7 = []
    for val in unique:
        if val['y'] == -650:
            row7.append(val)

    x = -850
    for i in range(8):
        tile_found = False
        for val in row7:
            if val['x'] > x - 100 and val['x'] < x + 100:
                brain.print(val['tile'])
                tile_found = True
        if tile_found == False:
            brain.print('??')
        x = x + 250
    brain.new_line()
    x = -850

    row8 = []
    for val in unique:
        if val['y'] == -900:
            row8.append(val)

    x = -850
    for i in range(8):
        tile_found = False
        for val in row8:
            if val['x'] > x - 100 and val['x'] < x + 100:
                brain.print(val['tile'])
                tile_found = True
        if tile_found == False:
            brain.print('??')
        x = x + 250


# VR threads — Do not delete
vr_thread(main)