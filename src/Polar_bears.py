from direct.interval.IntervalGlobal import Sequence

from direct.actor.Actor import Actor
from panda3d.core import CollisionNode, CollisionRay, CollisionHandlerFloor, BitMask32, Point3
class PolarBears(Actor):
    def __init__(self, render, config=None, cTrav=None):
        self.render = render
        if config is None:
            config = {}
        self.mesh_bear = None
        actor_model = config.get("model_path", "assets/models/polar_bear2.glb")
        super().__init__(actor_model, {"walk": actor_model})
        self.reparentTo(self.render)
        actor_scale = config.get("scale", 1.0)
        self.setScale(actor_scale, actor_scale, actor_scale)
        self.create_mesh_bear()
        # lower panda slightly so it sits closer to the ground
        # adjust this value as needed
        z = config.get("z_pos", 0)
        self.setZ(config.get("z_pos", 0))
        self.setH(70)
        # self.setHpr(0, 0, 0)  
        self.loop("walk")

        # posInterval1 = self.posInterval(30, Point3( 19.768331, -7.1950926, z), startPos=Point3(0, 0, z))
        # posInterval2 = self.posInterval(40, Point3(60.418693, -21.990522, -24.099922), startPos=Point3(19.768331, -7.1950926, -24.099922))
        # posInterval3 = self.posInterval(50, Point3(73.783195, -26.85472, -23.89992), startPos=Point3(60.418693, -21.990522, -23.89992))
        # posInterval4 = self.posInterval(50, Point3(88.12219, -32.0736, -23.54993), startPos=Point3(73.783195, -26.85472, -23.54993))
        # posInterval5 = self.posInterval(50, Point3(108.168945, -39.37017, -23.199935), startPos=Point3(88.12219, -32.0736, -23.199935))
        # posInterval6 = self.posInterval(50, Point3(145.47914, -52.949897, -22.94994), startPos=Point3(108.168945, -39.37017, -22.94994))

        posInterval1 = self.posInterval(50, Point3( 145.47914, -52.949897, z), startPos=Point3(0, 0, z))
        posInterval2 = self.posInterval(50, Point3(0, 0, z), startPos=Point3(145.47914, -52.949897, z))
        hprInterval1 = self.hprInterval(3, Point3(250, 0, 0), startHpr=Point3(70, 0, 0))
        hprInterval2 = self.hprInterval(3, Point3(70, 0, 0), startHpr=Point3(250, 0, 0))

        # posInterval2 = self.posInterval(50, Point3(112.55255, -39.659835, z+2), startPos=Point3(5.0796813, -0.5430069, z))
        # hprInterval1 = self.hprInterval(3, Point3(70, 0, 0), startHpr=Point3(250, 0, 0))
        # hprInterval2 = self.hprInterval(3, Point3(250, 0, 0), startHpr=Point3(70, 0, 0))
        # self.pandaPace = Sequence(posInterval1, hprInterval1, posInterval2, hprInterval2, name="pandaPace")
        self.pandaPace = Sequence(posInterval1,hprInterval1, posInterval2, hprInterval2, name="pandaPace")
        self.pandaPace.loop()
        # self.pandaPace.loop()

        # self.setupCollision(cTrav)
    # def setupCollision(self, cTrav):
    #     if cTrav is None:
    #         return  # No collision traverser provided, skip setup
    #      # Tạo tia Ray chiếu từ trên xuống (cao 100 đơn vị so với gốc của gấu)
    #     ray = CollisionRay(0, 0, 100, 0, 0, -1)
    #     rayNode = CollisionNode('bearRay')
    #     rayNode.addSolid(ray)
    #     # Mask 1 để chỉ va chạm với môi trường (mặt đất)
    #     rayNode.setFromCollideMask(BitMask32.bit(1))
    #     rayNode.setIntoCollideMask(BitMask32.allOff())
        
    #     self.rayNodePath = self.attachNewNode(rayNode)
    #     self.floorHandler = CollisionHandlerFloor()
    #     self.floorHandler.addCollider(self.rayNodePath, self)
        
    #     # Đăng ký với hệ thống tính toán va chạm
    #     cTrav.addCollider(self.rayNodePath, self.floorHandler)

    def create_mesh_bear(self):
        self.mesh_bear = self.render.attachNewNode("mesh_bear")
        self.instanceTo(self.mesh_bear)

        # 2. Ép bản sao hiển thị dưới dạng lưới (Wireframe)
        self.mesh_bear.setRenderModeWireframe()
        self.mesh_bear.setRenderModeThickness(2) # Độ dày của sợi lưới
        
        # 3. Đặt màu sắc và tắt các hiệu ứng che khuất
        self.mesh_bear.setColor(1, 0, 0, 1, 1)   # Lưới màu Đỏ rực
        self.mesh_bear.setTextureOff(1)          # Tắt ảnh da gấu
        self.mesh_bear.setLightOff(1)            # Tắt bóng đổ

        # 4. KỸ THUẬT QUAN TRỌNG: Đẩy lưới nổi lên trên để không bị nhấp nháy với da gấu gốc
        self.mesh_bear.setDepthOffset(1)

        # Mặc định ẩn lưới đi
        self.mesh_bear.hide()

    def toggle_outline(self):
        """Hàm xử lý việc bật/tắt viền"""
        if self.mesh_bear.isHidden():
            self.mesh_bear.show()
        else:
            self.mesh_bear.hide()
    
    def changePandaScale(self, factor):
        """Scale the panda actor by factor."""
        s = self.getScale()
        self.setScale(s.getX() * factor, s.getY() * factor, s.getZ() * factor)

    def changePandaHeight(self, delta):
        """Adjust panda Z by delta."""
        self.setZ(self.getZ() + delta)

    def moveForward(self, distance):
        """Di chuyển gấu tiến hoặc lùi (dựa theo hướng đang xoay)."""
        self.setY(self, distance)

    def turn(self, angle):
        """Xoay gấu sang trái hoặc phải."""
        self.setH(self.getH() + angle)