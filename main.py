import carla
import cv2
import numpy as np
import time
import math

from src.camera import setup_camera, release_video_writer
from src.radar import setup_radar, get_front_vehicle_distance
from src.vehicle_control import apply_vehicle_control

def main():
    global front_vehicle_distance
    front_vehicle_distance = float('inf')
    
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.load_world('Town06')
    time.sleep(2)
    
    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.filter('model3')[0]
    
    spawn_points = [
        carla.Transform(carla.Location(x=-102.95, y=45.43, z=1), carla.Rotation(yaw=0)),
        carla.Transform(carla.Location(x=20.95, y=45.43, z=1), carla.Rotation(yaw=0))
    ]
    
    vehicles = [world.try_spawn_actor(vehicle_bp, sp) for sp in spawn_points]
    if any(v is None for v in vehicles):
        print("Failed to spawn one or more vehicles.")
        return
    
    camera = setup_camera(world, vehicles[0])
    radar = setup_radar(world, vehicles[0])
    
    try:
        while True:
            front_vehicle_distance = get_front_vehicle_distance()  # 距離を取得
            apply_vehicle_control(vehicles[0], 50, front_vehicle_distance)
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        for actor in [camera, radar, *vehicles]:
            actor.destroy()
        release_video_writer()  # VideoWriter を解放
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
