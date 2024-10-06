import pandas as pd
import numpy as np
from astroquery.gaia import Gaia

def query_gaia_dr3():
    # PLACEHOLDER: Modify this query as needed to get the desired star data
    query = """
    SELECT TOP 1000
        source_id, ra, dec, parallax, phot_g_mean_mag
    FROM gaiadr3.gaia_source
    WHERE parallax > 0 AND phot_g_mean_mag < 6
    """
    job = Gaia.launch_job(query)
    result = job.get_results()
    return result

def load_exoplanet_data(file_path):
    df = pd.read_csv(file_path)
    required_columns = ['ra', 'dec', 'sy_dist']
    
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' is missing from the dataset.")
    
    df['ra'] = df['ra'].apply(lambda x: sexagesimal_to_decimal(x, is_ra=True))
    df['dec'] = df['dec'].apply(lambda x: sexagesimal_to_decimal(x, is_ra=False))
    
    return df

def sexagesimal_to_decimal(sexagesimal_str, is_ra=True):
    parts = sexagesimal_str.split(':')
    if len(parts) != 3:
        raise ValueError(f"Invalid sexagesimal format: {sexagesimal_str}")
    
    hours_or_degrees = float(parts[0])
    minutes = float(parts[1])
    seconds = float(parts[2])
    
    decimal_value = abs(hours_or_degrees) + minutes / 60 + seconds / 3600
    
    if is_ra:
        decimal_value *= 15  # 1 hour of RA equals 15 degrees
    elif hours_or_degrees < 0:
        decimal_value = -decimal_value
    
    return decimal_value

def convert_to_exoplanet_frame(star_ra, star_dec, star_distance, exo_ra, exo_dec, exo_distance):
    star_x, star_y, star_z = spherical_to_cartesian(star_ra, star_dec, star_distance)
    exo_x, exo_y, exo_z = spherical_to_cartesian(exo_ra, exo_dec, exo_distance)
    
    relative_x = star_x - exo_x
    relative_y = star_y - exo_y
    relative_z = star_z - exo_z
    
    return cartesian_to_spherical(relative_x, relative_y, relative_z)

def spherical_to_cartesian(ra, dec, distance):
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)
    x = distance * np.cos(dec_rad) * np.cos(ra_rad)
    y = distance * np.cos(dec_rad) * np.sin(ra_rad)
    z = distance * np.sin(dec_rad)
    return x, y, z

def cartesian_to_spherical(x, y, z):
    distance = np.sqrt(x**2 + y**2 + z**2)
    dec = np.degrees(np.arcsin(z / distance))
    ra = np.degrees(np.arctan2(y, x)) % 360
    return ra, dec, distance

def rotate_coordinates(ra, dec, lambda_angle, epsilon_angle):
    lambda_rad = np.radians(lambda_angle)
    epsilon_rad = np.radians(epsilon_angle)

    x, y, z = spherical_to_cartesian(ra, dec, 1)

    Rz = np.array([[np.cos(lambda_rad), -np.sin(lambda_rad), 0],
                   [np.sin(lambda_rad),  np.cos(lambda_rad), 0],
                   [0,                   0,                  1]])

    Rx = np.array([[1, 0,                   0],
                   [0, np.cos(epsilon_rad), -np.sin(epsilon_rad)],
                   [0, np.sin(epsilon_rad),  np.cos(epsilon_rad)]])

    rotation_matrix = np.dot(Rx, Rz)

    rotated_coordinates = rotation_matrix @ np.array([x, y, z])
    return cartesian_to_spherical(rotated_coordinates[0], rotated_coordinates[1], rotated_coordinates[2])

def process_star_data(exo_ra, exo_dec, exo_distance):
    stars = query_gaia_dr3()
    processed_stars = []

    for star in stars:
        ra, dec, distance = convert_to_exoplanet_frame(
            star['ra'], star['dec'], 1000 / star['parallax'],
            exo_ra, exo_dec, exo_distance
        )
        
        # PLACEHOLDER: Replace these with actual values or make them configurable
        lambda_angle = 45
        epsilon_angle = 23.5
        
        rotated_ra, rotated_dec, _ = rotate_coordinates(ra, dec, lambda_angle, epsilon_angle)
        
        processed_stars.append({
            'id': str(star['source_id']),
            'ra': rotated_ra,
            'dec': rotated_dec,
            'magnitude': star['phot_g_mean_mag']
        })

    return processed_stars