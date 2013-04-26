#!/usr/bin/env python

"""
voice_cmd_vel.py is a simple demo of speech recognition.
  You can control a mobile base using commands found
  in the corpus file.
"""
#import argparse
#parser = argparse.ArgumentParser()
#parser.add_argument("--quiet", help="mute the robot voice", action="store_true")
#args = parser.parse_args()
#if args.quiet:
#    print("robot quiet")

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
        self.loud = True
        #if args.quiet:
        #    self.loud = False
        #print(self.args)
        rospy.on_shutdown(self.cleanup)
        self.speed = 0.2
        self.msg = Joy()

        # publish to cmd_vel, subscribe to speech output
        self.pub_ = rospy.Publisher('joy', Joy)
        rospy.Subscriber('recognizer/output', String, self.speechCb)
	#print "here"
        r = rospy.Rate(10.0)
        if self.loud:
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
	default_buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        motion_buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        open_right_buttons = list(motion_buttons)
        close_right_buttons = list(motion_buttons)
        open_left_buttons = list(motion_buttons)
        close_left_buttons = list(motion_buttons)
        select_buttons = list(default_buttons)
        start_buttons = list(default_buttons)
        triangle_buttons = list(default_buttons)
        #13 = right open
        # 0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5  6
        #[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        #[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        open_right_buttons[13] = 1
        close_right_buttons[15] = 1
        open_left_buttons[5] = 1
        close_left_buttons[7] = 1
        select_buttons[0] = 1
        start_buttons[3] = 1
        triangle_buttons[12] = 1
        if msg.data.find("open right gripper") > -1:
            self.msg = Joy(Header(), axes, open_right_buttons)
            self.pub_.publish(self.msg)
            if self.loud:
                self.soundhandle.say("open right gripper", self.voice)
        if msg.data.find("close right gripper") > -1:
            self.msg = Joy(Header(), axes, close_right_buttons)
            self.pub_.publish(self.msg)
            if self.loud:
                self.soundhandle.say("close right gripper", self.voice)
        if msg.data.find("open left gripper") > -1:
            self.msg = Joy(Header(), axes, open_left_buttons)
            self.pub_.publish(self.msg)
            if self.loud:
                self.soundhandle.say("open left gripper", self.voice)
        if msg.data.find("close left gripper") > -1:
            self.msg = Joy(Header(), axes, close_left_buttons)
            self.pub_.publish(self.msg)
            if self.loud:
                self.soundhandle.say("close left gripper", self.voice)
   	if msg.data.find("start recording") > -1:
            self.msg = Joy(Header(), axes, select_buttons)
            self.pub_.publish(self.msg)
            if self.loud:
                self.soundhandle.say("start recording", self.voice)
        if msg.data.find("stop recording") > -1:
            self.msg = Joy(Header(), axes, start_buttons)
            self.pub_.publish(self.msg)
            if self.loud:
                self.soundhandle.say("stop recording", self.voice)
        if msg.data.find("robot look") > -1:
            self.msg = Joy(Header(), axes, triangle_buttons)
            self.pub_.publish(self.msg)
            if self.loud:
                self.soundhandle.say("robot look", self.voice)

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
