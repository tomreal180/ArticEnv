from panda3d.core import AmbientLight, DirectionalLight, Fog, Vec4
class EnvironmentSystem:
    def __init__(self, loader, render, config=None):
        #Initialize environment system with lighting, fog, and scene loading
        self.loader = loader
        self.render = render
        self.fog_color = Vec4(0.8, 0.85, 0.9, 1.0) # Màu sương mù trùng với bầu trời
        if config is None:
            config = {}
        #Configure environment settings like lighting and fog
        # Enviroment lighting
        alight = AmbientLight('alight')
        alight.setColor(Vec4(0.5, 0.6, 0.7, 1)) # Xanh nhạt
        self.render.setLight(self.render.attachNewNode(alight))

        # Enviroment lighting shadow
        dlight = DirectionalLight('dlight')
        dlight.setColor(Vec4(0.7, 0.7, 0.75, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(45, -45, 0)
        self.render.setLight(dlnp)
        # Enviroment fog
        blizzard_fog = Fog("Blizzard Fog")
        blizzard_fog.setColor(self.fog_color)
        blizzard_fog.setExpDensity(0.015) # Độ đặc của sương (tăng số này sương sẽ dày hơn)
        self.render.setFog(blizzard_fog)
    
        #Load scene model
        self.scene = self.loader.loadModel(config.get("model_path","assets/models/snow_mountain/scene.gltf"))
        self.scene.reparentTo(self.render)
        scene_scale = config.get("scale", 1.0)
        self.scene.setScale(scene_scale, scene_scale, scene_scale)

        

    def changeSceneScale(self, factor):
        """Scale the loaded scene by factor."""
        s = self.scene.getScale()
        self.scene.setScale(s.getX() * factor, s.getY() * factor, s.getZ() * factor)    