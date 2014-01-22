#!/usr/bin/env python


import roslib; roslib.load_manifest('pocketsphinx')
import rospy
import math
import subprocess
from std_msgs.msg import String
import time

from pocketsphinx.msg import Segment
import roslib
from std_msgs.msg import Header
from sound_play.libsoundplay import SoundClient



# parent_state = {"begin recording": ["all start", "finish recording", "cancel recording"],
#                 "robot look": ["begin recording", "stop segment"],
#                 "begin segment": ["robot look"],
#                 "stop segment": ["begin segment", "new segment"],
#                 "new segment": ["stop segment"],
#                 "stop recording": ["stop segment"],
#                 "finish recording": ["stop recording"],
#                 "cancel recording": ["stop recording", "begin recording", "robot look", "begin segment", "stop segment", "new segment"]}
# old parent stuff

# parent_state = {"begin recording": ["all start", "finish recording", "cancel recording"],
#                 "robot look": ["begin recording", "stop segment", "robot look"],
#                 "begin segment": ["robot look"],
#                 "stop segment": ["begin segment", "new segment"],
#                 "new segment": ["stop segment","begin recording"],
#                 "stop recording": ["stop segment"],
#                 "finish recording": ["stop recording", "stop segment"],
#                 "cancel recording": ["stop recording", "begin recording", "robot look", "begin segment", "stop segment", "new segment"],
#                 "done session": ["finish recording", "cancel recording", "all start"]}


parent_state = {"begin recording": ["all start", "finish recording", "cancel recording"],
                "robot look": ["begin recording", "stop segment", "robot look"],
                "begin segment": ["robot look"],
                "stop segment": ["begin segment", "new segment"],
                "new segment": ["stop segment","begin recording"],
                "check demo": ["stop segment"],
                "finish recording": ["check demo", "stop segment"],
                "cancel recording": ["check demo", "begin recording", "robot look", "begin segment", "stop segment", "new segment"],
                "done session": ["finish recording", "cancel recording", "all start"]}


class voice_cmd_demo_recording:
    
    def __init__(self):
        self.loud = True
        #if args.quiet:
        #    self.loud = False
        #print(self.args)
        rospy.on_shutdown(self.cleanup)
        self.speed = 0.2
        self.msg = Segment()
        # publish to cmd_vel, subscribe to speech output
        self.pub_ = rospy.Publisher('segment', Segment)
        rospy.Subscriber('recognizer/output', String, self.speechCb)
        r = rospy.Rate(10.0)
        if self.loud:
            self.soundhandle = SoundClient()
            self.voice = 'voice_don_diphone'
            
        self.current_state = "all start"

        #self.voice = 'voice_kal_diphone'
            #self.soundhandle.say("open gripper", self.voice)
        while not rospy.is_shutdown() and self.current_state != "done session":
        #    self.pub_.publish(self.msg)
            r.sleep()
        
        time.sleep(2.5)
        if self.loud:
            subprocess.call("espeak -v en 'shutting down'", shell=True)
    #self.soundhandle = SoundClient()
    
    
    def speechCb(self, msg):
        rospy.loginfo(msg.data)
        commands = ["begin recording", "check demo", "begin segment", "stop segment", "robot look", "new segment", "cancel recording", "finish recording", "done session"]
        for i, command in enumerate(commands):
            if msg.data.find(command) > -1:
                print command
                if self.current_state not in parent_state[command]:
                    
                    if self.loud:
                        subprocess.call("espeak -v en 'still in state %s'"%(self.current_state), shell=True)
                else:
                    self.current_state = command
                    h = Header()
                    h.stamp = rospy.Time.now()
                    self.msg = Segment(h, command)
                    self.pub_.publish(self.msg)
                    if self.loud:
                        subprocess.call("espeak -v en '%s'"%(command), shell=True)
                        
                break

    def cleanup(self):
        # stop the robot!
        s = Segment()
        self.pub_.publish(s)

if __name__=="__main__":
    rospy.init_node('voice_cmd_demo_recording')
    try:
        voice_cmd_demo_recording()
    except:
        pass
