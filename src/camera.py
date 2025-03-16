import carla
import cv2
import numpy as np
from ultralytics import YOLO

class CarlaYOLO:
    def __init__(self, model_path='model/yolov8n.pt', output_video='work/output.mp4', video_size=(1600, 900), fps=30, focal_length=800):
        # Load YOLOv8 model
        self.model = YOLO(model_path)
        self.video_writer = None
        self.output_video = output_video
        self.video_size = video_size
        self.fps = fps
        self.focal_length = focal_length  # 仮の焦点距離（カメラの特性に合わせて調整）
        self.min_distance = float('inf')

        # カメラ行列
        self.camera_matrix = np.array([[self.focal_length, 0, video_size[0] // 2],
                                       [0, self.focal_length, video_size[1] // 2],
                                       [0, 0, 1]])

        # 物体の実際の高さ（メートル単位）
        self.object_heights = {
            "car": 1.440,
            "truck": 3.0,
            "bus": 3.2,
            "person": 1.7,
            "bicycle": 1.1
        }

    def initialize_video_writer(self):
        """Initialize the video writer."""
        if self.video_writer is None:
            self.video_writer = cv2.VideoWriter(
                self.output_video, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, self.video_size
            )

    def process_image(self, image):
        """Convert CARLA image to OpenCV format, perform YOLO object detection, and save to video."""
        self.initialize_video_writer()  # Ensure video writer is initialized

        # Convert CARLA image to OpenCV format (RGB)
        array = self._carla_to_opencv(image)

        # Perform YOLO object detection
        results = self.model(array)  # Perform detection using YOLOv8
        self._draw_bounding_boxes(array, results)

        # Display and save the image with bounding boxes
        self._display_and_save(array)

    def _carla_to_opencv(self, image):
        """Convert CARLA image to OpenCV format (RGB)."""
        array = np.frombuffer(image.raw_data, dtype=np.uint8).reshape((image.height, image.width, 4))
        return cv2.cvtColor(array[:, :, :3], cv2.COLOR_BGR2RGB)

    def _draw_bounding_boxes(self, image, results):
        """Draw bounding boxes and labels on the image for vehicles, pedestrians, and bicycles."""
        boxes = results[0].boxes.xywh.numpy()  # Bounding boxes (x, y, width, height)
        labels = results[0].names  # Class names
        scores = results[0].boxes.conf.numpy()  # Confidence scores

        # クラスIDに対応するオブジェクトのリスト (車両、歩行者、自転車)
        target_classes = ['car', 'truck', 'bus', 'person', 'bicycle']
        detected_objects={}
        for i, box in enumerate(boxes):
            x, y, w, h = box
            label_id = int(results[0].boxes.cls[i])  # Class ID
            label = labels[label_id]  # Get class name using the ID
            # 車両、歩行者、自転車のいずれかであれば描画
            if label in target_classes:
                score = scores[i]  # Confidence score

                # Convert box coordinates to integer
                x1, y1, x2, y2 = int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)

                # 距離を計算
                z = self._estimate_distance(label, h)

                # 3D座標変換
                x_3d, y_3d = self._get_3d_position(x, y, z)

                # Draw bounding box
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Put label and confidence score
                cv2.putText(image, f'{label} {score:.2f} ({x_3d:.2f}, {y_3d:.2f}, {z:.2f}m)',
                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                detected_objects[i] = {
                    'label' : label,
                    'x_3d' : x_3d,
                    'y_3d' : y_3d,
                    'z_3d' : z
                }
        if detected_objects:
            for tmp_id in detected_objects:
                x_3d, z_3d = detected_objects[tmp_id]['x_3d'], detected_objects[tmp_id]['z_3d']
                
                # 正面に近いオブジェクトを探す（x_3d が 0 に近いほど正面）
                distance_from_center = abs(x_3d)

                # 最も正面に近く、かつ最も z_3d が小さい（近い）オブジェクトを選択
                if distance_from_center < 1.0 and z_3d < self.min_distance:  # 1.0 は許容範囲（調整可能）
                    self.min_distance = z_3d
        print(self.min_distance)
            
    def get_camera_min_distance(self):
        return self.min_distance
                
    def _estimate_distance(self, label, bbox_height):
        """Estimate the distance to the object using its height in the image."""
        if label in self.object_heights:
            H = self.object_heights[label]  # 実際の高さ
            h = bbox_height  # 画像内の高さ（ピクセル）
            f = self.focal_length  # 焦点距離
            if h > 0:  # 0除算防止
                return (H * f) / h
        return 10.0  # デフォルト値（推定失敗時）

    def _get_3d_position(self, x_2d, y_2d, z):
        """Convert 2D bounding box center to 3D position."""
        fx = self.camera_matrix[0, 0]
        fy = self.camera_matrix[1, 1]
        cx = self.camera_matrix[0, 2]
        cy = self.camera_matrix[1, 2]

        x_3d = (x_2d - cx) * z / fx
        y_3d = (y_2d - cy) * z / fy
        return x_3d, y_3d

    def _display_and_save(self, image):
        """Display the image with bounding boxes and save to video."""
        cv2.imshow("Camera View", image)
        self.video_writer.write(image)  # Save frame to video
        cv2.waitKey(1)

    def release_video_writer(self):
        """Release the video writer."""
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None

def setup_camera(world, vehicle, camera_listener):
    """Setup camera sensor and attach it to the vehicle."""
    blueprint_library = world.get_blueprint_library()
    camera_bp = blueprint_library.find('sensor.camera.rgb')
    camera_bp.set_attribute('image_size_x', '1600')
    camera_bp.set_attribute('image_size_y', '900')
    camera_bp.set_attribute('fov', '90')
    camera_bp.set_attribute('sensor_tick', '0.05')  # Set FPS to 30

    camera = world.spawn_actor(camera_bp, carla.Transform(carla.Location(x=1.5, z=2.0)), attach_to=vehicle)
    camera.listen(camera_listener)

    return camera
