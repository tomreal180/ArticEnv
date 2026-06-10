from panda3d.core import AmbientLight, DirectionalLight, Fog, Vec4
class EnvironmentSystem:
    def __init__(self, loader, render, config=None):
        #Initialize environment system with lighting, fog, and scene loading
        self.loader = loader
        self.render = render
        self.fog_color = None 
        if config is None:
            config = {}
        #Configure environment settings like lighting and fog
        self.setupBlizzardEffect()  # Mặc định là hiệu ứng bão tuyết, có thể toggle sang ngày hè nắng chói bằng MyApp.toggleBlizzardEffect()
    
        #Load scene model
        self.scene = self.loader.loadModel(config.get("model_path","assets/models/snow_mountain/scene.gltf"))
        self.scene.reparentTo(self.render)
        scene_scale = config.get("scale", 1.0)
        self.scene.setScale(scene_scale, scene_scale, scene_scale)

        

    def changeSceneScale(self, factor):
        """Scale the loaded scene by factor."""
        s = self.scene.getScale()
        self.scene.setScale(s.getX() * factor, s.getY() * factor, s.getZ() * factor)    

    def updateFogDensity(self, delta):
        """Update the fog density by delta (positive to increase, negative to decrease)."""
        if self.render.hasFog():
            fog = self.render.getFog()
            new_density = max(0, fog.getExpDensity() + delta)  # Ensure density doesn't go negative
            fog.setExpDensity(new_density)

    def setupBlizzardEffect(self):
        """Enable or disable blizzard effect by adjusting fog density."""
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
        self.fog_color = Vec4(0.5, 0.6, 0.7, 1) # Màu sương mù trùng với màu bầu trời để tạo hiệu ứng mờ ảo
        blizzard_fog = Fog("Blizzard Fog")
        blizzard_fog.setColor(self.fog_color)
        blizzard_fog.setExpDensity(0.015) # Độ đặc của sương (tăng số này sương sẽ dày hơn)
        self.render.setFog(blizzard_fog)       

    def setupSunnySummerEffect(self):
        """Switch to a sunny summer environment by changing lighting and fog settings."""
        self.render.clearFog() # Xóa sương mù cũ trước khi thiết lập cái mới

        # Ánh sáng môi trường (sáng và trong trẻo hơn)
        alight = AmbientLight('alight_summer')
        alight.setColor(Vec4(0.8, 0.85, 0.9, 1))
        self.render.setLight(self.render.attachNewNode(alight))

        # Ánh sáng mặt trời (màu vàng ấm)
        dlight = DirectionalLight('sunlight')
        dlight.setColor(Vec4(0.95, 0.9, 0.8, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(60, -60, 0) # Góc chiếu từ trên cao xuống
        self.render.setLight(dlnp)

        # Sương mù mỏng tạo chiều sâu (màu xanh da trời nhạt)
        self.fog_color = Vec4(0.6, 0.75, 0.9, 1) 
        summer_fog = Fog("Summer Fog")
        summer_fog.setColor(self.fog_color)
        summer_fog.setExpDensity(0.002) # Sương rất loãng so với 0.015 của bão tuyết
        self.render.setFog(summer_fog)