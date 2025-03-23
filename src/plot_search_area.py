import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.patches import Polygon as MplPolygon
from fsn import set_search_area, generate_sector_polygon

def plot_polygons(radar_x, radar_y, camera_x, camera_y):
    """レーダーとカメラのポリゴンを描画"""
    radar_polygon, radar_points = generate_sector_polygon(radar_x, radar_y)
    camera_polygon, camera_points = generate_sector_polygon(camera_x, camera_y)

    fig, ax = plt.subplots(figsize=(8, 8))

    # レーダー描画
    plt.plot(0, 1, 'ro')  # レーダー位置

    # カメラ描画
    plt.plot(0, 0, 'bo')  # カメラ位置

    # レーダーのポリゴン描画
    radar_patch = MplPolygon(radar_points, closed=True, edgecolor='b', facecolor='b', alpha=0.3, label="Radar Area")
    ax.add_patch(radar_patch)

    # カメラのポリゴン描画
    camera_patch = MplPolygon(camera_points, closed=True, edgecolor='m', facecolor='m', alpha=0.3, label="Camera Area")
    ax.add_patch(camera_patch)

    # レーダーとカメラの位置
    ax.plot(radar_x, radar_y, 'ro', label="Radar_object")
    ax.plot(camera_x, camera_y, 'bo', label="Camera_object")

    # 設定
    ax.set_xlabel("X (横位置)")
    ax.set_ylabel("Y (縦距離)")
    ax.set_title("Radar and Camera Detection Area")
    ax.legend()
    ax.grid()
    ax.axis("equal")

    # 描画
    plt.show()

# 例: レーダー、カメラ、物標の位置
plot_polygons(-0.03236273905, 8.556522068, 2.2, 12.5)
	