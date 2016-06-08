#!/usr/bin/env python
import numpy as np
from copy import deepcopy
import random
from setting import *

def qlearn():
	cur_x = start_x
	cur_y = start_y
	# value iteration
	qList = []
	for i in range(itr):
		randNum = random.uniform(0,1)
		randNum2 = random.uniform(0,1)
		command = ""
		intended = ""
		# move left
		if randNum < 0.25:
			intended = "left"
			c = str(0) + str(-1)
			command = generateMove(randNum2, c)
		# move right
		elif randNum < 0.5:
			intended = "right"
			c = str(0) + str(1)
			command = generateMove(randNum2, c)
		# move up
		elif randNum < 0.75:
			intended = "up"
			c = str(-1) + str(0)
			command = generateMove(randNum2, c)
		# move down
		else:
			intended = "down"
			c = str(1) + str(0)
			command = generateMove(randNum2, c)
		
		# move
		new_x = cur_x + command[0]
		new_y = cur_y + command[1]
		if [new_x, new_y] in walls:
			new_x = cur_x
			new_y = cur_y
			r = r_wall
			q = str(cur_x) + str(cur_y) + intended
			left_q = qMapPrev[str(new_x) + str(new_y) + "left"]
			right_q = qMapPrev[str(new_x) + str(new_y) + "right"]
			up_q = qMapPrev[str(new_x) + str(new_y) + "up"]
			down_q = qMapPrev[str(new_x) + str(new_y) + "down"]
			u_i = r + d_factor * max([left_q, right_q, up_q, down_q]) 
			qMapCur[q] = (1-alpha) * qMapPrev[q] + alpha * u_i 
		elif [new_x, new_y] in pits:
			new_x = cur_x
			new_y = cur_y
			r = r_pit
			q = str(cur_x) + str(cur_y) + intended
			u_i = r 
			qMapCur[q] = (1-alpha) * qMapPrev[q] + alpha * u_i 
		elif [new_x, new_y] == goal:
			new_x = start_x
			new_y = start_y
			r = r_goal
			q = str(cur_x) + str(cur_y) + intended
			u_i = r 
			qMapCur[q] = (1-alpha) * qMapPrev[q] + alpha * u_i 
		else:
			new_x = cur_x + command[0]
			new_y = cur_y + command[1]
			r = r_move
			q = str(cur_x) + str(cur_y) + intended
			left_q = qMapPrev[str(new_x) + str(new_y) + "left"]
			right_q = qMapPrev[str(new_x) + str(new_y) + "right"]
			up_q = qMapPrev[str(new_x) + str(new_y) + "up"]
			down_q = qMapPrev[str(new_x) + str(new_y) + "down"]
			u_i = r + d_factor * max([left_q, right_q, up_q, down_q]) 
			qMapCur[q] = (1-alpha) * qMapPrev[q] + alpha * u_i 
		cur_x = new_x
		cur_y = new_y
		# update q maps
		for k in qMapCur.keys():
			qMapPrev[k] = qMapCur[k]
		if i%100 == 0:
			setPolicy()
			qPolicy = []
			for h in range(height):
				for w in range(width):
					qPolicy.append(mapPolicy[h][w])
			qList.append(qPolicy)
	return qList

def generateMove(randNum2, command):
	if randNum2 < p_forward:
		forward = command + "forward"
		return moveMap[forward]
	elif randNum2 < p_forward + p_left:
		left = command + "left"
		return moveMap[left]
	elif randNum2 < p_forward + p_left + p_right:
		right = command + "right"
		return moveMap[right]
	else:
		backward = command + "backward"
		return moveMap[backward]

def setPolicy():
	max_vals = []
	for h in range(height):
		row = []
		for w in range(width):
			if h == goal[0] and w == goal[1]:
				continue
			if [h, w] in walls:
				continue
			if [h, w] in pits:
				continue
#			print qMapCur
			max_action = "W"
			max_val = 0
			left = str(h) + str(w) + "left"
			max_val = qMapCur[left]
			right = str(h) + str(w) + "right"
			if qMapCur[right] > max_val:
				max_val = qMapCur[right]
				max_action = "E"
			up = str(h) + str(w) + "up"
			if qMapCur[up] > max_val:
				max_val = qMapCur[up]
				max_action = "N"
			down = str(h) + str(w) + "down"
			if qMapCur[down] > max_val:
				max_val = qMapCur[down]
				max_action = "S"
			row += [max_val]
			mapPolicy[h][w] = max_action
		max_vals += [row]
