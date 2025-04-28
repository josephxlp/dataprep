import rasterio
import numpy as np
from rasterio.plot import show

def dem_rem_geoid(ellipsoid_height, geoid_height):
    return ellipsoid_height - geoid_height  # Orthometric = Ellipsoid - Geoid

def dem_add_geoid(orthometric_height, geoid_height):
    return orthometric_height + geoid_height  # Ellipsoid = Orthometric + Geoid

def ellipsoid2orthometric(ellipsoid_dem_path, geoid_model_path, orthometric_output_path):
    with rasterio.open(ellipsoid_dem_path) as dem_src, rasterio.open(geoid_model_path) as geoid_src:
        ellipsoid_height = dem_src.read(1)
        geoid_height = geoid_src.read(1)
        profile = dem_src.profile
        orthometric_height = dem_rem_geoid(ellipsoid_height, geoid_height)
    
    profile.update(dtype=rasterio.float32)
    with rasterio.open(orthometric_output_path, 'w', **profile) as dst:
        dst.write(orthometric_height.astype(np.float32), 1)

def orthometric2ellipsoid(orthometric_dem_path, geoid_model_path, ellipsoid_output_path):
    with rasterio.open(orthometric_dem_path) as dem_src, rasterio.open(geoid_model_path) as geoid_src:
        orthometric_height = dem_src.read(1)
        geoid_height = geoid_src.read(1)
        profile = dem_src.profile
        ellipsoid_height = dem_add_geoid(orthometric_height, geoid_height)
    
    profile.update(dtype=rasterio.float32)
    with rasterio.open(ellipsoid_output_path, 'w', **profile) as dst:
        dst.write(ellipsoid_height.astype(np.float32), 1)

def orthometric2orthometric(orthometric_old_path, geoid_old_path, geoid_new_path, orthometric_new_output_path):
    with rasterio.open(orthometric_old_path) as dem_src, \
         rasterio.open(geoid_old_path) as geoid_old_src, \
         rasterio.open(geoid_new_path) as geoid_new_src:
        
        orthometric_old_height = dem_src.read(1)
        geoid_old_height = geoid_old_src.read(1)
        geoid_new_height = geoid_new_src.read(1)
        profile = dem_src.profile
        ellipsoid_height = dem_add_geoid(orthometric_old_height, geoid_old_height)  # Convert to ellipsoid height
        orthometric_new_height = dem_rem_geoid(ellipsoid_height, geoid_new_height)  # Convert to new orthometric height
    
    profile.update(dtype=rasterio.float32)
    with rasterio.open(orthometric_new_output_path, 'w', **profile) as dst:
        dst.write(orthometric_new_height.astype(np.float32), 1)

# Example usage:
# ellipsoid2orthometric("ellipsoid_dem.tif", "geoid_model.tif", "orthometric_dem.tif")
# orthometric2ellipsoid("orthometric_dem.tif", "geoid_model.tif", "ellipsoid_dem.tif")
# orthometric2orthometric("orthometric_old.tif", "geoid_old.tif", "geoid_new.tif", "orthometric_new.tif")


