from math import pi, sin, cos
from direct.task import Task
class CameraSystem:
    def __init__(self,camera,taskMgr, config=None):
        self.taskMgr = taskMgr
        self.camera = camera
        self.target = None
        if config is None:
            config = {}
        self.cameraDistance = config.get("distance", 20.0)
        self.cameraHeight = config.get("height", 10.0)
        
        self.taskMgr.add(self.followCameraTask, "FollowCameraTask")
        # self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    def setTarget(self, target):
        """Thiết lập mục tiêu để camera đi theo."""
        self.target = target

    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(self.cameraDistance * sin(angleRadians), -self.cameraDistance * cos(angleRadians), self.cameraHeight)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont
    
        
    def followCameraTask(self, task):
        if self.target:
            target_pos = self.target.getPos()
            heading = self.target.getH()
            angle_radians = heading * (pi / 180.0)
            
            # Tính toán vị trí camera luôn nằm ở phía sau lưng nhân vật
            cam_x = target_pos.getX() - self.cameraDistance * sin(angle_radians)
            cam_y = target_pos.getY() - self.cameraDistance * cos(angle_radians)
            
            self.camera.setPos(cam_x, cam_y, self.cameraHeight)
            # Camera luôn hướng về phía gấu (cộng thêm 1.5 Z để nhìn vào thân thay vì dưới chân)
            self.camera.lookAt(target_pos.getX(), target_pos.getY(), target_pos.getZ() + 1.5)
        return task.cont
    
    def changeCameraHeight(self, delta):
        """Adjust camera height (Z) by delta."""
        self.cameraHeight = self.cameraHeight + delta

    def changeCameraDistance(self, delta):
        """Adjust orbit camera distance from the panda."""
        self.cameraDistance = max(2.0, self.cameraDistance + delta)
    def setPosition(self, pos):
        """Set camera position directly."""
        self.camera.setPos(pos)