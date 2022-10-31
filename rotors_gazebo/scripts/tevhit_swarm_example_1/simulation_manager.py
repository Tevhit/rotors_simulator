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

        self.gorev_yayinlama_reset = False

        self.mission_altitude = 0

        self.rastgele_formasyon_envanter_konumlar = []

    def arm_uav(self, iha_isimleri):

        iha_idleri = []
        for i in range(0, len(iha_isimleri)):
            iha_id = int(iha_isimleri[i].replace('firefly', ''))
            iha_idleri.append(iha_id)
            self.aktif_iha_idler.append(iha_id)

        threads = []
        for i in range(0, len(iha_idleri)):
            my_thread = UAV(iha_idleri[i], self.aktif_iha_idler)
            threads.append(my_thread)
            self.threads.append(my_thread)

        for i in range(0, len(threads)):
            threads[i].start()

        for i in range(0, len(self.threads)):
            self.threads[i].set_aktif_iha_idler(self.aktif_iha_idler)
            self.threads[i].setAktifIhalar(self.getAktifIhalar())
            self.threads[i].setRastgeleFormasyonEnvanterKonumlar(self.rastgele_formasyon_envanter_konumlar)
            self.threads[i].setReferansNoktasi()

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
    """

    def rastgeleFormasyonuEnvantereKaydet(self):

        tum_iha_konumlar = []

        for i in range(0, len(self.tum_ihalar_konumlar)):
            iha_konum = [self.tum_ihalar_konumlar[i].pose_x, self.tum_ihalar_konumlar[i].pose_y]
            tum_iha_konumlar.append(iha_konum)

        for i in range(0, len(self.threads)):
            self.threads[i].setRastgeleFormasyonEnvanterKonumlar(tum_iha_konumlar)

        self.rastgele_formasyon_envanter_konumlar = tum_iha_konumlar


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
    """
    -------------------------------------------------------------------------------------------------------
    -------------------------------------------------------------------------------------------------------
    """

    """
    -------------------------------------------------------------------------------------------------------
    -------------------------------------------------------------------------------------------------------
    BU KISIMDA ARAYUZDEN ALINAN GOREVLER ROS ORTAMINA PUBLISH EDILIR
    """
    def publish_mission(self, gorev_adi, gorev_parametreleri = ''):
        self.setGorevYayinlamaReset()

        self.pub_thread = threading.Thread(target=self.myThreadGorevPub, args=(gorev_adi,gorev_parametreleri,))
        self.pub_thread.start()

    def myThreadGorevPub(self, gorev_adi, gorev_parametreleri):

        self.gorev_yayinlama_reset = False
        pub = rospy.Publisher('gorev', String, queue_size=10)
        rate = rospy.Rate(10)
        while (not rospy.is_shutdown()):
            if self.gorev_yayinlama_reset:
                break
            pub.publish(str(gorev_adi) + ' ' + gorev_parametreleri + ' ' + str(self.mission_altitude))
            rate.sleep()

    def setGorevYayinlamaReset(self):
        self.gorev_yayinlama_reset = True
        try:
            self.pub_thread.join()
        except:
            pass
    """
    -------------------------------------------------------------------------------------------------------
    -------------------------------------------------------------------------------------------------------
    """

    def suruAyriklikYayinla(self, gorev_adi):
        self.setGorevYayinlamaReset()
        gorev_parametreleri = ''
        self.pub_thread = threading.Thread(target=self.myThreadSuruAyriklikPub, args=(gorev_adi,gorev_parametreleri,))
        self.pub_thread.start()

    def myThreadSuruAyriklikPub(self, gorev_adi, gorev_parametreleri):

        self.gorev_yayinlama_reset = False
        pub = rospy.Publisher('ayriklik', String, queue_size=10)
        rate = rospy.Rate(10)
        while (not rospy.is_shutdown()):
            if self.gorev_yayinlama_reset:
                break
            pub.publish(gorev_adi)
            rate.sleep()