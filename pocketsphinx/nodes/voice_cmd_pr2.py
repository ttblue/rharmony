#!/usr/bin/env python

"""
voice_cmd_vel.py is a simple demo of speech recognition.
  You can control a mobile base using commands found
  in the corpus file.
"""

import roslib; roslib.load_manifest('pocketsphinx')
import rospy
import math

from std_msgs.msg import String

from sensor_msgs.msg import Joy
import roslib
from std_msgs.msg import Header
from sound_play.libsoundplay import SoundClient
class voice_cmd_pr2:

    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        self.speed = 0.2
        self.msg = Joy()

        # publish to cmd_vel, subscribe to speech output
        self.pub_ = rospy.Publisher('joy', Joy)
        rospy.Subscriber('recognizer/output', String, self.speechCb)
	#print "here"
        r = rospy.Rate(10.0)
	self.soundhandle = SoundClient()
	self.voice = 'voice_kal_diphone'
	self.soundhandle.say("open gripper", self.voice)
        while not rospy.is_shutdown():
        #    self.pub_.publish(self.msg)
            r.sleep()
	#self.soundhandle = SoundClient()
        
    def speechCb(self, msg):
        rospy.loginfo(msg.data)
        axes = [0]*20
        motion_buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        open_right_buttons = list(motion_buttons)
        #13 = right open
        #open_right_buttons[13] = 1
        open_right_buttons[11] = 1
        if msg.data.find("open right gripper") > -1:
            #print "got open right gripper"
            #self.msg = Joy(Header(),[-0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.493912935256958, 0.0, -0.0, -0.613559365272522, -0.0, -0.0, -0.0, -0.0, 0.07150902599096298, 0.0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0])
            self.msg = Joy(Header(), axes, open_right_buttons)
            #print "got open right gripper"
            
            self.pub_.publish(self.msg)
            self.soundhandle.say("okay fine i will open right gripper", self.voice)
    def cleanup(self):
        # stop the robot!
        j = Joy()
        self.pub_.publish(j)

if __name__=="__main__":
    rospy.init_node('voice_cmd_pr2')
    try:
        voice_cmd_pr2()
    except:
        pass

