#!/usr/bin/env python
__author__ = 'flier'

import argparse

import rospy
import leap_interface
from leap_motion.msg import leap
from leap_motion.msg import leapros

FREQUENCY_ROSTOPIC_DEFAULT = 0.01
PARAMNAME_FREQ = '/leapmotion/freq'

# Obviously, this method publishes the data defined in leapros.msg to /leapmotion/data
def sender(freq=FREQUENCY_ROSTOPIC_DEFAULT):
    '''
    @param freq: Frequency to publish sensed info as ROS message
    '''
    rospy.set_param(PARAMNAME_FREQ, freq)
    rospy.loginfo("Parameter set on server: PARAMNAME_FREQ={}, freq={}".format(rospy.get_param(PARAMNAME_FREQ, FREQUENCY_ROSTOPIC_DEFAULT), freq))

    li = leap_interface.Runner()
    li.setDaemon(True)
    li.start()
    # pub     = rospy.Publisher('leapmotion/raw',leap)
    pub_ros   = rospy.Publisher('leapmotion/data',leapros)
    rospy.init_node('leap_pub')

    while not rospy.is_shutdown():
        hand_direction_   = li.get_hand_direction()
        hand_normal_      = li.get_hand_normal()
        hand_palm_pos_    = li.get_hand_palmpos()
        hand_pitch_       = li.get_hand_pitch()
        hand_roll_        = li.get_hand_roll()
        hand_yaw_         = li.get_hand_yaw()
        thumb_position_   = li.get_thumb_position()
        index_position_   = li.get_index_position()
        pinky_position_   = li.get_pinky_position()
        hand_validity_    = li.get_hand_validity()
        msg = leapros()
        msg.direction.x = hand_direction_[0]
        msg.direction.y = hand_direction_[1]
        msg.direction.z = hand_direction_[2]
        msg.normal.x = hand_normal_[0]
        msg.normal.y = hand_normal_[1]
        msg.normal.z = hand_normal_[2]
        msg.palmpos.x = hand_palm_pos_[0]
        msg.palmpos.y = hand_palm_pos_[1]
        msg.palmpos.z = hand_palm_pos_[2]
        msg.ypr.x = hand_yaw_
        msg.ypr.y = hand_pitch_
        msg.ypr.z = hand_roll_
        msg.thumb_pos.x = thumb_position_[0]
        msg.thumb_pos.y = thumb_position_[1]
        msg.thumb_pos.z = thumb_position_[2]
        msg.index_pos.x = index_position_[0]
        msg.index_pos.y = index_position_[1]
        msg.index_pos.z = index_position_[2]
        msg.pinky_pos.x = pinky_position_[0]
        msg.pinky_pos.y = pinky_position_[1]
        msg.pinky_pos.z = pinky_position_[2]    
        msg.hand_valid = hand_validity_            
        # We don't publish native data types, see ROS best practices
        # pub.publish(hand_direction=hand_direction_,hand_normal = hand_normal_, hand_palm_pos = hand_palm_pos_, hand_pitch = hand_pitch_, hand_roll = hand_roll_, hand_yaw = hand_yaw_)
        pub_ros.publish(msg)
        rospy.sleep(rospy.get_param(PARAMNAME_FREQ, FREQUENCY_ROSTOPIC_DEFAULT))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='LeapMotion ROS driver. Message Sender module to ROS world using LeapSDK.')
    parser.add_argument('--freq', help='Frequency to publish sensed info as ROS message', type=float)
    args, unknown = parser.parse_known_args()
    if not args.freq:
        args.freq = FREQUENCY_ROSTOPIC_DEFAULT
    try:
        sender(args.freq)
    except rospy.ROSInterruptException:
        pass
