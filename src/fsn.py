import math

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

def fsn():
    fsn_result = {}
    radar_result = set_search_area(fl_g_sel_radar_obj_dist, fl_g_sel_radar_obj_lat_pos)
    camera_result = set_search_area(fl_g_sel_cam_obj_dist, fl_g_sel_cam_obj_lat_pos)
    print(radar_result)
    print(camera_result)
    print(fsn_result)