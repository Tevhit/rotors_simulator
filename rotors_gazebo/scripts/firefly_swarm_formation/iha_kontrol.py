import threading
import time

import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose
import sys

from std_msgs.msg import String

import formation_calculator

from konum_eslestirme import KonumEslestirme

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose


class UAV(threading.Thread):
    def __init__(self, uav_id, aktif_iha_idler):
        threading.Thread.__init__(self)

        self.uav_id = uav_id

        self.my_pose_x = 0
        self.my_pose_y = 0
        self.my_pose_z = 0

        self.aktif_ihalar = []
        self.aktif_iha_idler = aktif_iha_idler
        self.aktif_iha_sayisi = len(self.aktif_iha_idler)

        self.killed = False

        self.gorevVerileriniGuncelle()
        self.gorev = None
        self.irtifa = 0

        self.konum_eslestirme = KonumEslestirme()

        self.rastgele_formasyon_envanter_konumlar = []

        self.referans_noktasi = [0, 0]

        self.bitirme_thread = False

    # Rastgele formasyon konumlarini envanterde saklamak icin
    def setRastgeleFormasyonEnvanterKonumlar(self, rastgele_formasyon_envanter_konumlar):
        self.rastgele_formasyon_envanter_konumlar = rastgele_formasyon_envanter_konumlar

    def setAktifIhalar(self, aktif_ihalar):
        self.aktif_ihalar = aktif_ihalar

    def set_aktif_iha_idler(self, aktif_iha_idler):
        self.aktif_iha_idler = aktif_iha_idler
        self.aktif_iha_sayisi = len(self.aktif_iha_idler)

    # Suruden cikarilan IHA'nin thread'ini durdurmak icin
    def killIha(self):
        if self.bitirme_thread == False:
            self.irtifaAyarla(0)

    def guncelleMyPose(self):
        for i in range(0, len(self.aktif_iha_idler)):
            if self.aktif_ihalar[i].iha_id == self.uav_id:

                konum = [0, 0, 0]
                konum[0] = self.aktif_ihalar[i].pose_x
                konum[1] = self.aktif_ihalar[i].pose_y
                konum[2] = self.aktif_ihalar[i].pose_z

                if 0.01 > konum[0] > -0.01:
                    konum[0] = 0
                if 0.01 > konum[1] > -0.01:
                    konum[1] = 0
                if 0.01 > konum[2] > -0.01:
                    konum[2] = 0

                self.my_pose_x = konum[0]
                self.my_pose_y = konum[1]
                self.my_pose_z = konum[2]

        # self.iha_hareket.setPoseX(self.my_pose_x)
        # self.iha_hareket.setPoseY(self.my_pose_y)
        # self.iha_hareket.setPoseZ(self.my_pose_z)


    """
   -------------------------------------------------------------------------------------------------------
   -------------------------------------------------------------------------------------------------------
   BU KISIMDA IHA, /GOREV TOPIC'INI DINLEYEREK GOREVLERI GERCEKLESTIRIR 
   """

    def gorevVerileriniGuncelle(self):

        if self.killed:
            self.killIha()
            return

        topic_name = "/mission"
        rospy.Subscriber(topic_name, String, self.callbackGorevVerileri)

    def callbackGorevVerileri(self, data):

        veriler = str(data).split()
        gorev = veriler[1]
        gorev = gorev[1:]

        yeni_gorev = []
        yeni_gorev.append(gorev)
        for i in range(2, len(veriler) - 1):
            yeni_gorev.append(veriler[i])

        self.irtifa = int(veriler[len(veriler) - 1][:-1])

        if self.gorev is None or len(self.gorev) != len(yeni_gorev):
            self.gorev = yeni_gorev
            self.setReferansNoktasi()
            return

        for i in range(0, len(yeni_gorev)):
            if self.gorev[i] != yeni_gorev[i]:
                self.gorev = yeni_gorev
                self.setReferansNoktasi()
                return

        # self.guncelleMyPose()

        self.goreviTakipEt()

    def goreviTakipEt(self):

        if self.killed:
            self.killIha()
            return

        formasyon_hedef_koordinatlar = []

        if self.gorev[0] == 'square_formation':
            formasyon_hedef_koordinatlar = formation_calculator.square_formation_target_positions(self.referans_noktasi,
                                                                                                  len(self.aktif_iha_idler),
                                                                                                  int(self.gorev[1]))
        elif self.gorev[0] == 'triangle_formation':
            formasyon_hedef_koordinatlar = formation_calculator.triangle_formation_target_positions(
                self.referans_noktasi,
                len(self.aktif_iha_idler),
                int(self.gorev[1]))
        elif self.gorev[0] == 'pentagon_formation':
            formasyon_hedef_koordinatlar = formation_calculator.pentagon_formation_target_positions(
                self.referans_noktasi,
                len(self.aktif_iha_idler),
                int(self.gorev[1]))
        elif self.gorev[0] == 'v_formation':
            formasyon_hedef_koordinatlar = formation_calculator.v_formation_target_positions(self.referans_noktasi,
                                                                                             len(self.aktif_iha_idler),
                                                                                             int(self.gorev[1]),
                                                                                             int(self.gorev[2]))
        elif self.gorev[0] == 'crescent_formation':
            formasyon_hedef_koordinatlar = formation_calculator.crescent_formation_target_positions(
                self.referans_noktasi,
                len(self.aktif_iha_idler),
                int(self.gorev[1]))
        elif self.gorev[0] == 'star_formation':
            formasyon_hedef_koordinatlar = formation_calculator.star_formation_target_positions(self.referans_noktasi,
                                                                                                len(self.aktif_iha_idler),
                                                                                                int(self.gorev[1]))
        elif self.gorev[0] == 'circle_formation':
            formasyon_hedef_koordinatlar = formation_calculator.circle_formation_target_positions(self.referans_noktasi,
                                                                                                  len(self.aktif_iha_idler),
                                                                                                  int(self.gorev[1]))
        elif self.gorev[0] == 'saved_formation':
            formasyon_hedef_koordinatlar = self.rastgele_formasyon_envanter_konumlar
        elif self.gorev[0] == 'sequential_landing':
            self.otomatikSiraliInisYap(int(self.gorev[1]))
            return
        elif self.gorev[0] == 'set_altitude':
            self.irtifaAyarla(int(self.gorev[1]))
            self.irtifa = int(self.gorev[1])
            return

        my_arr = []
        for i in range(0, len(formasyon_hedef_koordinatlar)):
            my_arr.append([[str(i)], formasyon_hedef_koordinatlar[i]])

        eslestirilmis_iha_hedef = self.konum_eslestirme.getBipartiteMatchingResult(self.aktif_ihalar, my_arr)

        a = 0
        for key in eslestirilmis_iha_hedef.keys():
            if key is self.uav_id:
                break
            a += 1
        hedef_key = [*eslestirilmis_iha_hedef.values()][a]

        hedef_konum = formasyon_hedef_koordinatlar[int(hedef_key)]

        pub_topic = '/firefly' + str(self.uav_id) + '/command/pose'
        pub = rospy.Publisher(pub_topic, PoseStamped, queue_size=10)

        ps = PoseStamped()

        ps.header.seq = 1
        ps.header.stamp = rospy.Time.now()
        ps.header.frame_id = "map"

        if self.killed:
            if my_pose_z < 0.5:
                self.bitirme_thread = True

        ps.pose.position.x = hedef_konum[0]
        ps.pose.position.y = hedef_konum[1]
        ps.pose.position.z = self.irtifa

        ps.pose.orientation.x = 0.0
        ps.pose.orientation.y = 0.0
        ps.pose.orientation.z = 0.0
        ps.pose.orientation.w = 0.0

        pub.publish(ps)

    """
   -------------------------------------------------------------------------------------------------------
   -------------------------------------------------------------------------------------------------------
   """

    """
   -------------------------------------------------------------------------------------------------------
   -------------------------------------------------------------------------------------------------------
   BU KISIMDA SADECE IRTIFA AYARLAMA ISLEMINI YAPAR
   """

    def irtifaAyarla(self, irtifa=0):
        self.irtifa = 0

        my_pose_x = 0
        my_pose_y = 0
        my_pose_z = 0
        for i in range(0, len(self.aktif_ihalar)):
            if self.aktif_ihalar[i].iha_id == self.uav_id:
                my_pose_x = self.aktif_ihalar[i].pose_x
                my_pose_y = self.aktif_ihalar[i].pose_y
                my_pose_z = self.aktif_ihalar[i].pose_z

        pub_topic = '/firefly' + str(self.uav_id) + '/command/pose'
        pub = rospy.Publisher(pub_topic, PoseStamped, queue_size=10)

        ps = PoseStamped()

        ps.header.seq = 1
        ps.header.stamp = rospy.Time.now()
        ps.header.frame_id = "map"

        if self.killed:
            if my_pose_z < 0.5:
                self.bitirme_thread = True

        ps.pose.position.x = my_pose_x
        ps.pose.position.y = my_pose_y
        ps.pose.position.z = irtifa

        ps.pose.orientation.x = 0.0
        ps.pose.orientation.y = 0.0
        ps.pose.orientation.z = 0.0
        ps.pose.orientation.w = 0.0

        pub.publish(ps)

    """
   -------------------------------------------------------------------------------------------------------
   -------------------------------------------------------------------------------------------------------
   """

    """
   -------------------------------------------------------------------------------------------------------
   -------------------------------------------------------------------------------------------------------
   BU KISIMDA FORMASYON ICIN TUM IHA'LARIN ORTA NOKTASINI REFERANS NOKTASI OLARAK ATAR 
   """

    def setReferansNoktasi(self):
        referans_noktasi = [0, 0]
        xToplam = 0
        yToplam = 0

        for i in range(0, self.aktif_iha_sayisi):
            xToplam += self.aktif_ihalar[i].pose_x
            yToplam += self.aktif_ihalar[i].pose_y

        referans_noktasi[0] = int(xToplam / self.aktif_iha_sayisi)
        referans_noktasi[1] = int(yToplam / self.aktif_iha_sayisi)

        self.referans_noktasi = referans_noktasi

    """
   -------------------------------------------------------------------------------------------------------
   -------------------------------------------------------------------------------------------------------
   """

    """
   -------------------------------------------------------------------------------------------------------
   -------------------------------------------------------------------------------------------------------
   BU KISIMDA IHA, KENDI SIRASINI BEKLEYEREK OTOMATIK SIRALI INIS YAPAR 
   """

    def otomatikSiraliInisYap(self, bekleme_suresi):

        bir_onceki_iha_z = 0

        for i in range(0, len(self.aktif_iha_idler)):
            if self.aktif_ihalar[i].iha_id == (self.uav_id - 1):
                bir_onceki_iha_z = self.aktif_ihalar[i].pose_z

                if 0.01 > bir_onceki_iha_z > -0.01:
                    bir_onceki_iha_z = 0

        if bir_onceki_iha_z < 0.1:
            time.sleep(bekleme_suresi)
            self.killed = True

    """
   -------------------------------------------------------------------------------------------------------
   -------------------------------------------------------------------------------------------------------
   """

    # def getAktifIhalar(self):
    #
    #     aktif_ihalar = []
    #     for i in range(0, len(self.tum_ihalar_konumlar)):
    #         if self.tum_ihalar_konumlar[i].iha_id in self.aktif_iha_idler:
    #             aktif_ihalar.append(self.tum_ihalar_konumlar[i])
    #
    #     return aktif_ihalar

    # iha_konum_dinleme = threading.Thread(target=self.tumIHAlarinKonumVerileriniDinle)
    # iha_konum_dinleme.start()


    # def tumIHAlarinKonumVerileriniDinle(self):
    #     for i in range(1, self.total_uav_count + 1):
    #         self.listener(i)
    #     rospy.spin()

    # def listener(self, iha_id):
    #     topic_name = "/firefly" + str(iha_id) + "/odometry_sensor1/pose"
    #     rospy.Subscriber(topic_name, Pose, self.callback, iha_id)
    #
    # def callback(self, data, iha_id):
    #     dizideMevcutIhalar = []
    #     for i in range(0, len(self.tum_ihalar_konumlar)):
    #         dizideMevcutIhalar.append(self.tum_ihalar_konumlar[i].iha_id)
    #
    #     if iha_id in dizideMevcutIhalar:
    #         index = dizideMevcutIhalar.index(iha_id)
    #         self.tum_ihalar_konumlar[index].pose_x = data.position.x
    #         self.tum_ihalar_konumlar[index].pose_y = data.position.y
    #         self.tum_ihalar_konumlar[index].pose_z = data.position.z
    #     else:
    #         iha = IHA(iha_id, data.position.x, data.position.y, data.position.z)
    #         self.tum_ihalar_konumlar.append(iha)
    #
    #     for i in range(0, len(self.threads)):
    #         self.threads[i].setAktifIhalar(self.getAktifIhalar())