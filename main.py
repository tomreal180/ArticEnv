from direct.showbase.ShowBase import ShowBase
import gltf
from direct.actor.Actor import Actor
from panda3d.core import Filename, getModelPath, Point3, LineSegs
import json

# Import custom systems
from src.Polar_bears import PolarBears
from src.enviroment_system import EnvironmentSystem
from src.snow_system import SnowSystem
from src.camera_system import CameraSystem

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Đọc file cấu hình initial values
        with open("config.json", "r") as f:
            self.config = json.load(f)

        # Ensure relative texture URIs from scene.gltf (like textures/...) are resolvable.
        getModelPath().appendDirectory(Filename.from_os_specific("assets/models/snow_mountain"))
        # Thêm thư mục assets vào đường dẫn để tìm model và texture
        # getModelPath().appendDirectory(Filename.from_os_specific("assets"))

        #Init environment system
        self.environment_system = EnvironmentSystem(self.loader, self.render, self.config.get("scene"))
        self.blizzard_effect = True
        #Change background color to match fog color
        self.setBackgroundColor(self.environment_system.fog_color)
        # Controls for scene scale (keyboard: 'y' increases, 'x' decreases)
        self.accept('z', self.environment_system.changeSceneScale, [1.5])
        self.accept('x', self.environment_system.changeSceneScale, [1.0 / 1.5])
        self.accept('s', self.environment_system.updateFogDensity, [0.005])  # Tăng độ đặc của sương
        self.accept('a', self.environment_system.updateFogDensity, [-0.005]) #
        self.accept('d', self.toggleBlizzardEffect)  # Bật/tắt hiệu ứng bão tuyết


        #Init camera system
        # self.camNode.setActive(0)
        self.camera_system = CameraSystem(self.taskMgr,self.camera, self.config.get("camera"))
        #Controls for camera height (keyboard: 'z' decreases, 'u' increases)
        self.accept('y', self.camera_system.changeCameraHeight, [-0.25])
        self.accept('u', self.camera_system.changeCameraHeight, [0.25])
        #Controls for camera distance (keyboard: 'i' decreases, 'o' increases)
        self.accept('i', self.camera_system.changeCameraDistance, [-2.0])
        self.accept('o', self.camera_system.changeCameraDistance, [2.0])
        self.accept('t', self.camera_system.zoomtoBear)

        #Init snow system
        self.snow_system = SnowSystem(self.loader, self.render, self.taskMgr, globalClock, self.config.get("snow_system"))

        self.accept('k', self.snow_system.updatenumFlakes, [500])
        self.accept('j', self.snow_system.updatenumFlakes, [-500])
        self.accept('l', self.updateSnowPosition)
        #Init polar bear actor
        self.polar_bear = PolarBears(self.render, self.config.get("actor"))
        # allow fine adjustments at runtime: 'b' lower, 'n' raise
        self.accept('v', self.polar_bear.changePandaHeight, [-0.05])
        self.accept('b', self.polar_bear.changePandaHeight, [0.05])
        self.accept('n', self.polar_bear.changePandaScale, [1.5])
        self.accept('m', self.polar_bear.changePandaScale, [1.0 / 1.5])

        
        # Nút E để bật/tắt lưới
        self.accept('e', self.polar_bear.toggle_outline)

        # Nút W để bật/tắt khung YOLO 2D
        self.accept('w', self.toggle_yolo_bbox)
        self.is_yolo_bbox_visible = False
        self.taskMgr.add(self.draw_yolo_bounding_box, "draw_yolo_bbox_task")

        # Set camera to follow the polar bear
        self.camera_system.setTarget(self.polar_bear)

        # Cài đặt phím mũi tên để di chuyển nhân vật
        self.accept('arrow_up', self.polar_bear.moveForward, [0.5])
        self.accept('arrow_down', self.polar_bear.moveForward, [-0.5])
        self.accept('arrow_left', self.polar_bear.turn, [10.0])
        self.accept('arrow_right', self.polar_bear.turn, [-10.0])

        # Hỗ trợ đè phím (nhấn giữ mũi tên sẽ liên tục di chuyển)
        self.accept('arrow_up-repeat', self.polar_bear.moveForward, [-0.5])
        self.accept('arrow_down-repeat', self.polar_bear.moveForward, [0.5])
        self.accept('arrow_left-repeat', self.polar_bear.turn, [10.0])
        self.accept('arrow_right-repeat', self.polar_bear.turn, [-10.0])


        self.accept('p', self.printValue)


    
        
    def printValue(self):
        """Print current values of camera settings, panda position/rotation/scale, and scene scale for debugging."""
        print("Camera Height:", self.camera_system.cameraHeight)
        print("Camera Distance:", self.camera_system.cameraDistance)
        print("Panda Position:", self.polar_bear.getPos())
        print("Panda Rotation:", self.polar_bear.getHpr())
        print("Panda Scale:", self.polar_bear.getScale())
        print("Scene Scale:", self.environment_system.scene.getScale())


  
    def updateSnowPosition(self):
        self.snow_system.updateSnowPosition(self.camera_system.getCameraPosition())

    def toggleBlizzardEffect(self):
        if self.blizzard_effect:
            self.environment_system.setupSunnySummerEffect()
            self.snow_system.setnumFlakes(0)  # Tắt tuyết khi chuyển sang hiệu ứng ngày hè
        else:
            self.environment_system.setupBlizzardEffect()
            self.snow_system.setnumFlakes(self.config.get("snow_system", {}).get("num_flakes", 1000))
        self.setBackgroundColor(self.environment_system.fog_color)
        self.blizzard_effect = not self.blizzard_effect

    def toggle_yolo_bbox(self):
        """Toggle the visibility of the YOLO bounding box overlay on the screen."""
        self.is_yolo_bbox_visible = not getattr(self, 'is_yolo_bbox_visible', False)
        if self.is_yolo_bbox_visible:
            print("Activated YOLO 2D bounding box overlay.")
        else:
            print("Deactivated YOLO 2D bounding box overlay.")
            if hasattr(self, 'yolo_bbox_node') and not self.yolo_bbox_node.isEmpty():
                self.yolo_bbox_node.removeNode()

    def draw_yolo_bounding_box(self, task):
        # Remove the old bounding box
        if hasattr(self, 'yolo_bbox_node') and not self.yolo_bbox_node.isEmpty():
            self.yolo_bbox_node.removeNode()

        if not getattr(self, 'is_yolo_bbox_visible', False):
            return task.cont

        bounds = self.polar_bear.getTightBounds()
        if not bounds:
            return task.cont
            
        min_pt, max_pt = bounds
        
        # Get the 8 corners of the bounding box in 3D space
        corners = [
            Point3(min_pt[0], min_pt[1], min_pt[2]),
            Point3(max_pt[0], min_pt[1], min_pt[2]),
            Point3(min_pt[0], max_pt[1], min_pt[2]),
            Point3(max_pt[0], max_pt[1], min_pt[2]),
            Point3(min_pt[0], min_pt[1], max_pt[2]),
            Point3(max_pt[0], min_pt[1], max_pt[2]),
            Point3(min_pt[0], max_pt[1], max_pt[2]),
            Point3(max_pt[0], max_pt[1], max_pt[2])
        ]

        # get main camera to project 3D points to 2D screen space
        cam = self.cam
        if not cam:
            return task.cont
            
        lens = cam.node().getLens()
        
        min_x, max_x = float('inf'), float('-inf')
        min_y, max_y = float('inf'), float('-inf')
        
        # project 8 corners of the 3D bounding box to 2D screen space
        for corner in corners:
            p3d = Point3()
            # project() returns True if the point is in front of the camera, converting camera coordinates to 2D screen coordinates
            if lens.project(cam.getRelativePoint(self.render, corner), p3d):
                min_x = min(min_x, p3d[0])
                max_x = max(max_x, p3d[0])
                min_y = min(min_y, p3d[1])
                max_y = max(max_y, p3d[1])

        # If no points are on the screen, skip
        if min_x == float('inf'):
            return task.cont

        # Limit the bounding box to the screen bounds (-1 to 1 in both x and y)
        min_x, max_x = max(-1, min_x), min(1, max_x)
        min_y, max_y = max(-1, min_y), min(1, max_y)

        # Calculate YOLO coordinates (Coordinate system: x,y center of the box and w,h in [0,1], origin at top-left corner)
        yolo_x_center = ((min_x + max_x) / 2.0 + 1.0) / 2.0
        yolo_y_center = 1.0 - (((min_y + max_y) / 2.0 + 1.0) / 2.0)
        yolo_width = (max_x - min_x) / 2.0
        yolo_height = (max_y - min_y) / 2.0
        
        # Uncomment dòng dưới nếu muốn in nhãn liên tục ra Console hoặc ghi file
        # print(f"0 {yolo_x_center:.6f} {yolo_y_center:.6f} {yolo_width:.6f} {yolo_height:.6f}")

        # Draw the 2D rectangle on the screen (attached to render2d)
        lines = LineSegs()
        lines.setColor(0, 1, 0, 1) # Green border
        lines.setThickness(2)
        
        lines.moveTo(min_x, 0, min_y)
        lines.drawTo(max_x, 0, min_y)
        lines.drawTo(max_x, 0, max_y)
        lines.drawTo(min_x, 0, max_y)
        lines.drawTo(min_x, 0, min_y)
        
        self.yolo_bbox_node = self.render2d.attachNewNode(lines.create())
        
        return task.cont

app = MyApp()
app.run()