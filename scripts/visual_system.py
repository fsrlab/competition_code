#! /usr/bin/env python
from numpy import rate
import rospy
from competion_code.srv import *
import _thread

status = 0
point_0 = [0,-1.7]
point_1 = [-1,-3.1]
point_2 = [-0.2,-3.0]
point_3 = [-1.6,-2.8]
point_4 = [-2.3,-0.1]
point_5 = [-2.5,0.8]
points = [point_1,point_2,point_3,point_4,point_5]
point_6 = [-1,-1.7]
def doReq(req):
    global status
    sum = req.x + req.y
    rospy.loginfo("now point is: x = %f,y = %f ",req.x, req.y)
    if abs(point_0[0]-req.x)<0.1 and abs(point_0[1]-req.y)<0.1:
        rospy.loginfo("This is begin point")
        # put relative func at here
        status = 1

    elif abs(point_6[0]-req.x)<0.1 and abs(point_6[1]-req.y)<0.1:
        rospy.loginfo("This is exchange point")
        # put relative func at here
        status = 2
    for index, poi in enumerate(points):
        if abs(poi[0]-req.x)<0.1 and abs(poi[1]-req.y)<0.1:
            rospy.loginfo("This is the %d mineral point",index)
            # put relative func at here
            status = 3
    resp = PointResponse(sum)
    return resp

def main(name):
    global status
    # go to the first point
    response = client.call(x=point_0[0],y=point_0[1])
    rospy.loginfo("response from move_system is %f ",response.result)
    rate = rospy.Rate(10)
    while 1:
        if status == 1:
            # put relative func at here (at begin point)
            rospy.loginfo("scan and range tag")
            status =0
        elif status == 2:
            # put relative func at here (at exchange point)
            rospy.loginfo("exchanging the the mineral at exchange point")
            #next point to go
            response = client.call(x=1,y=2)
            rospy.loginfo("response from move_system is %f ",response.result)
            status =0
        elif status == 3:
            # put relative func at here (at miner point)
            rospy.loginfo("grasping the mineral")
            status =0
        rate.sleep()

if __name__ == "__main__":
    rospy.init_node("visual_system")
    client = rospy.ServiceProxy("target_position",Point)

    try:
        _thread.start_new_thread(main,("main",))
    except Exception as e:
        print ("Error: %s",e)

    while 1:
        server = rospy.Service("grasp_or_loosen",Point,doReq)
        rospy.loginfo("visual_system is ok")
        rospy.spin()

