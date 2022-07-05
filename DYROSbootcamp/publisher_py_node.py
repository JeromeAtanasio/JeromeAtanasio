#!/usr/bin/env python
# license removed for brevity

import rospy
from std_msgs.msg import Int32


def talker():
    pub = rospy.Publisher('/helloros_topic', Int32, queue_size=10)
    rospy.init_node('dyros_publisher_node', anonymous=True)
    rate = rospy.Rate(1)  #1hz
    i = 1
    while not rospy.is_shutdown():
        pub.publish(i)
        i = i + 1
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
