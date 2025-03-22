import carla
import math

# グローバル変数として sel_radar_obj_dist を定義
sel_radar_obj_dist = float(326)
sel_radar_obj_lat_pos = float(326)

def get_radar_sel_obj():
    """現在の前方車両との距離を取得"""
    global sel_radar_obj_dist, sel_radar_obj_lat_pos
    return sel_radar_obj_dist, sel_radar_obj_lat_pos

def radar_callback(data):
    """Radar センサーのコールバック関数"""
    global sel_radar_obj_dist, sel_radar_obj_lat_pos
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
        for obj in detected_objects:
            x_3d, y_3d, z_3d = radar_to_cartesian(detected_objects[obj]['distance'], detected_objects[obj]['azimuth'], detected_objects[obj]['altitude'])

            if z_3d < sel_radar_obj_dist:
                sel_radar_obj_dist = z_3d
                sel_radar_obj_lat_pos = x_3d


def radar_to_cartesian(depth, azimuth, altitude):
    x = depth * math.cos(altitude) * math.sin(azimuth)
    y = depth * math.sin(altitude)
    z = depth * math.cos(altitude) * math.cos(azimuth)
    
    return x, y, z

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
