#!/usr/bin/env python
import numpy as np
from copy import deepcopy

def mdp(config):
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
    
	mapPrev = []
	mapCur = []
	mapPolicy = []

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

	mapPrev[goal[0]][goal[1]] = 0
	mapCur[goal[0]][goal[1]] = 0
	iterate = True
	for i in range(itr):
#		if i == 1:
#			break
		if iterate is not True:
			break
		iterate = False
		for x in range(height):
			for y in range(width):
				if x == goal[0] and y == goal[1]:
					continue
				elif [x,y] in walls or [x,y] in pits:
					continue
				else:
					# move command left: [x,y] -> [x,y-1]
					r_forward = r_move
					u_forward = 0
					if [x, y-1] in walls:
						r_forward += r_wall
						u_forward = d_factor * mapPrev[x][y]
					elif [x, y-1] in pits:
						r_forward += r_pit
						u_forward = d_factor * mapPrev[x][y-1]
					elif [x, y-1] == goal:
						r_forward += r_goal
						u_forward = d_factor * mapPrev[x][y-1]
					else:
						u_forward = d_factor * mapPrev[x][y-1]

					r_backward = r_move
					u_backward = 0
					if [x, y+1] in walls:
						r_backward += r_wall
						u_backward = d_factor * mapPrev[x][y]
					elif [x, y+1] in pits:
						r_backward += r_pit
						u_backward = d_factor * mapPrev[x][y+1]
					elif [x, y+1] == goal:
						r_backward += r_goal
						u_backward = d_factor * mapPrev[x][y+1]
					else:
						u_backward = d_factor * mapPrev[x][y+1]

					r_left = r_move
					u_left = 0
					if [x+1, y] in walls:
						r_left += r_wall
						u_left = d_factor * mapPrev[x][y]
					elif [x+1, y] in pits:
						r_left += r_pit
						u_left = d_factor * mapPrev[x+1][y]
					elif [x+1, y] == goal:
						r_left += r_goal
						u_left = d_factor * mapPrev[x+1][y]
					else:
						u_left = d_factor * mapPrev[x+1][y]

					r_right = r_move
					u_right = 0
					if [x-1, y] in walls:
						r_right += r_wall
						u_right = d_factor * mapPrev[x][y]
					elif [x-1, y] in pits:
						r_right += r_pit
						u_right = d_factor * mapPrev[x-1][y]
					elif [x-1, y] == goal:
						r_right += r_goal
						u_right = d_factor * mapPrev[x-1][y]
					else:
						u_right = d_factor * mapPrev[x-1][y]

					left_sum = p_forward * (r_forward + u_forward) + p_backward * (r_backward + u_backward) + p_left * (r_left + u_left) + p_right * (r_right + u_right)
					
					
					# move command right: [x,y] -> [x,y+1]
					r_forward = r_move
					u_forward = 0
					if [x, y+1] in walls:
						r_forward += r_wall
						u_forward = d_factor * mapPrev[x][y]
					elif [x, y+1] in pits:
						r_forward += r_pit
						u_forward = d_factor * mapPrev[x][y+1]
					elif [x, y+1] == goal:
						r_forward += r_goal
						u_forward = d_factor * mapPrev[x][y+1]
					else:
						u_forward = d_factor * mapPrev[x][y+1]

					r_backward = r_move
					u_backward = 0
					if [x, y-1] in walls:
						r_backward += r_wall
						u_backward = d_factor * mapPrev[x][y]
					elif [x, y-1] in pits:
						r_backward += r_pit
						u_backward = d_factor * mapPrev[x][y-1]
					elif [x, y-1] == goal:
						r_backward += r_goal
						u_backward = d_factor * mapPrev[x][y-1]
					else:
						u_backward = d_factor * mapPrev[x][y-1]

					r_left = r_move
					u_left = 0
					if [x-1, y] in walls:
						r_left += r_wall
						u_left = d_factor * mapPrev[x][y]
					elif [x-1, y] in pits:
						r_left += r_pit
						u_left = d_factor * mapPrev[x-1][y]
					elif [x-1, y] == goal:
						r_left += r_goal
						u_left = d_factor * mapPrev[x-1][y]
					else:
						u_left = d_factor * mapPrev[x-1][y]

					r_right = r_move
					u_right = 0
					if [x+1, y] in walls:
						r_right += r_wall
						u_right = d_factor * mapPrev[x][y]
					elif [x+1, y] in pits:
						r_right += r_pit
						u_right = d_factor * mapPrev[x+1][y]
					elif [x+1, y] == goal:
						r_right += r_goal
						u_right = d_factor * mapPrev[x+1][y]
					else:
						u_right = d_factor * mapPrev[x+1][y]

					right_sum = p_forward * (r_forward + u_forward) + p_backward * (r_backward + u_backward) + p_left * (r_left + u_left) + p_right * (r_right + u_right)
					
					# move command up: [x,y] -> [x-1,y]
					r_forward = r_move
					u_forward = 0
					if [x-1, y] in walls:
						r_forward += r_wall
						u_forward = d_factor * mapPrev[x][y]
					elif [x-1, y] in pits:
						r_forward += r_pit
						u_forward = d_factor * mapPrev[x-1][y]
					elif [x-1, y] == goal:
						r_forward += r_goal
						u_forward = d_factor * mapPrev[x-1][y]
					else:
						u_forward = d_factor * mapPrev[x-1][y]

					r_backward = r_move
					u_backward = 0
					if [x+1, y] in walls:
						r_backward += r_wall
						u_backward = d_factor * mapPrev[x][y]
					elif [x+1, y] in pits:
						r_backward += r_pit
						u_backward = d_factor * mapPrev[x+1][y]
					elif [x+1, y] == goal:
						r_backward += r_goal
						u_backward = d_factor * mapPrev[x+1][y]
					else:
						u_backward = d_factor * mapPrev[x+1][y]

					r_left = r_move
					u_left = 0
					if [x, y-1] in walls:
						r_left += r_wall
						u_left = d_factor * mapPrev[x][y]
					elif [x, y-1] in pits:
						r_left += r_pit
						u_left = d_factor * mapPrev[x][y-1]
					elif [x, y-1] == goal:
						r_left += r_goal
						u_left = d_factor * mapPrev[x][y-1]
					else:
						u_left = d_factor * mapPrev[x][y-1]

					r_right = r_move
					u_right = 0
					if [x, y+1] in walls:
						r_right += r_wall
						u_right = d_factor * mapPrev[x][y]
					elif [x, y+1] in pits:
						r_right += r_pit
						u_right = d_factor * mapPrev[x][y+1]
					elif [x, y+1] == goal:
						r_right += r_goal
						u_right = d_factor * mapPrev[x][y+1]
					else:
						u_right = d_factor * mapPrev[x][y+1]

					up_sum = p_forward * (r_forward + u_forward) + p_backward * (r_backward + u_backward) + p_left * (r_left + u_left) + p_right * (r_right + u_right)
					
					# move command down: [x,y] -> [x+1,y]
					r_forward = r_move
					u_forward = 0
					if [x+1, y] in walls:
						r_forward += r_wall
						u_forward = d_factor * mapPrev[x][y]
					elif [x+1, y] in pits:
						r_forward += r_pit
						u_forward = d_factor * mapPrev[x+1][y]
					elif [x+1, y] == goal:
						r_forward += r_goal
						u_forward = d_factor * mapPrev[x+1][y]
					else:
						u_forward = d_factor * mapPrev[x+1][y]

					r_backward = r_move
					u_backward = 0
					if [x-1, y] in walls:
						r_backward += r_wall
						u_backward = d_factor * mapPrev[x][y]
					elif [x-1, y] in pits:
						r_backward += r_pit
						u_backward = d_factor * mapPrev[x-1][y]
					elif [x-1, y] == goal:
						r_backward += r_goal
						u_backward = d_factor * mapPrev[x-1][y]
					else:
						u_backward = d_factor * mapPrev[x-1][y]

					r_left = r_move
					u_left = 0
					if [x, y+1] in walls:
						r_left += r_wall
						u_left = d_factor * mapPrev[x][y]
					elif [x, y+1] in pits:
						r_left += r_pit
						u_left = d_factor * mapPrev[x][y+1]
					elif [x, y+1] == goal:
						r_left += r_goal
						u_left = d_factor * mapPrev[x][y+1]
					else:
						u_left = d_factor * mapPrev[x][y+1]

					r_right = r_move
					u_right = 0
					if [x, y-1] in walls:
						r_right += r_wall
						u_right = d_factor * mapPrev[x][y]
					elif [x, y-1] in pits:
						r_right += r_pit
						u_right = d_factor * mapPrev[x][y-1]
					elif [x, y-1] == goal:
						r_right += r_goal
						u_right = d_factor * mapPrev[x][y-1]
					else:
						u_right = d_factor * mapPrev[x][y-1]

					down_sum = p_forward * (r_forward + u_forward) + p_backward * (r_backward + u_backward) + p_left * (r_left + u_left) + p_right * (r_right + u_right)
					
					sums = [down_sum, up_sum, left_sum, right_sum]
					max_sum = max(sums)
					if down_sum == max_sum:
						mapPolicy[x][y] = "S"
					elif up_sum == max_sum:
						mapPolicy[x][y] = "N"
					elif left_sum == max_sum:
						mapPolicy[x][y] = "W"
					elif right_sum == max_sum:
						mapPolicy[x][y] = "E"
					

					mapCur[x][y] = max_sum
		diff_sum = 0
		for x_ in range(height):
			for y_ in range(width):
				if [x_, y_] in walls or [x_, y_] in pits or [x_, y_] == goal:
					continue
				diff_sum += abs(mapCur[x_][y_] - mapPrev[x_][y_])
		if diff_sum > threshold:
			iterate = True
		mapPrev = deepcopy(mapCur)			

	policyList = []
	for h in range(height):
		for w in range(width):
			policyList.append(mapPolicy[h][w])
	return policyList
					
					
					


					


