import carla
import cv2
import numpy as np
import time
import math

from src.camera import setup_camera, CarlaYOLO
from src.radar import setup_radar, get_radar_min_dist
from src.vehicle_control import apply_vehicle_control

def main():
    radar_min_dist = float('inf')
    camera_min_dist = float('inf')
    fsn_min_dist = float('inf')
    
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.load_world('Town06')
    time.sleep(2)
    
    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.filter('model3')[0]
    pedestrian_bp = blueprint_library.find('walker.pedestrian.0003')
    
    spawn_points = [
        carla.Transform(carla.Location(x=-102.95, y=45.43, z=1), carla.Rotation(yaw=0)),
        carla.Transform(carla.Location(x=20.95, y=45.43, z=1), carla.Rotation(yaw=0))
    ]
    spawn_points_ped = carla.Transform(carla.Location(x=20.95, y=50.43, z=1), carla.Rotation(yaw=0))
    
    vehicles = [world.try_spawn_actor(vehicle_bp, sp) for sp in spawn_points]
    pedestrian = world.spawn_actor(pedestrian_bp, spawn_points_ped)
    if any(v is None for v in vehicles):
        print("Failed to spawn one or more vehicles.")
        return
    # CarlaYOLOインスタンスを作成
    carla_yolo = CarlaYOLO()
    camera = setup_camera(world, vehicles[0], carla_yolo.process_image)
    radar = setup_radar(world, vehicles[0])
    
    try:
        while True:
            radar_min_dist = get_radar_min_dist()  # 距離を取得
            camera_min_dist = carla_yolo.get_camera_min_distance()
            #simple fsn method to confirm object confidnce
            if (radar_min_dist + 5) > camera_min_dist > (radar_min_dist - 5):
                fsn_min_dist = radar_min_dist
            print(f'radar : {radar_min_dist}, camera : {camera_min_dist}')
            apply_vehicle_control(vehicles[0], 50, fsn_min_dist)
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        for actor in [camera, radar, *vehicles]:
            actor.destroy()
        carla_yolo.release_video_writer()  # VideoWriter を解放
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
