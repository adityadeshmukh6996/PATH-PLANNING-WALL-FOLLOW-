#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion
from gazebo_msgs.srv import DeleteModel, DeleteModelRequest
from ad_213410_miniprj.msg import startAction, startGoal, startFeedback, startResult 
import sys
import actionlib

rospy.init_node('project')

l = []
r = []
mid = []
theta = 0
move = Twist()
scan = LaserScan()
position = Odometry()


success = True
result = startResult()
def action_callback(goal):
	action_server = actionlib.SimpleActionServer('miniprj_action_server', startAction, action_callback, auto_start=False)
	action_server.start()
	r = rospy.Rate(2)
	success = True
	start = goal.start_drving
	if start == True :
		if action_server.is_preempt_requested():
			action_server.set_preempted()
			success = False
		if success :
			result.final_state = "exited"
			action_server.set_succeeded(result)	


#def me_callback(goal):
#	r = rospy.Rate(2)
#	success = True
#	start = goal.start_drving
#	if start == True :		 
rospy.wait_for_service('/gazebo/delete_model')
delete_model_service = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
kk = DeleteModelRequest()
kk.model_name = "obstacle"
result = delete_model_service(kk)
print(result)
def callback(scan):
		global l, r, mid
		l = scan.ranges[0:35]
		r = scan.ranges[324:359]
		mid = scan.ranges
		return scan

rospy.Subscriber('scan', LaserScan, callback)
pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
def my_callback(position):
		global x,y,z,theta
		x = position.pose.pose.position.x
		y = position.pose.pose.position.y
		quaternion_orient = position.pose.pose.orientation
		[roll,pitch,theta] = euler_from_quaternion([quaternion_orient.x, quaternion_orient.y,
		quaternion_orient.z, quaternion_orient.w])
		return position
rospy.Subscriber('odom', Odometry, my_callback)
while not rospy.is_shutdown():
		rate = rospy.Rate(1)
		if (l == [] and r == []) or (theta == 0 and mid == []):
			continue
		print (l,r)
		while min(l)>=0.5 or min(r)>=0.5:
			move.linear.x = 0.2
			pub.publish(move)
			rate.sleep()

		else:
			move.linear.x=0
			pub.publish(move)
		while  abs(-1.57-theta)>0.1 :
			move.angular.z = 0.1
			pub.publish(move)
		else :
			move.angular.z = 0.0
			pub.publish(move)	
		while min(mid[35:125]) <= 0.9 :
			move.linear.x = 0.2
			print(min(mid[35:125]))
			pub.publish(move)
			rate.sleep()
		else:
			move.linear.x = 0
			pub.publish(move)	
		while theta < 0.0  :
			move.angular.z = 0.1
			pub.publish(move)
			print(theta)
			rate.sleep()
		move.angular.z = 0
		pub.publish(move)
		while min(l)>=0.5 or min(r)>=0.5:
			move.linear.x = 0.2
			pub.publish(move)
			rate.sleep()
#		if action_server.is_preempt_requested():
#			action_server.set_preempted()
#			success = False
#		if success:
#			result.final_state = "exited the maze"
#			action.set_succeeded(result)		
	
	
	

