from math import pi, sin, cos
from direct.task import Task
from panda3d.core import Camera, Vec4, PerspectiveLens
class CameraSystem:
    def __init__(self,win,render,taskMgr, make_Camera_func, win_aspect, config=None):
        self.win = win
        self.render = render
        self.taskMgr = taskMgr
        self.make_Camera = make_Camera_func
        self.win_aspect = win_aspect
        self.camerasystem = {}
        self.target = None
        if config is None:
            config = {}
        self.cameraDistance = config.get("distance", 20.0)
        self.cameraHeight = config.get("height", 10.0)
        
        # Khởi tạo camera toàn màn hình bằng function create_viewport_camera
        # self.camera = None
        self.split_cameras = ["Cam_TopDown", "Cam_Behind", "Cam_Right", "Cam_Left"]
        self.create_cameras()
        # self.camera.getDisplayRegion(0).setActive(0)  # Kích hoạt DisplayRegion của camera chính
        # Tắt các task cập nhật camera mỗi khung hình để camera cố định
        # self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.zoom = False
        self.taskMgr.add(self.followCameraTask, "FollowCameraTask")

    def setTarget(self, target):
        """Thiết lập mục tiêu để camera đi theo."""
        self.target = target

    def spinCameraTask(self, task):
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

    def create_cameras(self):
        self.create_viewport_camera("Cam_Main", viewport=(0.0, 1.0, 0.0, 1.0))
        # self.camera = self.camerasystem["Cam_Main"]["camera"]
        self.camerasystem["Cam_Main"]["viewport"].setActive(1)
        self.create_viewport_camera("Cam_TopDown", viewport=(0.0, 0.5, 0.5, 1.0))
        self.create_viewport_camera("Cam_Behind", viewport=(0.5, 1.0, 0.5, 1.0))
        self.create_viewport_camera("Cam_Right", viewport=(0.0, 0.5, 0.0, 0.5))
        self.create_viewport_camera("Cam_Left", viewport=(0.5, 1.0, 0.0, 0.5))

    
    def create_viewport_camera(self, cam_name, viewport):
        """Hàm khởi tạo camera và gán vào một khung (DisplayRegion) trên màn hình"""
        
        l, r, b, t = viewport

        dr = self.win.makeDisplayRegion(l, r, b, t)

        # # Xóa nền của vùng này để tránh bị đè hình cũ
        # dr.setClearColorActive(True) 
        # dr.setClearDepthActive(True)
        # Tạo một camera mới và gắn vào khu vực (left, right, bottom, top) của cửa sổ chính
        camNode = Camera(cam_name)

        lens = PerspectiveLens()
        lens.setAspectRatio(self.win_aspect)
        lens.setFov(60)
        camNode.setLens(lens)

        cam_np = self.render.attachNewNode(camNode)
        dr.setCamera(cam_np)
        dr.setActive(0) 
        # cam.setPos(pos)
        # cam.lookAt(self.target.getPos())

        
        # Lưu trữ lại để quản lý
        self.camerasystem[cam_name] = {
            "name": cam_name,
            "camera": cam_np,
            "viewport": dr
        }
    
        
    def followCameraTask(self, task):
        if self.target:
            target_pos = self.target.getPos()
            heading = self.target.getH()
            target_hpr = self.target.getHpr()

            for cam_name in self.split_cameras:
                camera = self.camerasystem.get(cam_name, {}).get("camera")
                if camera:
                    if cam_name == "Cam_TopDown":
                        camera.setPos(target_pos.getX(), target_pos.getY(), target_pos.getZ() + self.cameraDistance)
                        # Nhìn thẳng xuống (Pitch = -90), hướng (Heading) xoay ngược lại gấu (+180) để mông hướng lên trên
                        camera.setHpr(heading + 180, -90, 0)
                    elif cam_name == "Cam_Behind":
                        angle_radians = heading * (pi / 180.0)
                        # Tính toán vị trí camera nằm ở phía trước mặt nhân vật
                        cam_x = target_pos.getX() - self.cameraDistance * sin(angle_radians)
                        cam_y = target_pos.getY() + self.cameraDistance * cos(angle_radians)
                        camera.setPos(cam_x, cam_y, self.cameraHeight)
                        camera.lookAt(target_pos.getX(), target_pos.getY(), target_pos.getZ()+1.5)
                    elif cam_name == "Cam_Right":
                        angle_radians = (heading - 90) * (pi / 180.0)
                        cam_x = target_pos.getX() - self.cameraDistance * sin(angle_radians)
                        cam_y = target_pos.getY() + self.cameraDistance * cos(angle_radians)
                        camera.setPos(cam_x, cam_y, self.cameraHeight)
                        camera.lookAt(target_pos.getX(), target_pos.getY(), target_pos.getZ())
                    elif cam_name == "Cam_Left":
                        angle_radians = (heading + 90) * (pi / 180.0)
                        # Tính toán vị trí camera nằm ở phía trước mặt nhân vật
                        cam_x = target_pos.getX() - self.cameraDistance * sin(angle_radians)
                        cam_y = target_pos.getY() + self.cameraDistance * cos(angle_radians)
                        camera.setPos(cam_x, cam_y, self.cameraHeight)
                        camera.lookAt(target_pos.getX(), target_pos.getY(), target_pos.getZ()+1.5)
                    else:
                        raise Exception(f"Camera {cam_name} chưa được định nghĩa vị trí theo mục tiêu.")

            # Cập nhật vị trí và hướng nhìn cho Cam_Main (độc lập với các camera chia màn hình)
            main_cam = self.camerasystem.get("Cam_Main", {}).get("camera")
            if main_cam:
                main_cam.setPos(0, -self.cameraDistance, self.cameraHeight)
                main_cam.lookAt(target_pos.getX(), target_pos.getY(), target_pos.getZ()+1.5)
        return task.cont
    
    def zoomtoBear(self):
        self.zoom =  not self.zoom
        if self.zoom:
            self.camerasystem["Cam_Main"]["viewport"].setActive(1)
            for cam_name in self.split_cameras:
                self.camerasystem[cam_name]["viewport"].setActive(0)
        else:
            self.camerasystem["Cam_Main"]["viewport"].setActive(0)
            for cam_name in self.split_cameras:
                self.camerasystem[cam_name]["viewport"].setActive(1)
    def turnCamera(self, angle):
        """Xoay camera quanh mục tiêu theo góc (độ)."""
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