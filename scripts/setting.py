#!/usr/bin/env python
from read_config import read_config

config = read_config()
height = config["map_size"][0]
width = config["map_size"][1]
start = config["start"]
start_x = start[0]
start_y = start[1]
goal = config["goal"]
move_list = config["move_list"]
walls = config["walls"]
pits = config["pits"]
itr = config["max_iterations"]
r_goal = config["reward_for_reaching_goal"]
r_move = config["reward_for_each_step"]
r_wall = config["reward_for_hitting_wall"]
r_pit = config["reward_for_falling_in_pit"]
p_forward = config["prob_move_forward"]
p_backward = config["prob_move_backward"]
p_left = config["prob_move_left"]
p_right = config["prob_move_right"]
d_factor = config["discount_factor"]
threshold = config["threshold_difference"]
alpha = config["learn_rate"]
mapPrev = []
mapCur = []
mapPolicy = []
qMapPrev = {}
qMapCur = {}
moveMap = {}

for h in range(height):
	mapPrev += [[0 for w in range(width)]]
	mapCur += [[0 for w in range(width)]]
	mapPolicy += [["" for w in range(width)]]

mapPolicy[goal[0]][goal[1]] = "GOAL"

for wall in walls:
	try:
		mapPolicy[wall[0]][wall[1]] = "WALL"
		mapPrev[wall[0]][wall[1]] = 0
		mapCur[wall[0]][wall[1]] = 0
	except IndexError:
		continue
    
for pit in pits:
	mapPolicy[pit[0]][pit[1]] = "PIT"
	mapPrev[pit[0]][pit[1]] = 0
	mapCur[pit[0]][pit[1]] = 0

for w in range(width):
	walls += [[-1, w]]
	walls += [[height, w]]
for h in range(height):
	walls += [[h, -1]]
	walls += [[h, width]]

for h in range(height):
	for w in range(width):
		if h == goal[0] and w == goal[1]:
			continue
		left = str(h) + str(w) + "left"
		qMapPrev[left] = 0.0
		qMapCur[left] = 0.0
		right = str(h) + str(w) + "right"
		qMapPrev[right] = 0.0
		qMapCur[right] = 0.0
		up = str(h) + str(w) + "up"
		qMapPrev[up] = 0.0
		qMapCur[up] = 0.0
		down = str(h) + str(w) + "down"
		qMapPrev[down] = 0.0
		qMapCur[down] = 0.0

#print qMapPrev
# map of move commands
# command move left
left = str(0) + str(-1) + "left"
moveMap[left] = [1, 0]
right = str(0) + str(-1) + "right"
moveMap[right] = [-1, 0]
forward = str(0) + str(-1) + "forward"
moveMap[forward] = [0, -1]
backward = str(0) + str(-1) + "backward"
moveMap[backward] = [0, 1]
# command move right
left = str(0) + str(1) + "left"
moveMap[left] = [-1, 0]
right = str(0) + str(1) + "right"
moveMap[right] = [1, 0]
forward = str(0) + str(1) + "forward"
moveMap[forward] = [0, 1]
backward = str(0) + str(1) + "backward"
moveMap[backward] = [0, -1]
# command move up
left = str(-1) + str(0) + "left"
moveMap[left] = [0, -1]
right = str(-1) + str(0) + "right"
moveMap[right] = [0, 1]
forward = str(-1) + str(0) + "forward"
moveMap[forward] = [-1, 0]
backward = str(-1) + str(0) + "backward"
moveMap[backward] = [1, 0]
# command move down
left = str(1) + str(0) + "left"
moveMap[left] = [0, 1]
right = str(1) + str(0) + "right"
moveMap[right] = [0, -1]
forward = str(1) + str(0) + "forward"
moveMap[forward] = [1, 0]
backward = str(1) + str(0) + "backward"
moveMap[backward] = [-1, 0]


