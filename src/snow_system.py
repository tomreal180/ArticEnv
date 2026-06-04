from panda3d.core import Vec3,Vec4, CardMaker, TransparencyAttrib
import random

class SnowSystem:
    def __init__(self, loader, render, taskMgr, globalClock, config=None):
        self.loader = loader
        self.render = render
        self.taskMgr = taskMgr
        self.globalClock = globalClock
        
        if config is None:
            config = {}

        #Configuration of snow system
        self.num_flakes = config.get("num_flakes", 1000)
        wind = config.get("wind_vector", [15, -5, -15])
        self.wind_vector = Vec3(wind[0], wind[1], wind[2])
        self.spawn_bounds = config.get("spawn_bounds", [-40, 40, -40, 40, -30, 20]) # (minX, maxX, minY, maxY, minZ, maxZ)
        tex_path = config.get("texture_path", "assets/textures/snowflake.png")
        self.snow_tex = self.loader.loadTexture(tex_path)
        self.snow_particles = []

        self.snow_root = self.render.attachNewNode("snow_root")

        self.create_snow()
        self.taskMgr.add(self.update_snow, "update_snow_task")

    def create_snow(self):
        flake_cm = CardMaker('flake')
        flake_cm.setFrame(-0.1, 0.1, -0.1, 0.1)

        for _ in range(self.num_flakes):
            flake = self.snow_root.attachNewNode(flake_cm.generate())
            x = random.uniform(self.spawn_bounds[0], self.spawn_bounds[1])
            y = random.uniform(self.spawn_bounds[2], self.spawn_bounds[3])
            z = random.uniform(self.spawn_bounds[4], self.spawn_bounds[5])
            flake.setPos(x, y, z)
            flake.setBillboardPointEye()
            flake.setColor(Vec4(1, 1, 1, 0.8))

            #set texture and transparency
            flake.setTexture(self.snow_tex)
            flake.setTransparency(TransparencyAttrib.MAlpha)

            self.snow_particles.append(flake)

    def update_snow(self, task):
        dt = self.globalClock.getDt()
        movement = self.wind_vector * dt

        for flake in self.snow_particles:
            new_pos = flake.getPos() + movement

            if new_pos.getZ() < self.spawn_bounds[4]:
                new_pos.setZ(self.spawn_bounds[5])
            if new_pos.getX() > self.spawn_bounds[1]:
                new_pos.setX(self.spawn_bounds[0])
            if new_pos.getY() < self.spawn_bounds[2]:
                new_pos.setY(self.spawn_bounds[3])

            flake.setPos(new_pos)

        return task.cont