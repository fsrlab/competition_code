#! /usr/bin/env python
from os import stat
import rospy
from competion_code.srv import *
import _thread
status = 0

def doReq(req):
    global status
    sum = req.x + req.y
    rospy.loginfo("target point is: x = %d,y = %d ",req.x, req.y)
    # set status at here
    status = 1
    resp = PointResponse(sum)
    return resp

def main(name):
    global status
    rate = rospy.Rate(10)
    while 1:
        if status == 1:
            pass
        rate.sleep()
        
if __name__ == "__main__":
    rospy.init_node("move_system")
    try:
        _thread.start_new_thread(main,("main",))
    except Exception as e:
        print ("Error: %s",e)

    while 1:
        server = rospy.Service("target_position",Point,doReq)
        rospy.loginfo("move_system is ok")
        rospy.spin()

