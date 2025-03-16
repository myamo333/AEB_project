import carla
import cv2
import numpy as np
from ultralytics import YOLO

class CarlaYOLO:
    def __init__(self, model_path='model/yolov8n.pt', output_video='work/output.mp4', video_size=(1600, 900), fps=30):
        # Load YOLOv8 model
        self.model = YOLO(model_path)
        self.video_writer = None
        self.output_video = output_video
        self.video_size = video_size
        self.fps = fps

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

        for i, box in enumerate(boxes):
            x, y, w, h = box
            label_id = int(results[0].boxes.cls[i])  # Class ID
            label = labels[label_id]  # Get class name using the ID
            
            # 車両、歩行者、自転車のいずれかであれば描画
            if label in target_classes:
                score = scores[i]  # Confidence score

                # Convert box coordinates to integer
                x1, y1, x2, y2 = int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)

                # Draw bounding box
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Put label and confidence score
                cv2.putText(image, f'{label} {score:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


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
