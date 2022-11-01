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

        self.threads = []
        self.aktif_iha_idler = []
        self.tum_ihalar_konumlar = []

        self.total_uav_count = total_uav_count

        iha_konum_dinleme = threading.Thread(target=self.tumIHAlarinKonumVerileriniDinle)
        iha_konum_dinleme.start()

        self.mission_altitude = 0

        self.mission_name = ""
        self.mission_params = ""
        self.publish_mission_thread = None
        self.publish_mission_thread = threading.Thread(target=self.mission_publisher, )
        self.publish_mission_thread.start()

    def arm_uav(self, uav_names):

        iha_idleri = []
        for i in range(0, len(uav_names)):
            iha_id = int(uav_names[i].replace('firefly', ''))
            iha_idleri.append(iha_id)
            self.aktif_iha_idler.append(iha_id)

        for i in range(0, len(iha_idleri)):
            my_thread = UAV(iha_idleri[i], self.aktif_iha_idler)
            my_thread.start()

    def disarm_uav(self, iha_id):

        index = self.aktif_iha_idler.index(iha_id)
        self.threads[index].killed = True

        self.threads.pop(index)

        self.aktif_iha_idler.pop(index)

        for i in range(0, len(self.threads)):
            self.threads[i].set_aktif_iha_idler(self.aktif_iha_idler)
            self.threads[i].setAktifIhalar(self.getAktifIhalar())

    def getAktifIhalar(self):

        aktif_ihalar = []
        for i in range(0, len(self.tum_ihalar_konumlar)):
            if self.tum_ihalar_konumlar[i].iha_id in self.aktif_iha_idler:
                aktif_ihalar.append(self.tum_ihalar_konumlar[i])

        return aktif_ihalar

    """
    -------------------------------------------------------------------------------------------------------
    -------------------------------------------------------------------------------------------------------
    BU KISIMDA BUTUN IHA'LARIN KONUMLARI ANLIK OLARAK DINLENEREK THREAD'LERE ILETILIR
    """

    def tumIHAlarinKonumVerileriniDinle(self):
        for i in range(1, self.total_uav_count + 1):
            self.listener(i)
        rospy.spin()

    def listener(self, iha_id):
        topic_name = "/firefly" + str(iha_id) + "/odometry_sensor1/pose"
        rospy.Subscriber(topic_name, Pose, self.callback, iha_id)

    def callback(self, data, iha_id):
        dizideMevcutIhalar = []
        for i in range(0, len(self.tum_ihalar_konumlar)):
            dizideMevcutIhalar.append(self.tum_ihalar_konumlar[i].iha_id)

        if iha_id in dizideMevcutIhalar:
            index = dizideMevcutIhalar.index(iha_id)
            self.tum_ihalar_konumlar[index].pose_x = data.position.x
            self.tum_ihalar_konumlar[index].pose_y = data.position.y
            self.tum_ihalar_konumlar[index].pose_z = data.position.z
        else:
            iha = IHA(iha_id, data.position.x, data.position.y, data.position.z)
            self.tum_ihalar_konumlar.append(iha)

        for i in range(0, len(self.threads)):
            self.threads[i].setAktifIhalar(self.getAktifIhalar())

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
