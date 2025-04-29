import os 
import subprocess
from glob import glob
import time 
import yaml 
from os.path import join,isfile, exists


def create_text_file(key, files, output_dir, overwrite=False):
    """Create a text file listing the raster file paths."""
    txt_path = join(output_dir, f"{key}.txt")
    
    if isfile(txt_path) and overwrite is False:
        print(f"[SKIP] Text file already exists: {txt_path}")
        return txt_path

    with open(txt_path, "w") as txt_file:
        txt_file.write("\n".join(files) + "\n")
    
    print(f"[INFO] Created text file: {txt_path}")
    return txt_path

def create_vrt_file(key, txt_path, output_dir,epsg="4749",overwrite=False):
    """Create a VRT file using gdalbuildvrt."""
    vrt_path = join(output_dir, f"{key}.vrt")

    if isfile(vrt_path) and overwrite is False:
        print(f"[SKIP] VRT file already exists: {vrt_path}")
        return vrt_path

    if epsg is None:
        cmd = ["gdalbuildvrt", "-input_file_list", txt_path, vrt_path]
    else:
        cmd = ["gdalbuildvrt", "-a_srs", f"EPSG:{epsg}", "-input_file_list", txt_path, vrt_path]

    try:
        subprocess.run(cmd, check=True)
        print(f"[INFO] Created VRT file: {vrt_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error: gdalbuildvrt failed with error code {e.returncode}")
    return vrt_path

def save_yaml(data, file_path):
    """Save dictionary data to a YAML file.""" # add overwrite
    #if not exists(file_path) and overwrite is False:
    with open(file_path, "w") as file:
        yaml.dump(data, file, default_flow_style=False,allow_unicode=True)

def print_file_length(dt,key):
    print(f"{key} {len(dt[key])} files")

def loadfiles_byvariable(archieve_dpath, outdir):
    os.makedirs(outdir, exist_ok=True)
    ti = time.perf_counter()
    ds = {}
    ds["tdem_dem"] = glob(f"{archieve_dpath}/TDEMX/*/DEM/*_DEM.tif")
    ds["tdem_wam"] = glob(f"{archieve_dpath}/TDEMX/*/AUXFILES/*WAM.tif")
    ds["tdem_lsm"] = glob(f"{archieve_dpath}/TDEMX/*/AUXFILES/*LSM.tif")
    ds["tdem_hem"] = glob(f"{archieve_dpath}/TDEMX/*/AUXFILES/*HEM.tif")
    ds["tdem_cov"] = glob(f"{archieve_dpath}/TDEMX/*/AUXFILES/*COV.tif")
    ds["tdem_com"] = glob(f"{archieve_dpath}/TDEMX/*/AUXFILES/*COM.tif")
    print_file_length(ds,"tdem_dem")
    print_file_length(ds,"tdem_wam")
    print_file_length(ds,"tdem_hem")
    print_file_length(ds,"tdem_cov")
    print_file_length(ds,"tdem_com")
    ds["edem_wgs"] = glob(f"{archieve_dpath}/EDEMx/TILES/comprexn/*/EDEM/*_EDEM_W84.tif")
    ds["edem_egm"] = glob(f"{archieve_dpath}/EDEMx/TILES/comprexn/*/EDEM/*_EDEM_EGM.tif")
    ds["edem_lcm"] = glob(f"{archieve_dpath}/EDEMx/TILES/comprexn/*/EDEM_AUXFILES/*LCM.tif")
    ds["edem_hem"] = glob(f"{archieve_dpath}/EDEMx/TILES/comprexn/*/EDEM_AUXFILES/*HEM.tif")
    ds["edem_edm"] = glob(f"{archieve_dpath}/EDEMx/TILES/comprexn/*/EDEM_AUXFILES/*EDM.tif")
    print_file_length(ds,"edem_wgs")
    print_file_length(ds,"edem_egm")
    print_file_length(ds,"edem_lcm")
    print_file_length(ds,"edem_hem")
    print_file_length(ds,"edem_edm")


    ds["wsfbh"] = [f"{archieve_dpath}/WSF3D/data/WSFBH/WSF3D_V02_BuildingHeight.tif"]
    ds["pdem"] = [f"{archieve_dpath}/PBAND_DTM/RNG/NegroAOITDX08.tif"]
    ds["egm08"] = [f"{archieve_dpath}/GEOID/GLOBAL/us_nga_egm2008_1.tif"]
    ds["etchm"] = glob(f"{archieve_dpath}/ETH_CHM/data/*/*/*.tif")
    ds["esawc"] = glob(f"{archieve_dpath}/ESAWC/data/v200/2021/map_tiled/*/*.tif")
    

    print_file_length(ds,"wsfbh")
    print_file_length(ds,"pdem")
    print_file_length(ds,"egm08")
    print_file_length(ds,"esawc") 
    print_file_length(ds,"etchm") 
     

    ds["gedi_dtm"] = [f"{archieve_dpath}/GEDI/GRID/comprexn/GEDI_L3_be/GEDI03_elev_lowestmode_mean_2019108_2022019_002_03_EPSG4326.tif"]
    ds["gedi_dsm"] = [f"{archieve_dpath}/GEDI/GRID/comprexn/GEDI_L3_vh/GEDI03_rh100_mean_2019108_2022019_002_03_EPSG4326.tif"]
    ds["cdem_wbm"] = glob(f"{archieve_dpath}/CDEM/WBM/wbm_auto/*/*/*WBM.tif")
    print_file_length(ds,"gedi_dtm")
    print_file_length(ds,"gedi_dsm")
    print_file_length(ds,"cdem_wbm")
                        
    ds["ldem"] = glob(f"{archieve_dpath}/LIDAR_DTM/reproj/*.tif"); # fix heeterogeous stuff AMZ

    ds["s2"] = glob(f"{archieve_dpath}/S2/comprexn/*/*.tif") 
    ds["s1"] = glob(f"{archieve_dpath}/S1/comprexn/*/*.tif")
    print_file_length(ds,"ldem")
    print_file_length(ds,"s2")
    print_file_length(ds,"s1")
    # glob(f"{archieve_dpath}/S1/comprexn/*/*.tif")[0]

    ds["lgeoid"] = glob(f"{archieve_dpath}/GEOID/ROI/REPROJ/*.tif") # reproject this first to epsg 4326
    print_file_length(ds,"lgeoid")

    ds["fbchm"] = glob(f"{archieve_dpath}/FB_CHM/RESAMPLE/sorted_files/*/*maskednearest.tif") # only mekong for now
    ds["fbcha"] = glob(f"{archieve_dpath}/FB_CHM/RESAMPLE/sorted_files/*/*nearest.tif")
    print_file_length(ds,"fbchm")
    print_file_length(ds,"fbcha")

    yaml_filename = join(outdir,"loadfiles_byvariable.yaml")
    save_yaml(data=ds, file_path=yaml_filename)
    tf = time.perf_counter() - ti 
    print(f"loadfiles_byvariable @{tf/60} min(s)")
    return ds, yaml_filename
