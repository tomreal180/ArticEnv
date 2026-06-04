from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight, Vec4, Vec3
from panda3d.core import CardMaker, Fog, NodePath
import random
from direct.actor.Actor import Actor

class BlizzardEnvironment(ShowBase):
    def __init__(self):
        super().__init__()

        # 1. SETUP MÀU SẮC BÃO TUYẾT (Trắng xám lạnh)
        blizzard_color = Vec4(0.8, 0.85, 0.9, 1.0)
        self.setBackgroundColor(blizzard_color)

        # 2. SƯƠNG MÙ DÀY ĐẶC (Exponential Fog)
        storm_fog = Fog("Blizzard Fog")
        storm_fog.setColor(blizzard_color)
        # Tăng thông số này sương sẽ đặc hơn (Ví dụ: 0.05 là không thấy gì luôn)
        storm_fog.setExpDensity(0.025) 
        self.render.setFog(storm_fog)

        # 3. ÁNH SÁNG BẸT (Triệt tiêu bóng đổ)
        alight = AmbientLight('alight')
        alight.setColor(Vec4(0.8, 0.85, 0.9, 1)) # Cường độ cao
        self.render.setLight(self.render.attachNewNode(alight))

        dlight = DirectionalLight('dlight')
        dlight.setColor(Vec4(0.1, 0.1, 0.1, 1)) # Cường độ cực thấp, gần như không có
        self.render.setLight(self.render.attachNewNode(dlight))

        # 4. MẶT ĐẤT TUYẾT
        cm = CardMaker('snow_ground')
        cm.setFrame(-100, 100, -100, 100)
        self.ground = self.render.attachNewNode(cm.generate())
        self.ground.setHpr(0, -90, 0)
        self.ground.setColor(Vec4(0.85, 0.9, 0.95, 1))

        # 5. HỆ THỐNG HẠT TUYẾT TỰ CODE (Procedural Snow)
        self.snow_particles = []
        self.num_flakes = 1000  # Số lượng hạt tuyết
        self.wind_vector = Vec3(20, -5, -15) # Hướng gió: thổi mạnh sang ngang (x) và rơi xuống (z)

        self.create_snow()
        # Đưa hàm cập nhật tuyết vào vòng lặp thời gian thực của Panda3D
        self.taskMgr.add(self.update_snow, "update_snow_task")

        # Camera quan sát
        self.cam.setPos(0, -30, 5)
        self.cam.lookAt(0, 0, 2)

        self.pandaActor = Actor("blinding_blizzard.glb",
                                {"walk": "blinding_blizzard.glb",})
        # Loop its animation.
        self.pandaActor.reparentTo(self.render)
        # lower panda slightly so it sits closer to the ground
        # adjust this value as needed
        self.pandaActor.loop("walk")

    def create_snow(self):
        """Tạo ra hàng ngàn hạt tuyết (dưới dạng các mặt phẳng nhỏ) ngẫu nhiên trong không gian"""
        flake_cm = CardMaker('flake')
        flake_cm.setFrame(-0.1, 0.1, -0.1, 0.1) # Kích thước 1 hạt tuyết
        
        self.snow_root = self.render.attachNewNode("snow_root")
        
        for _ in range(self.num_flakes):
            flake = self.snow_root.attachNewNode(flake_cm.generate())
            # Rải đều tuyết trong một hộp không gian (Bounding Box) quanh camera
            x = random.uniform(-40, 40)
            y = random.uniform(-40, 40)
            z = random.uniform(0, 30)
            flake.setPos(x, y, z)
            # Cho hạt tuyết luôn quay mặt về phía camera để tránh bị dẹt
            flake.setBillboardPointEye() 
            flake.setColor(Vec4(1, 1, 1, 0.8)) # Màu trắng hơi trong suốt
            self.snow_particles.append(flake)

    def update_snow(self, task):
        """Hàm này chạy liên tục mỗi khung hình (Frame) để đẩy hạt tuyết theo chiều gió"""
        dt = globalClock.getDt() # Thời gian trôi qua giữa 2 frame
        movement = self.wind_vector * dt
        
        for flake in self.snow_particles:
            new_pos = flake.getPos() + movement
            
            # Khái niệm Wrapping: Nếu hạt tuyết bay ra khỏi vùng quan sát, 
            # hãy đưa nó quay lại đầu nguồn gió để tạo cảm giác bão tuyết vô tận
            if new_pos.getZ() < 0:
                new_pos.setZ(30)
            if new_pos.getX() > 40:
                new_pos.setX(-40)
            if new_pos.getY() < -40:
                new_pos.setY(40)
                
            flake.setPos(new_pos)
            
        return task.cont # Báo cho Panda3D biết tiếp tục chạy hàm này ở frame sau

app = BlizzardEnvironment()
app.run()