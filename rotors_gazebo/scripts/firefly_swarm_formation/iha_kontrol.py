import threading
import time

import rospy
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose
import sys

from std_msgs.msg import String

import formation_calculator

import bipartite_matching

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

        self.ayriklikVerileriniGuncelle()

        self.rastgele_formasyon_envanter_konumlar = []

        self.referans_noktasi = [0, 0]

        self.bitirme_thread = False

        self.suru_ayriklik = False
        self.ayrik_aktif_ihalar = []
        self.referans_noktasi_ayriklik = [-1, -1]
        self.ayrik_aktif_iha_idler = None

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

    def ayriklikVerileriniGuncelle(self):

        if self.killed:
            self.killIha()
            return

        topic_name = "/ayriklik"
        rospy.Subscriber(topic_name, String, self.callbackSuruAyriklik)

    def callbackSuruAyriklik(self, data):

        veriler = str(data).split()
        ayriklik = veriler[1]
        ayriklik = ayriklik[1:]
        ayriklik = ayriklik[:-1]

        if ayriklik == 'separate_two_swarm':
            self.suru_ayriklik = True
            return
        if ayriklik == 'join_two_swarm':
            self.suru_ayriklik = False
            self.referans_noktasi_ayriklik = [-1, -1]
            self.ayrik_aktif_ihalar = []
            self.setReferansNoktasi()
            return

    """
   -------------------------------------------------------------------------------------------------------
   -------------------------------------------------------------------------------------------------------
   BU KISIMDA IHA, /GOREV TOPIC'INI DINLEYEREK GOREVLERI GERCEKLESTIRIR 
   """

    def gorevVerileriniGuncelle(self):

        if self.killed:
            self.killIha()
            return

        topic_name = "/gorev"
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

        if self.suru_ayriklik:
            if self.referans_noktasi_ayriklik[0] == -1:
                self.referans_noktasi_ayriklik[0] = self.referans_noktasi[0]
                self.referans_noktasi_ayriklik[1] = self.referans_noktasi[1]
                s1 = []
                s2 = []
                for i in range(0, len(self.aktif_ihalar)):
                    if self.aktif_ihalar[i].pose_x < self.referans_noktasi_ayriklik[0]:
                        s1.append(self.aktif_ihalar[i])
                    else:
                        s2.append(self.aktif_ihalar[i])
                fark = abs(len(s1) - len(s2))
                if fark > 0:
                    if len(s1) > len(s2):
                        p = len(s1)
                        for i in range(0, int(fark / 2)):
                            s2.append(s1[p - 1])
                            p -= 1
                            s1.pop(len(s1) - 1)
                    elif len(s1) < len(s2):
                        p = len(s2)
                        for i in range(0, int(fark / 2)):
                            s1.append(s2[p - 1])
                            p -= 1
                            s2.pop(len(s2) - 1)

                varmi = 0
                for i in range(0, len(s1)):
                    if s1[i].uav_id == self.uav_id:
                        varmi = 1
                for i in range(0, len(s2)):
                    if s2[i].uav_id == self.uav_id:
                        varmi = 2

                s3 = []
                if varmi == 1:
                    s3 = s1
                    self.referans_noktasi_ayriklik[0] = self.referans_noktasi_ayriklik[0] - 5
                elif varmi == 2:
                    s3 = s2
                    self.referans_noktasi_ayriklik[0] = self.referans_noktasi_ayriklik[0] + 5

                aktif_id_idler = []
                for i in range(0, len(s3)):
                    aktif_id_idler.append(s3[i].uav_id)

                self.ayrik_aktif_iha_idler = aktif_id_idler

                self.ayrik_aktif_ihalar = []
                for i in range(0, len(self.aktif_ihalar)):
                    if self.aktif_ihalar[i].iha_id in self.ayrik_aktif_iha_idler:
                        self.ayrik_aktif_ihalar.append(self.aktif_ihalar[i])

        formasyon_hedef_koordinatlar = []

        if self.gorev[0] == 'square_formation':
            if self.suru_ayriklik:
                self.referans_noktasi = self.referans_noktasi_ayriklik
                formasyon_hedef_koordinatlar = formation_calculator.square_formation_target_positions(self.referans_noktasi,
                                                                                            len(self.ayrik_aktif_iha_idler),
                                                                                            int(self.gorev[1]))
            else:
                formasyon_hedef_koordinatlar = formation_calculator.square_formation_target_positions(self.referans_noktasi,
                                                                                            len(self.aktif_iha_idler),
                                                                                            int(self.gorev[1]))
            # self.guncelleMyPose()
            # self.iha_hareket.setTargetPoseX(6)
            # self.iha_hareket.setTargetPoseY(8)
            # self.iha_hareket.setTargetPoseZ(2)
            # self.iha_hareket.hedefKonumaGit()
            # return
        elif self.gorev[0] == 'triangle_formation':
            if self.suru_ayriklik:
                self.referans_noktasi = self.referans_noktasi_ayriklik
                formasyon_hedef_koordinatlar = formation_calculator.triangle_formation_target_positions(self.referans_noktasi,
                                                                                             len(self.ayrik_aktif_iha_idler),
                                                                                             int(self.gorev[1]))
            else:
                formasyon_hedef_koordinatlar = formation_calculator.triangle_formation_target_positions(self.referans_noktasi,
                                                                                             len(self.aktif_iha_idler),
                                                                                             int(self.gorev[1]))
        elif self.gorev[0] == 'pentagon_formation':
            if self.suru_ayriklik:
                self.referans_noktasi = self.referans_noktasi_ayriklik
                formasyon_hedef_koordinatlar = formation_calculator.pentagon_formation_target_positions(self.referans_noktasi,
                                                                                              len(self.ayrik_aktif_iha_idler),
                                                                                              int(self.gorev[1]))
            else:
                formasyon_hedef_koordinatlar = formation_calculator.pentagon_formation_target_positions(self.referans_noktasi,
                                                                                              len(self.aktif_iha_idler),
                                                                                              int(self.gorev[1]))
        elif self.gorev[0] == 'v_formation':
            if self.suru_ayriklik:
                self.referans_noktasi = self.referans_noktasi_ayriklik
                formasyon_hedef_koordinatlar = formation_calculator.v_formation_target_positions(self.referans_noktasi,
                                                                                          len(self.ayrik_aktif_iha_idler),
                                                                                          int(self.gorev[1]),
                                                                                          int(self.gorev[2]))
            else:
                formasyon_hedef_koordinatlar = formation_calculator.v_formation_target_positions(self.referans_noktasi,
                                                                                          len(self.aktif_iha_idler),
                                                                                          int(self.gorev[1]),
                                                                                          int(self.gorev[2]))
        elif self.gorev[0] == 'crescent_formation':
            if self.suru_ayriklik:
                self.referans_noktasi = self.referans_noktasi_ayriklik
                formasyon_hedef_koordinatlar = formation_calculator.crescent_formation_target_positions(self.referans_noktasi,
                                                                                             len(self.ayrik_aktif_iha_idler),
                                                                                             int(self.gorev[1]))
            else:
                formasyon_hedef_koordinatlar = formation_calculator.crescent_formation_target_positions(self.referans_noktasi,
                                                                                             len(self.aktif_iha_idler),
                                                                                             int(self.gorev[1]))
        elif self.gorev[0] == 'star_formation':
            if self.suru_ayriklik:
                self.referans_noktasi = self.referans_noktasi_ayriklik
                formasyon_hedef_koordinatlar = formation_calculator.star_formation_target_positions(self.referans_noktasi,
                                                                                              len(
                                                                                                  self.ayrik_aktif_iha_idler),
                                                                                              int(self.gorev[1]))
            else:
                formasyon_hedef_koordinatlar = formation_calculator.star_formation_target_positions(self.referans_noktasi,
                                                                                              len(self.aktif_iha_idler),
                                                                                              int(self.gorev[1]))
        elif self.gorev[0] == 'circle_formation':
            if self.suru_ayriklik:
                self.referans_noktasi = self.referans_noktasi_ayriklik
                formasyon_hedef_koordinatlar = formation_calculator.circle_formation_target_positions(self.referans_noktasi,
                                                                                              len(
                                                                                                  self.ayrik_aktif_iha_idler),
                                                                                              int(self.gorev[1]))
            else:
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

        if not self.suru_ayriklik:
            eslestirilmis_iha_hedef = bipartite_matching.bipartite_matching_result(self.aktif_ihalar, my_arr)
        else:
            eslestirilmis_iha_hedef = bipartite_matching.bipartite_matching_result(self.ayrik_aktif_ihalar, my_arr)

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