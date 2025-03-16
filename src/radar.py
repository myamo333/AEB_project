import carla
import math

# グローバル変数として radar_min_dist を定義
radar_min_dist = float('inf')

def get_radar_min_dist():
    """現在の前方車両との距離を取得"""
    global radar_min_dist
    return radar_min_dist

def radar_callback(data):
    """Radar センサーのコールバック関数"""
    global radar_min_dist
    detected_objects = {
        i: {
            'distance': d.depth,
            'azimuth': d.azimuth,
            'velocity': d.velocity,
            'altitude': d.altitude
        }
        for i, d in enumerate(data) if d.altitude > -0.1 * math.pi / 180
    }
    if detected_objects:
        radar_min_dist = min(detected_objects.values(), key=lambda x: abs(x['azimuth']))['distance']

def setup_radar(world, vehicle):
    """Radar センサーをセットアップ"""
    blueprint_library = world.get_blueprint_library()
    radar_bp = blueprint_library.find('sensor.other.radar')
    radar_bp.set_attribute('horizontal_fov', '30')
    radar_bp.set_attribute('range', '100')
    radar_bp.set_attribute('points_per_second', '1500')
    
    radar = world.spawn_actor(radar_bp, carla.Transform(carla.Location(x=2.5, z=0.5)), attach_to=vehicle)
    radar.listen(radar_callback)
    
    return radar
