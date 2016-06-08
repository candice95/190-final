#!/usr/bin/env python

import rospy
from read_config import read_config
from astar import astar
from mdp import mdp
from qlearn import *
from cse_190_assi_3.msg import *
from std_msgs.msg import Bool

class Robot():
	def __init__(self):
		self.config = read_config()
		rospy.init_node("robot")
		self.path_publisher = rospy.Publisher(
			"/results/path_list",
			AStarPath,
			queue_size = 10
		)
		self.mdp_publisher = rospy.Publisher(
			"/results/policy_list",
			PolicyList,	
			queue_size = 10
		)
		self.qlearn_publisher = rospy.Publisher(
			"/results/qlearn_policy_list",
			PolicyList,	
			queue_size = 10
		)
		self.complete_publisher = rospy.Publisher(
			"/map_node/sim_complete",
			Bool,
			queue_size = 10
		)
		qPolicy = qlearn()
		for eachPolicy in qPolicy:
			rospy.sleep(1)
			self.qlearn_publisher.publish(eachPolicy)
		rospy.sleep(1)
		paths = astar(self.config)
		for eachEntry in paths:
			rospy.sleep(1)
			self.path_publisher.publish(eachEntry)
		mdps = mdp(self.config)
		rospy.sleep(1)
		self.mdp_publisher.publish(mdps)
		rospy.sleep(1)
		self.complete_publisher.publish(True)
		rospy.sleep(1)
		rospy.signal_shutdown("shutting down")
if __name__ == '__main__':
	robot = Robot()
