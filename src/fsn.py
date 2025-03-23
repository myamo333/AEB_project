import math
import numpy as np
from shapely.geometry import Polygon

fl_g_sel_radar_obj_dist = 326
fl_g_sel_radar_obj_lat_pos = 326
fl_g_sel_cam_obj_dist = 326
fl_g_sel_cam_obj_lat_pos = 326
u1_g_sel_obj_type = ""

def get_radar_info(sel_radar_obj_dist, sel_radar_obj_lat_pos):
    global fl_g_sel_radar_obj_dist, fl_g_sel_radar_obj_lat_pos
    fl_g_sel_radar_obj_dist = sel_radar_obj_dist
    fl_g_sel_radar_obj_lat_pos = sel_radar_obj_lat_pos

def get_camera_info(sel_cam_obj_dist, sel_cam_obj_lat_pos, sel_obj_type):
    global fl_g_sel_cam_obj_dist, fl_g_sel_cam_obj_lat_pos, u1_g_sel_obj_type
    fl_g_sel_cam_obj_dist = sel_cam_obj_dist
    fl_g_sel_cam_obj_lat_pos = sel_cam_obj_lat_pos
    u1_g_sel_obj_type = sel_obj_type

def set_search_area(x, y):
    d = math.sqrt(x*x + y*y)
    d_max = d * 1.2
    d_min = d * 0.8
    theta = math.degrees(math.atan2(y, x))
    theta_min = theta - 5
    theta_max = theta + 5
    return {
        "d": d,
        "d_min": d_min,
        "d_max": d_max,
        "theta": theta,
        "theta_area": (theta_min, theta_max)
    }

def generate_sector_polygon(x, y):
    """指定した座標を基に扇形のポリゴンを生成"""
    result = set_search_area(x, y)

    d_min = result["d_min"]
    d_max = result["d_max"]
    theta_min = math.radians(result["theta_area"][0])
    theta_max = math.radians(result["theta_area"][1])

    angles = np.linspace(theta_min, theta_max, 50)  # 50分割で滑らかに

    # 最小・最大距離の弧の点を計算
    min_arc = [(d_min * np.cos(a), d_min * np.sin(a)) for a in angles]
    max_arc = [(d_max * np.cos(a), d_max * np.sin(a)) for a in reversed(angles)]

    # ポリゴンの点を並べる (時計回り)
    polygon_points = min_arc + max_arc + [min_arc[0]]

    # Shapelyのポリゴンオブジェクトを生成
    polygon = Polygon(polygon_points)

    # ポリゴンオブジェクトと、その頂点リストを返す
    return polygon, polygon_points

def detect_overlap_with_polygon(radar_x, radar_y, camera_x, camera_y):
    """ポリゴンの交差判定による重なりチェック"""
    radar_polygon, radar_points = generate_sector_polygon(radar_x, radar_y)
    camera_polygon, camera_points = generate_sector_polygon(camera_x, camera_y)

    return radar_polygon.intersects(camera_polygon)  # Trueなら重なっている

def fsn():
    radar_result = set_search_area(fl_g_sel_radar_obj_dist, fl_g_sel_radar_obj_lat_pos)
    camera_result = set_search_area(fl_g_sel_cam_obj_dist, fl_g_sel_cam_obj_lat_pos)
    fsn_result = detect_overlap_with_polygon(fl_g_sel_radar_obj_lat_pos, fl_g_sel_radar_obj_dist, fl_g_sel_cam_obj_lat_pos, fl_g_sel_cam_obj_dist)
    print(radar_result)
    print(camera_result)
    print(fsn_result)