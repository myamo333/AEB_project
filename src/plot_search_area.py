import matplotlib.pyplot as plt
import numpy as np
import math
from fsn import set_search_area

def calculate_sector(x, y):
    """指定した座標を基に検知範囲を計算"""
    result = set_search_area(x, y)
    
    d_min = result["d_min"]
    d_max = result["d_max"]
    theta_min = math.radians(result["theta_area"][0])
    theta_max = math.radians(result["theta_area"][1])
    
    angles = np.linspace(theta_min, theta_max, 50)
    
    x_min_arc = d_min * np.cos(angles)
    y_min_arc = d_min * np.sin(angles)
    x_max_arc = d_max * np.cos(angles)
    y_max_arc = d_max * np.sin(angles)

    return (d_min, d_max, theta_min, theta_max, x_min_arc, y_min_arc, x_max_arc, y_max_arc)

def plot_sector(d_min, d_max, theta_min, theta_max, x_min_arc, y_min_arc, x_max_arc, y_max_arc, color, label_prefix):
    """扇形の範囲を描画"""
    plt.plot(x_min_arc, y_min_arc, f"{color}--", label=f"{label_prefix} Min Range")
    plt.plot(x_max_arc, y_max_arc, f"{color}-", label=f"{label_prefix} Max Range")

    # 境界線を描画
    plt.plot([d_min * np.cos(theta_min), d_max * np.cos(theta_min)], 
             [d_min * np.sin(theta_min), d_max * np.sin(theta_min)], f"{color}-")
    plt.plot([d_min * np.cos(theta_max), d_max * np.cos(theta_max)], 
             [d_min * np.sin(theta_max), d_max * np.sin(theta_max)], f"{color}-")

def plot_radar_camera_sector(radar_x, radar_y, camera_x, camera_y, target_x, target_y):
    """レーダーとカメラの検知範囲をプロット"""
    # レーダーとカメラの検知範囲を計算
    radar_sector = calculate_sector(radar_x, radar_y)
    camera_sector = calculate_sector(target_x, target_y)

    plt.figure(figsize=(8, 8))

    # レーダー描画
    plt.plot(0, 1, 'ro', label="Radar")  # レーダー位置
    plot_sector(*radar_sector, 'b', "Radar")

    # カメラ描画
    plt.plot(camera_x, camera_y, 'bo', label="Camera")  # カメラ位置
    plot_sector(*camera_sector, 'm', "Camera")

    # 物標（ターゲット）
    plt.plot(target_x, target_y, 'gx', markersize=10, label="Target")

    # レーダーとカメラの方向線
    plt.plot([0, radar_x], [0, radar_y], 'k-', label="Radar Direction")
    plt.plot([camera_x, target_x], [camera_y, target_y], 'y-', label="Target Direction")

    # グラフ設定
    plt.xlabel("X (横位置)")
    plt.ylabel("Y (縦距離)")
    plt.title("Radar and Camera Detection")
    plt.legend()
    plt.grid()
    plt.axis("equal")

    # 描画
    plt.show()

# 例: レーダー、カメラ、物標の位置
plot_radar_camera_sector(1, 10, 0, 0, 1, 7)
