 #### Modules ####

import os
import sys
import numpy as np

import pandas as pd

import cv2
from cv_bridge import CvBridge
from cv_bridge import CvBridgeError

import pytz
import rosbag
import rospy

import time
import datetime

 #### Where is my data ####

dir = "/home/robotv/data"
# data = "/home/robotv/data/*"
img_out = dir + "/" + "img_output"

class ImageExtractor():

    def __init__(self):
        self.bridge = CvBridge
        cv_img = 0
        filelist = os.listdir(dir)                                               # Bring the directory data from 'dir' and put it into 'filelist'

        for i in filelist:
            if i[-3: ] == 'bag':
                bag_path = os.path.join(dir, i)                                   # If the file is .bag file, append them to the list 'bag_path'
                with rosbag.Bag(bag_path, 'r') as bag:                           # rosbag.Bag(bag_path, 'r') use rosbag module to 'r'(read) from the bag_path
                    for topic, msg, t in bag.read_messages():                    # Check the topic and message info of the bag file.
                        if topic == "camera/aligned_depth_to_color/image_raw":
                            try:
                                cv_img = self.bridge.imgmsg_to_cv2(msg, "passthrough)")
                                depth_array = np.array(cv_img)

                            except CvBridgeError as e:
                                print(e)
                                
                            ## Converting universal time to normal time ##
                            timestr = "%.13f" % msg.header.stamp.to_sec()   
                            ts = pytz.timezone('Asia/Seoul')
                            timefloat = float(timestr)
                            timeint = (int(round(timefloat * 1000)))

                            print(timeint)

                            img_time = pytz.datetime.datetime.fromtimestamp(timeint/(1000), ts)
                            img_name_time = img_time.strftime("%Y-%m-%d_%H-%M-%S-%f")   # Year-Month-Day_Hour-Minute-Second

                            # Data processing
                            data = np.resize(depth_array, (480,640))
                            save_csv = pd.DataFrame(data)
                            img_name = img_name_time + ".png"
                            save_img_paths = os.path.join(img_out, img_name)
                            print(save_img_paths)
                            print(i)
                            depth_array = cv2.cvtColor(depth_array, cv2.COLOR_RGB2BGR)
                            cv2.imwrite(save_img_paths, depth_array * 255)      # Saving images


if __name__ == '__main__':
    try:
        extractor = ImageExtractor()
    except rospy.ROSInterruptException:
        pass