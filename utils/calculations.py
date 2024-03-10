import math


def compute_next_ref_gps(last_ref_pose, angle_of_attack=40, step_distance=0.01) -> list:
        # Earth radius in kilometers
        R = 6371.0

        # Convert heading to radians
        heading_rad = math.radians(last_ref_pose.heading)
        
        # Convert angle of attack to radians
        angle_of_attack_rad = math.radians(angle_of_attack)

        # Calculate the change in latitude and longitude
        delta_lat = (step_distance * math.cos(heading_rad) * math.cos(angle_of_attack_rad)) / R
        delta_long = (step_distance * math.sin(heading_rad) * math.cos(angle_of_attack_rad)) / (R * math.cos(math.radians(last_ref_pose.lat)))

        # Calculate new latitude and longitude
        new_lat = last_ref_pose.lat + math.degrees(delta_lat)
        new_long = last_ref_pose.long + math.degrees(delta_long)

        # Assuming a linear descent, update altitude

        new_alt = last_ref_pose.alt - step_distance * math.sin(angle_of_attack_rad)

        print("new alt", new_alt)

        return [new_lat, new_long, new_alt, last_ref_pose.heading]


def spherical_law_of_cosines(coord1, coord2):
    lat1, lon1, alt1, _ = coord1
    lat2, lon2, alt2, _ = coord2

    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Spherical law of cosines formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # Earth's radius in kilometers
    radius_earth = 6371

    # Include altitude difference
    distance = math.sqrt((radius_earth * c)**2 + (alt2 - alt1)**2)

    return distance*1000  # meter

def compute_end_point(pose,angle_of_attack=40,step_distance=40):
    lat,long,alt,heading = compute_next_ref_gps(pose,angle_of_attack=40,step_distance=40)
    return lat,long,alt
