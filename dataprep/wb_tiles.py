import os
import yaml
from .rgrid import format_tile_fpath, gdal_regrid, get_raster_info
from .rtransforms import scale_raster, raster_calc
from .rgeoid import ellipsoid2orthometric, orthometric2orthometric
from .rfilter import dem_remove_badpixels
from glob import glob


def retile_datasets(
    ds_tiles_dpath, tilename, xmin, ymin, xmax, ymax, xres, yres,
    tdem_dem_fpath, tdem_hem_fpath, tdem_wam_fpath, cdem_wbm_fpath,
    dtm_fpath, pdem_fpath, edem_egm_fpath, edem_wgs_fpath,
    edem_lcm_fpath, esawc_fpath, etchm_fpath, egm08_fpath,
    s1_fpath, s2_fpath, tdem_com_fpath, fbchm_fpath,
    fbcha_fpath, glow_fpath, gtop_fpath, lgeoid_fpath, wsfbh_fpath,
    hem_thr=0.5
):
    tilename_dpath = os.path.join(ds_tiles_dpath, tilename)
    os.makedirs(tilename_dpath, exist_ok=True)
    nmode = "num"
    cmode = "cat"  # check the ones that need this
    ds = {}

    # Check and process dtm_fpath
    if dtm_fpath:
        ldar_tile = format_tile_fpath(tilename_dpath, tilename, dtm_fpath)
        gdal_regrid(dtm_fpath, ldar_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
        ds['ldtm'] = ldar_tile
    else:
        print(f"Skipping dtm processing for tile {tilename}: dtm_fpath is None")

    # Check and process pdem_fpath
    if pdem_fpath:
        pdem_tile = format_tile_fpath(tilename_dpath, tilename, pdem_fpath)
        gdal_regrid(pdem_fpath, pdem_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
        ds['pdem'] = pdem_tile
    else:
        print(f"Skipping pdem processing for tile {tilename}: pdem_fpath is None")

    # Check and process edem_egm_fpath
    if edem_egm_fpath:
        edem_egm_tile = format_tile_fpath(tilename_dpath, tilename, edem_egm_fpath)
        gdal_regrid(edem_egm_fpath, edem_egm_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
        ds['edem_egm'] = edem_egm_tile
    else:
        print(f"Skipping edem_egm processing for tile {tilename}: edem_egm_fpath is None")

    # Check and process edem_wgs_fpath
    if edem_wgs_fpath:
        edem_wgs_tile = format_tile_fpath(tilename_dpath, tilename, edem_wgs_fpath)
        gdal_regrid(edem_wgs_fpath, edem_wgs_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
        ds['edem_wgs'] = edem_wgs_tile
    else:
        print(f"Skipping edem_wgs processing for tile {tilename}: edem_wgs_fpath is None")

    # Check and process egm08_fpath
    if egm08_fpath:
        egm08_tile = format_tile_fpath(tilename_dpath, tilename, egm08_fpath)
        gdal_regrid(egm08_fpath, egm08_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
        ds['egm08'] = egm08_tile
    else:
        print(f"Skipping egm08 processing for tile {tilename}: egm08_fpath is None")

    # Check and process wsfbh_fpath
    if wsfbh_fpath:
        wsfbh_tile = f"{tilename_dpath}/{tilename}_wsfbh.tif"
        gdal_regrid(wsfbh_fpath, wsfbh_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
        ds["wsfbh"] = wsfbh_tile
    else:
        print(f"Skipping wsfbh processing for tile {tilename}: wsfbh_fpath is None")

    # Check and process lgeoid_fpath
    if lgeoid_fpath:
        lgeoid_tile = f"{tilename_dpath}/{tilename}_lgeoid.tif"
        gdal_regrid(lgeoid_fpath, lgeoid_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
        ds["lgeoid"] = lgeoid_tile
    else:
        print(f"Skipping lgeoid processing for tile {tilename}: lgeoid_fpath is None")

    # Check and process gtop_fpath
    if gtop_fpath:
        gtop_tile = f"{tilename_dpath}/{tilename}_geditop.tif"
        gdal_regrid(gtop_fpath, gtop_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
        ds["gtop"] = gtop_tile
    else:
        print(f"Skipping gtop processing for tile {tilename}: gtop_fpath is None")

    # Check and process glow_fpath
    if glow_fpath:
        glow_tile = f"{tilename_dpath}/{tilename}_gedilow.tif"
        gdal_regrid(glow_fpath, glow_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
        ds["glow"] = glow_tile
    else:
        print(f"Skipping glow processing for tile {tilename}: glow_fpath is None")

    # Check and process s1_fpath
    if s1_fpath:
        s1_tile = format_tile_fpath(tilename_dpath, tilename, s1_fpath)
        gdal_regrid(s1_fpath, s1_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
        ds["s1"] = s1_tile
    else:
        print(f"Skipping s1 processing for tile {tilename}: s1_fpath is None")

    # Check and process s2_fpath
    if s2_fpath:
        print(s2_fpath)
        s2_tile = format_tile_fpath(tilename_dpath, tilename, s2_fpath)
        gdal_regrid(s2_fpath, s2_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
        ds["s2"] = s2_tile
    else:
        print(f"Skipping s2 processing for tile {tilename}: s2_fpath is None")

    # Check and process tdem_dem_fpath
    if tdem_dem_fpath:
        tdem_dem_tile = format_tile_fpath(tilename_dpath, tilename, tdem_dem_fpath)
        gdal_regrid(tdem_dem_fpath, tdem_dem_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
        ds["tdem_dem"] = tdem_dem_tile
    else:
        print(f"Skipping tdem_dem processing for tile {tilename}: tdem_dem_fpath is None")

    # Check and process tdem_hem_fpath
    if tdem_hem_fpath:
        tdem_hem_tile = format_tile_fpath(tilename_dpath, tilename, tdem_hem_fpath)
        gdal_regrid(tdem_hem_fpath, tdem_hem_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
        ds["tdem_hem"] = tdem_hem_tile
    else:
        print(f"Skipping tdem_hem processing for tile {tilename}: tdem_hem_fpath is None")

    # Check and process tdem_wam_fpath
    if tdem_wam_fpath:
        tdem_wam_tile = format_tile_fpath(tilename_dpath, tilename, tdem_wam_fpath)
        gdal_regrid(tdem_wam_fpath, tdem_wam_tile, xmin, ymin, xmax, ymax, xres, yres, mode=cmode)
        ds['tdem_wam'] = tdem_wam_tile
    else:
        print(f"Skipping tdem_wam processing for tile {tilename}: tdem_wam_fpath is None")

    # Check and process tdem_com_fpath
    if tdem_com_fpath:
        tdem_com_tile = format_tile_fpath(tilename_dpath, tilename, tdem_com_fpath)
        gdal_regrid(tdem_com_fpath, tdem_com_tile, xmin, ymin, xmax, ymax, xres, yres, mode=cmode)
        ds['tdem_com'] = tdem_com_tile
    else:
        print(f"Skipping tdem_com processing for tile {tilename}: tdem_com_fpath is None")

    # Check and process cdem_wbm_fpath
    if cdem_wbm_fpath:
        cdem_wbm_tile = format_tile_fpath(tilename_dpath, tilename, cdem_wbm_fpath)
        gdal_regrid(cdem_wbm_fpath, cdem_wbm_tile, xmin, ymin, xmax, ymax, xres, yres, mode=cmode)
        ds['cdem_wbm'] = cdem_wbm_tile
    else:
        print(f"Skipping cdem_wbm processing for tile {tilename}: cdem_wbm_fpath is None")

    # Check and process edem_lcm_fpath
    if edem_lcm_fpath:
        edem_lcm_tile = format_tile_fpath(tilename_dpath, tilename, edem_lcm_fpath)
        gdal_regrid(edem_lcm_fpath, edem_lcm_tile, xmin, ymin, xmax, ymax, xres, yres, mode=cmode)
        ds['edem_lcm'] = edem_lcm_tile
    else:
        print(f"Skipping edem_lcm processing for tile {tilename}: edem_lcm_fpath is None")

    # Check and process esawc_fpath
    if esawc_fpath:
        esawc_tile = format_tile_fpath(tilename_dpath, tilename, esawc_fpath)
        gdal_regrid(esawc_fpath, esawc_tile, xmin, ymin, xmax, ymax, xres, yres, mode=cmode)
        ds['esawc'] = esawc_tile
        # Additional processing if esawc_tile was processed
        esawc_tilex = esawc_tile.replace(".tif", "_x.tif")
        scale_raster(esawc_tile, esawc_tilex, method="minmax")
        ds['esawcx'] = esawc_tilex
    else:
        print(f"Skipping esawc processing for tile {tilename}: esawc_fpath is None")

    # Check and process etchm_fpath
    if etchm_fpath:
        etchm_tile = format_tile_fpath(tilename_dpath, tilename, etchm_fpath)
        gdal_regrid(etchm_fpath, etchm_tile, xmin, ymin, xmax, ymax, xres, yres, mode=cmode)
        ds["etchm"] = etchm_tile
    else:
        print(f"Skipping etchm processing for tile {tilename}: etchm_fpath is None")

    # Check and process fbchm_fpath
    if fbchm_fpath:
        fbchm_tile = format_tile_fpath(tilename_dpath, tilename, fbchm_fpath)
        gdal_regrid(fbchm_fpath, fbchm_tile, xmin, ymin, xmax, ymax, xres, yres, mode=cmode)
        ds["fbchm"] = fbchm_tile
    else:
        print(f"Skipping fbchm processing for tile {tilename}: fbchm_fpath is None")

    # Check and process fbcha_fpath
    if fbcha_fpath:
        fbcha_tile = format_tile_fpath(tilename_dpath, tilename, fbcha_fpath)
        gdal_regrid(fbcha_fpath, fbcha_tile, xmin, ymin, xmax, ymax, xres, yres, mode=cmode)
        ds["fbcha"] = fbcha_tile
    else:
        print(f"Skipping fbcha processing for tile {tilename}: fbcha_fpath is None")

    ####################################################################
    ##################### GEOID TRANFORMS
    ####################################################################
    # Only run if required paths are present
    if tdem_dem_fpath and egm08_fpath and 'tdem_dem' in ds and 'egm08' in ds:
        tdem_dem_tile_egm = ds['tdem_dem'].replace(".tif", "_egm.tif")
        if not os.path.isfile(tdem_dem_tile_egm):
            ellipsoid2orthometric(ds['tdem_dem'], ds['egm08'], tdem_dem_tile_egm)
        ds["tdem_egm"] = tdem_dem_tile_egm
    else:
        print(f"Skipping tdem_egm transformation for tile {tilename}: Missing required paths.")

    if pdem_fpath and lgeoid_fpath and egm08_fpath and 'pdem' in ds and 'lgeoid' in ds and 'egm08' in ds:
        pdem_tile_egm = ds['pdem'].replace(".tif", "_egm.tif")
        if not os.path.isfile(pdem_tile_egm):
            orthometric2orthometric(ds['pdem'], ds['lgeoid'], ds['egm08'], pdem_tile_egm)
        ds["pdem_egm"] = pdem_tile_egm
    else:
        print(f"Skipping pdem_egm transformation for tile {tilename}: Missing required paths.")

    if dtm_fpath and lgeoid_fpath and egm08_fpath and 'ldtm' in ds and 'lgeoid' in ds and 'egm08' in ds:
        ldem_tile_egm = ds['ldtm'].replace(".tif", "_egm.tif")
        if not os.path.isfile(ldem_tile_egm):
            orthometric2orthometric(ds['ldtm'], ds['lgeoid'], ds['egm08'], ldem_tile_egm)
        ds["ldem_egm"] = ldem_tile_egm
    else:
        print(f"Skipping ldem_egm transformation for tile {tilename}: Missing required paths.")


    ####################################################################
    ##################### BAD PIXEL REMOVAL
    ####################################################################

    if 'tdem_egm' in ds and 'tdem_hem' in ds and 'esawc' in ds and 'tdem_com' in ds:
        tdem_void_tile = ds['tdem_egm'].replace(".tif", "_v.tif")
        
        dem_remove_badpixels(ds['tdem_egm'], ds['tdem_hem'], ds['esawc'], ds['tdem_com'], 
                             tdem_void_tile,hem_thr)
        ds["tdem_egm_void"] = tdem_void_tile
    else:
        print(f"Skipping bad pixel removal for tile {tilename}: Missing required datasets.")

    remove_auxfiles(tilename_dpath)


def remove_aux_tifs(filelist):
    print(f"{len(filelist)}")
    for f in filelist:
        delete_file(f)

def delete_file(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)

def remove_auxfiles(tilename_dpath):
    fs = glob(f"{tilename_dpath}/*.aux.xml")
    print(f"{len(fs)}")
    for f in fs:
        delete_file(f)

def write_yaml(yaml_data, yaml_file_path):
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(yaml_data, yaml_file)
    print('write_yaml')

def read_yaml(filename):
    with open(filename, 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)
        print('read_yaml')
        return yaml_data


def get_tilename_from_tdem_basename(fpath):
    return os.path.basename(fpath).split('_')[4]

def process_tile(
    basefile, ds_tiles_dpath,
    tdem_dem_fpath, tdem_hem_fpath, tdem_wam_fpath, cdem_wbm_fpath,
    dtm_fpath, pdem_fpath, edem_egm_fpath, edem_wgs_fpath,
    edem_lcm_fpath, esawc_fpath, etchm_fpath, egm08_fpath,
    s1_fpath, s2_fpath, tdem_com_fpath, fbchm_fpath,
    fbcha_fpath, glow_fpath, gtop_fpath, lgeoid_fpath, wsfbh_fpath,
    hem_thr
):
    tilename = get_tilename_from_tdem_basename(basefile)
    print(os.path.basename(basefile))
    print(tilename)
    tilename_dpath = os.path.join(ds_tiles_dpath, tilename)
    os.makedirs(tilename_dpath, exist_ok=True)

    # Get raster info from basefile (assuming basefile is always present)
    proj, xres, yres, xmin, xmax, ymin, ymax, w, h = get_raster_info(basefile)

    retile_datasets(
        ds_tiles_dpath, tilename, xmin, ymin, xmax, ymax, xres, yres,
        tdem_dem_fpath, tdem_hem_fpath, tdem_wam_fpath, cdem_wbm_fpath,
        dtm_fpath, pdem_fpath, edem_egm_fpath, edem_wgs_fpath,
        edem_lcm_fpath, esawc_fpath, etchm_fpath, egm08_fpath,
        s1_fpath, s2_fpath, tdem_com_fpath, fbchm_fpath,
        fbcha_fpath, glow_fpath, gtop_fpath, lgeoid_fpath, wsfbh_fpath,
        hem_thr
    )