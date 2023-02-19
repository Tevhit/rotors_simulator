import rospy

from konum_eslestirme import KonumEslestirme
from iha_kontrol import UAV
from iha import IHA

from geometry_msgs.msg import Twist
from geometry_msgs.msg import Transform

from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose
from std_msgs.msg import String

import threading


class SimulationManager:

    def __init__(self, total_uav_count):
        rospy.init_node('SimulationManager', anonymous=True)

        self.armed_uav_ids = []

        self.total_uav_count = total_uav_count

        self.mission_altitude = 0
        self.mission_name = ""
        self.mission_params = ""
        self.publish_mission_thread = None
        self.publish_mission_thread = threading.Thread(target=self.mission_publisher,)
        self.publish_mission_thread.start()

    def arm_uav(self, uav_ids):
        for i in range(0, len(uav_ids)):
            self.armed_uav_ids.append(uav_ids[i])
            my_thread = UAV(uav_ids[i], self.armed_uav_ids)
            my_thread.start()

        print("armed_uav_ids : " + str(uav_ids))

    def disarm_uav(self, iha_id):
        index = self.armed_uav_ids.index(iha_id)
        self.threads[index].killed = True
        self.threads.pop(index)
        self.armed_uav_ids.pop(index)

    def set_mission_altitude(self, mission_altitude):
        self.mission_altitude = mission_altitude

    def publish_mission(self, mission_name, mission_params=''):
        self.mission_name = mission_name
        self.mission_params = mission_params

    def mission_publisher(self):
        pub = rospy.Publisher('mission', String, queue_size=10)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            pub.publish(self.mission_name + ' ' + self.mission_params + ' ' + str(self.mission_altitude))
            rate.sleep()

        self.publish_mission_thread.join()
