class IHA:

    def __init__(self, iha_id=0, pose_x=0, pose_y=0, pose_z=0):
        self.iha_id = iha_id
        self.pose_x = pose_x
        self.pose_y = pose_y
        self.pose_z = pose_z

    def setIhaId(self, iha_id):
        self.iha_id = iha_id

    def getIhaId(self):
        return self.iha_id

    def setPoseX(self, pose_x):
        self.pose_x = pose_x

    def getPoseX(self):
        return self.pose_x

    def setPoseY(self, pose_y):
        self.pose_y = pose_y

    def getPoseY(self):
        return self.pose_y

    def setPoseZ(self, pose_z):
        self.pose_z = pose_z

    def getPoseZ(self):
        return self.pose_z
