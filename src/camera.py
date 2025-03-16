import carla
import cv2
import numpy as np

# Video Writer setup
video_writer = None

def initialize_video_writer():
    """Initialize the video writer."""
    global video_writer
    if video_writer is None:
        video_writer = cv2.VideoWriter('work/output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (1600, 900))

def process_image(image):
    """Convert CARLA image to OpenCV format, display it, and save to video."""
    global video_writer
    initialize_video_writer()  # Ensure video writer is initialized

    array = np.frombuffer(image.raw_data, dtype=np.uint8).reshape((image.height, image.width, 4))
    array = cv2.cvtColor(array[:, :, :3], cv2.COLOR_BGR2RGB)
    cv2.imshow("Camera View", array)
    video_writer.write(array)  # Save frame to video
    cv2.waitKey(1)

def setup_camera(world, vehicle):
    """Setup camera sensor and attach it to the vehicle."""
    blueprint_library = world.get_blueprint_library()
    camera_bp = blueprint_library.find('sensor.camera.rgb')
    camera_bp.set_attribute('image_size_x', '1600')
    camera_bp.set_attribute('image_size_y', '900')
    camera_bp.set_attribute('fov', '90')
    camera_bp.set_attribute('sensor_tick', '0.05')  # Set FPS to 30
    
    camera = world.spawn_actor(camera_bp, carla.Transform(carla.Location(x=1.5, z=2.0)), attach_to=vehicle)
    camera.listen(process_image)
    
    return camera

def release_video_writer():
    """Release the video writer."""
    global video_writer
    if video_writer is not None:
        video_writer.release()
        video_writer = None
