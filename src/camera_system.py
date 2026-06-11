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
        self.cameraDistance = config.get("distance", 20.0)
        self.cameraHeight = config.get("height", 10.0)
        # Khởi tạo camera toàn màn hình bằng function create_viewport_camera
        # self.camera = None
        # self.camera.getDisplayRegion(0).setActive(0)  # Kích hoạt DisplayRegion của camera chính
        # Tắt các task cập nhật camera mỗi khung hình để camera cố định
        # self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.cameraPosition = self.camera.getPos()
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
        self.camera.setPos(self.cameraDistance * sin(angleRadians), -self.cameraDistance * cos(angleRadians), self.cameraHeight)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont
    
    # def create_fixed_camera(self, cam_name):
    #     if self.target:
    #         main_cam = self.create_viewport_camera(cam_name, viewport=(0.0, 1.0, 0.0, 1.0))
    #         main_cam.setPos(0, -self.cameraDistance, self.cameraHeight)
    #         main_cam.lookAt(self.target.getPos())
    #         self.camerasystem[cam_name] = main_cam
    
    # def create_viewport_camera(self, cam_name, viewport):
    #     """Function to create a camera and attach it to a viewport (DisplayRegion) on the screen"""
        
    #     l, r, b, t = viewport

    #     dr = self.win.makeDisplayRegion(l, r, b, t)

    #     # # Xóa nền của vùng này để tránh bị đè hình cũ
    #     # dr.setClearColorActive(True) 
    #     # dr.setClearDepthActive(True)
    #     # Tạo một camera mới và gắn vào khu vực (left, right, bottom, top) của cửa sổ chính
    #     camNode = Camera(cam_name)

    #     lens = PerspectiveLens()
    #     lens.setAspectRatio(self.win_aspect)
    #     lens.setFov(60)
    #     camNode.setLens(lens)

    #     cam_np = self.render.attachNewNode(camNode)
    #     dr.setCamera(cam_np)
    #     dr.setActive(0) 
    #     # cam.setPos(pos)
    #     # cam.lookAt(self.target.getPos())

        
    #     # save camera and its viewport in the camerasystem dictionary for later reference
    #     self.camerasystem[cam_name] = {
    #         "name": cam_name,
    #         "camera": cam_np,
    #         "viewport": dr
    #     }
    
        
    def followCameraTask(self, task):
        if self.target:
            target_pos = self.target.getPos()
            heading = self.target.getH()
            if self.cameraView == "main":
                self.camera.setPos(0, -self.cameraDistance-10, self.cameraHeight+5)
                self.camera.lookAt(target_pos.getX(), target_pos.getY(), target_pos.getZ()+1.5)
            elif self.cameraView == "topdown":
                self.camera.setPos(target_pos.getX(), target_pos.getY(), target_pos.getZ() + self.cameraDistance)
                self.camera.setHpr(heading + 180, -90, 0)
            elif self.cameraView == "behind":
                angle_radians = heading * (pi / 180.0)
                # calculate camera position behind the target based on its heading
                cam_x = target_pos.getX() - self.cameraDistance * sin(angle_radians)
                cam_y = target_pos.getY() + self.cameraDistance * cos(angle_radians)
                self.camera.setPos(cam_x, cam_y, self.cameraHeight)
                self.camera.lookAt(target_pos.getX(), target_pos.getY(), target_pos.getZ()+1.5)
            elif self.cameraView == "right":
                angle_radians = (heading + 90) * (pi / 180.0)
                cam_x = target_pos.getX() - self.cameraDistance * sin(angle_radians)
                cam_y = target_pos.getY() + self.cameraDistance * cos(angle_radians)
                self.camera.setPos(cam_x, cam_y, self.cameraHeight)
                self.camera.lookAt(target_pos.getX(), target_pos.getY(), target_pos.getZ())
            elif self.cameraView == "left":
                angle_radians = (heading - 90) * (pi / 180.0)
                # calculate camera position to the left of the target based on its heading
                cam_x = target_pos.getX() - self.cameraDistance * sin(angle_radians)
                cam_y = target_pos.getY() + self.cameraDistance * cos(angle_radians)
                self.camera.setPos(cam_x, cam_y, self.cameraHeight)
                self.camera.lookAt(target_pos.getX(), target_pos.getY(), target_pos.getZ()+1.5)
            else:
                raise Exception(f"Camera {self.cameraView} has no defined behavior in followCameraTask.")
        return task.cont
    def setCameraView(self, view_name):
        self.cameraView = view_name
        
    def ListenCameraPosition(self,task):
        """Listen to camera position changes and update the stored cameraPosition variable."""
        self.cameraPosition = self.camera.getPos()
        return task.cont


    def getCameraPosition(self):
        """Get the current position of the camera."""
        return self.cameraPosition
    
    def turnCamera(self, angle):
        """Turn the camera around the target by a specified angle (degrees)."""
        if self.target:
            heading = self.target.getH()
            new_heading = heading + angle
            self.target.setH(new_heading)

    def changeCameraHeight(self, delta):
        """Adjust camera height (Z) by delta."""
        self.cameraHeight = self.cameraHeight + delta

    def changeCameraDistance(self, delta):
        """Adjust orbit camera distance from the panda."""
        self.cameraDistance = max(2.0, self.cameraDistance + delta)
    def setPosition(self, pos):
        """Set camera position directly."""
        self.camera.setPos(pos)