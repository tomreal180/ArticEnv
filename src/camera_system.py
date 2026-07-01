from math import pi, sin, cos
from direct.task import Task
from panda3d.core import Camera, Vec4, PerspectiveLens
class CameraSystem:
    def __init__(self, taskMgr,camera, config=None):
        self.taskMgr = taskMgr
        self.camera = camera
        self.target = None
        if config is None:
            config = {}
        self.camera_distance = config.get("distance", 20.0)
        self.camera_height = config.get("height", 10.0)
        # self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.camera_position = self.camera.getPos()
        self.cameraView = "main"
        self.taskMgr.add(self.followCameraTask, "FollowCameraTask")
        self.taskMgr.add(self.ListenCameraPosition, "ListenCameraPositionTask")

    def setTarget(self, target):
        """Set the target node for the camera to follow."""
        self.target = target

    def spinCameraTask(self, task):
        """Spin the camera around the origin in a circular path."""
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(self.camera_distance * sin(angleRadians), -self.camera_distance * cos(angleRadians), self.camera_height)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont    
          
    def followCameraTask(self, task):
        if self.target:
            target_pos = self.target.getPos()
            heading = self.target.getH()
            if self.cameraView == "main":
                self.camera.setPos(0, -self.camera_distance-10, self.camera_height+5)
                self.camera.lookAt(target_pos.getX(), target_pos.getY(), target_pos.getZ()+1.5)
            elif self.cameraView == "topdown":
                self.camera.setPos(target_pos.getX(), target_pos.getY(), target_pos.getZ() + self.camera_distance)
                self.camera.setHpr(heading + 180, -90, 0)
            elif self.cameraView == "behind":
                angle_radians = heading * (pi / 180.0)
                # calculate camera position behind the target based on its heading
                cam_x = target_pos.getX() - self.camera_distance * sin(angle_radians)
                cam_y = target_pos.getY() + self.camera_distance * cos(angle_radians)
                self.camera.setPos(cam_x, cam_y, self.camera_height)
                self.camera.lookAt(target_pos.getX(), target_pos.getY(), target_pos.getZ()+1.5)
            elif self.cameraView == "right":
                angle_radians = (heading + 90) * (pi / 180.0)
                cam_x = target_pos.getX() - self.camera_distance * sin(angle_radians)
                cam_y = target_pos.getY() + self.camera_distance * cos(angle_radians)
                self.camera.setPos(cam_x, cam_y, self.camera_height)
                self.camera.lookAt(target_pos.getX(), target_pos.getY(), target_pos.getZ())
            elif self.cameraView == "left":
                angle_radians = (heading - 90) * (pi / 180.0)
                # calculate camera position to the left of the target based on its heading
                cam_x = target_pos.getX() - self.camera_distance * sin(angle_radians)
                cam_y = target_pos.getY() + self.camera_distance * cos(angle_radians)
                self.camera.setPos(cam_x, cam_y, self.camera_height)
                self.camera.lookAt(target_pos.getX(), target_pos.getY(), target_pos.getZ()+1.5)
            else:
                raise Exception(f"Camera {self.cameraView} has no defined behavior in followCameraTask.")
        return task.cont
    
    def setCameraView(self, view_name):
        self.cameraView = view_name
        
    def ListenCameraPosition(self,task):
        """Listen to camera position changes and update the stored cameraPosition variable."""
        self.camera_position = self.camera.getPos()
        return task.cont

    def getCameraPosition(self):
        """Get the current position of the camera."""
        return self.camera_position
    
    def turnCamera(self, angle):
        """Turn the camera around the target by a specified angle (degrees)."""
        if self.target:
            heading = self.target.getH()
            new_heading = heading + angle
            self.target.setH(new_heading)

    def changeCameraHeight(self, delta):
        """Adjust camera height (Z) by delta."""
        self.camera_height = self.camera_height + delta

    def changeCameraDistance(self, delta):
        """Adjust orbit camera distance from the panda."""
        self.camera_distance = max(2.0, self.camera_distance + delta)

    def setPosition(self, pos):
        """Set camera position directly."""
        self.camera.setPos(pos)