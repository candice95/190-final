#!/usr/bin/env python
from Queue import *

def astar(config):
	height = config["map_size"][0]
	width = config["map_size"][1]
	start = config["start"]
	start_x = start[0]
	start_y = start[1]
	goal = config["goal"]
	move_cost = config["reward_for_each_step"]
	move_list = config["move_list"]
	walls = config["walls"]
	pits = config["pits"]

	
	map_heuristic = []
	for h in range(height):
		map_heuristic += [[0 for w in range(width)]]
	# heuristic map initialization
	map_heuristic[goal[0]][goal[1]] = 0
	for h in range(height):
		for w in range(width):
			map_heuristic[h][w] = abs(h-goal[0]) + abs(w-goal[1])

	path = {}
	pq = PriorityQueue()
	pq.put((0+map_heuristic[start_x][start_y], 0, start, start))
	visited = []
	while not pq.empty():
		visit = pq.get()
		cost = visit[1]
		x = visit[2][0]
		y = visit[2][1]
		if visit[2] in visited:
			continue
		visited.append(visit[2])
		path[(x,y)] = visit[3] 
		if x == goal[0] and y == goal[1]:
			break
		if x-1 >= 0:
			newCost = cost + 1
			move = move_list[3]
			newX = x + move[0]
			if [newX, y] not in walls and [newX, y] not in pits and [newX, y] not in visited:
				pq.put((newCost + map_heuristic[newX][y], newCost, [newX, y], [x,y]))
		if x+1 < height:
			newCost = cost + 1
			move = move_list[2]
			newX = x + move[0]
			if [newX, y] not in walls and [newX, y] not in pits and [newX, y] not in visited:
				pq.put((newCost + map_heuristic[newX][y], newCost, [newX, y], [x,y]))
		if y-1 >= 0:
			newCost = cost + 1
			move = move_list[1]
			newY = y + move[1]
			if [x, newY] not in walls and [x, newY] not in pits and [x, newY] not in visited:
				pq.put((newCost + map_heuristic[x][newY], newCost, [x, newY], [x,y]))
		if y+1 < width:
			newCost = cost + 1
			move = move_list[0]
			newY = y + move[1]
			if [x, newY] not in walls and [x, newY] not in pits and [x, newY] not in visited:
				pq.put((newCost + map_heuristic[x][newY], newCost, [x, newY], [x,y]))
	
	actual_path = []
	s = (start[0], start[1])
	state = (goal[0], goal[1])
	while state != s:
		actual_path = [path[state]] + actual_path
		state = (path[state][0], path[state][1])
	actual_path = actual_path + [goal]
	
	return actual_path
