import math

def apply_vehicle_control(vehicle, target_speed, front_vehicle_distance):
    """Adjust vehicle throttle and brake based on target speed and distance to front vehicle."""
    velocity = vehicle.get_velocity()
    current_speed_kmh = math.sqrt(velocity.x**2 + velocity.y**2 + velocity.z**2) * 3.6
    speed_difference = target_speed - current_speed_kmh
    control = vehicle.get_control()
    
    if front_vehicle_distance <= 15:
        print("⚠️ AEB Activated! Braking...")
        control.throttle, control.brake = 0, 1
    else:
        control.throttle, control.brake = (0.5, 0) if speed_difference > 0 else (0, 0.5) if speed_difference < 0 else (0, 0)
    
    vehicle.apply_control(control)
