import carla
import cv2
import numpy as np
import time
import math
import csv

from src.camera import setup_camera, CarlaYOLO
from src.radar import setup_radar, get_radar_sel_obj
from src.vehicle_control import apply_vehicle_control
from src.fsn import get_radar_info, get_camera_info, fsn

csv_file_path = 'work/output_data.csv'
def main():
    sel_radar_obj_dist = float(326)
    sel_radar_obj_lat_pos = float(326)
    sel_cam_obj_dist = float(326)
    sel_cam_obj_lat_pos = float(326)
    sel_fsn_obj_dist = float(326)
    
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
    cnt = 0
    out_detected_obj = {}
    try:
        while True:
            sel_radar_obj_dist, sel_radar_obj_lat_pos = get_radar_sel_obj()  # 距離を取得
            sel_cam_obj_dist, sel_cam_obj_lat_pos, sel_obj_type = carla_yolo.get_camera_sel_obj()
            #simple fsn method to confirm object confidnce
            if (sel_radar_obj_dist + 5) > sel_cam_obj_dist > (sel_radar_obj_dist - 5):
                sel_fsn_obj_dist = sel_radar_obj_dist
            print(f'radar : {sel_radar_obj_dist}, camera : {sel_cam_obj_dist}')
            apply_vehicle_control(vehicles[0], 50, sel_fsn_obj_dist)
            get_radar_info(sel_radar_obj_dist, sel_radar_obj_lat_pos)
            get_camera_info(sel_cam_obj_dist, sel_cam_obj_lat_pos, sel_obj_type)
            fsn()
            out_detected_obj[cnt] = {
                'sel_radar_obj_dist' : sel_radar_obj_dist,
                'sel_radar_obj_lat_pos' : sel_radar_obj_lat_pos,
                'sel_cam_obj_dist' : sel_cam_obj_dist,
                'sel_cam_obj_lat_pos' : sel_cam_obj_lat_pos,
                'sel_cam_obj_type' : sel_obj_type,
                'sel_fsn_obj_dist' : sel_fsn_obj_dist
            }
            cnt += 1
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("Stopping...")# CSVファイルを開く（追記モード）
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            # ヘッダーを書き込む
            writer.writerow(['ID', 'sel_radar_obj_dist', 'sel_radar_obj_lat_pos', 'sel_cam_obj_dist', 'sel_cam_obj_lat_pos', 'sel_fsn_obj_dist'])
            
            # out_detected_obj の内容を書き込む
            for obj_id, obj_data in out_detected_obj.items():
                writer.writerow([
                    obj_id,
                    obj_data['sel_radar_obj_dist'],
                    obj_data['sel_radar_obj_lat_pos'],
                    obj_data['sel_cam_obj_dist'],
                    obj_data['sel_cam_obj_lat_pos'],
                    obj_data['sel_cam_obj_type'],
                    obj_data['sel_fsn_obj_dist']
                ])
    finally:
        for actor in [camera, radar, *vehicles]:
            actor.destroy()
        carla_yolo.release_video_writer()  # VideoWriter を解放
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
