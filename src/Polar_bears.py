from direct.actor.Actor import Actor
from panda3d.core import CollisionNode, CollisionRay, CollisionHandlerFloor, BitMask32
class PolarBears(Actor):
    def __init__(self, render, config=None, cTrav=None):
        self.render = render
        if config is None:
            config = {}
        actor_model = config.get("model_path", "assets/models/polar_bear_walk.glb")
        super().__init__(actor_model, {"walk": actor_model})
        self.reparentTo(self.render)
        actor_scale = config.get("scale", 1.0)
        self.setScale(actor_scale, actor_scale, actor_scale)
        # lower panda slightly so it sits closer to the ground
        # adjust this value as needed
        self.setZ(config.get("z_pos", 0))
        self.loop("walk")

        self.setupCollision(cTrav)
    def setupCollision(self, cTrav):
        if cTrav is None:
            return  # No collision traverser provided, skip setup
         # Tạo tia Ray chiếu từ trên xuống (cao 100 đơn vị so với gốc của gấu)
        ray = CollisionRay(0, 0, 100, 0, 0, -1)
        rayNode = CollisionNode('bearRay')
        rayNode.addSolid(ray)
        # Mask 1 để chỉ va chạm với môi trường (mặt đất)
        rayNode.setFromCollideMask(BitMask32.bit(1))
        rayNode.setIntoCollideMask(BitMask32.allOff())
        
        self.rayNodePath = self.attachNewNode(rayNode)
        self.floorHandler = CollisionHandlerFloor()
        self.floorHandler.addCollider(self.rayNodePath, self)
        
        # Đăng ký với hệ thống tính toán va chạm
        cTrav.addCollider(self.rayNodePath, self.floorHandler)
    
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