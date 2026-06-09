from direct.showbase.ShowBase import ShowBase
import gltf
from direct.actor.Actor import Actor
from panda3d.core import Filename, getModelPath
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
        #Change background color to match fog color
        self.setBackgroundColor(self.environment_system.fog_color)
        # Controls for scene scale (keyboard: 'y' increases, 'x' decreases)
        self.accept('y', self.environment_system.changeSceneScale, [1.5])
        self.accept('x', self.environment_system.changeSceneScale, [1.0 / 1.5])


        #Init camera system
        self.camNode.setActive(0)
        self.camera_system = CameraSystem(self.win, self.render,self.taskMgr,self.makeCamera, self.getAspectRatio(), self.config.get("camera"))
        #Controls for camera height (keyboard: 'z' decreases, 'u' increases)
        self.accept('z', self.camera_system.changeCameraHeight, [-0.25])
        self.accept('u', self.camera_system.changeCameraHeight, [0.25])
        #Controls for camera distance (keyboard: 'i' decreases, 'o' increases)
        self.accept('i', self.camera_system.changeCameraDistance, [-2.0])
        self.accept('o', self.camera_system.changeCameraDistance, [2.0])
        self.accept('t', self.camera_system.zoomtoBear)

        #Init snow system
        self.snow_system = SnowSystem(self.loader, self.render, self.taskMgr, globalClock, self.config.get("snow_system"))

        self.accept('p', self.printValue)
        #Init polar bear actor
        self.polar_bear = PolarBears(self.render, self.config.get("actor"))
        # allow fine adjustments at runtime: 'b' lower, 'n' raise
        self.accept('b', self.polar_bear.changePandaHeight, [-0.05])
        self.accept('n', self.polar_bear.changePandaHeight, [0.05])
        self.accept('g', self.polar_bear.changePandaScale, [1.5])
        self.accept('h', self.polar_bear.changePandaScale, [1.0 / 1.5])

        
        # Nút E để bật/tắt lưới
        self.accept('e', self.polar_bear.toggle_outline)

        # Gán gấu làm mục tiêu cho camera đi theo
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

    
        
    def printValue(self):
        print("Camera Height:", self.camera_system.cameraHeight)
        print("Camera Distance:", self.camera_system.cameraDistance)
        print("Panda Position:", self.polar_bear.getPos())
        print("Panda Rotation:", self.polar_bear.getHpr())
        print("Panda Scale:", self.polar_bear.getScale())
        print("Scene Scale:", self.environment_system.scene.getScale())
  
app = MyApp()
app.run()