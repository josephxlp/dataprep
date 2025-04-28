import os 
import yaml
from .rgrid import format_tile_fpath, gdal_regrid, get_raster_info
from .rtransforms import scale_raster,raster_calc
from .rgeoid import ellipsoid2orthometric,orthometric2orthometric
from .rfilter import dem_remove_badpixels
from glob import glob 


def retile_datasets(
    ds_tiles_dpath, tilename, xmin, ymin, xmax, ymax, xres, yres,
    tdem_dem_fpath, tdem_hem_fpath, tdem_wam_fpath, cdem_wbm_fpath,
    dtm_fpath, pdem_fpath, edem_egm_fpath, edem_wgs_fpath,
    edem_lcm_fpath, esawc_fpath, etchm_fpath, egm08_fpath,
    s1_fpath,s2_fpath,tdem_com_fpath,fbchm_fpath,
    fbcha_fpath,glow_fpath,gtop_fpath,lgeoid_fpath,wsfbh_fpath
):
    tilename_dpath = os.path.join(ds_tiles_dpath, tilename)
    os.makedirs(tilename_dpath,exist_ok=True)
    nmode = "num" 
    cmode = "cat" # check the ones that need this 
    ds = {}


    ldar_tile = format_tile_fpath(tilename_dpath, tilename, dtm_fpath)
    gdal_regrid(dtm_fpath, ldar_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
    ds['ldtm'] = ldar_tile

    pdem_tile = format_tile_fpath(tilename_dpath, tilename, pdem_fpath)
    gdal_regrid(pdem_fpath, pdem_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
    ds['pdem'] = pdem_tile

    # cdem_dem_tile = format_tile_fpath(tilename_dpath, tilename, cdem_dem_fpath)
    # gdal_regrid(cdem_dem_fpath, cdem_dem_tile, xmin, ymin, xmax, ymax, xres, yres, mode='num')
    # ds['cdem_dem'] = cdem_dem_tile

    edem_egm_tile = format_tile_fpath(tilename_dpath, tilename, edem_egm_fpath)
    gdal_regrid(edem_egm_fpath, edem_egm_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
    ds['edem_egm'] = edem_egm_tile

    edem_wgs_tile = format_tile_fpath(tilename_dpath, tilename, edem_wgs_fpath)
    gdal_regrid(edem_wgs_fpath, edem_wgs_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
    ds['edem_wgs'] = edem_wgs_tile

    egm08_tile = format_tile_fpath(tilename_dpath, tilename, egm08_fpath)
    gdal_regrid(egm08_fpath, egm08_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
    ds['egm08'] = egm08_tile

    wsfbh_tile = f"{tilename_dpath}/{tilename}_wsfbh.tif"
    gdal_regrid(wsfbh_fpath, wsfbh_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
    ds["wsfbh"] = wsfbh_tile

    lgeoid_tile = f"{tilename_dpath}/{tilename}_lgeoid.tif"
    gdal_regrid(lgeoid_fpath, lgeoid_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
    ds["lgeoid"] = lgeoid_tile

    gtop_tile = f"{tilename_dpath}/{tilename}_geditop.tif"
    gdal_regrid(gtop_fpath, gtop_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
    ds["gtop"] = gtop_tile

    glow_tile = f"{tilename_dpath}/{tilename}_gedilow.tif"
    gdal_regrid(glow_fpath, glow_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
    ds["glow"] = glow_tile

    s1_tile = format_tile_fpath(tilename_dpath, tilename, s1_fpath)
    gdal_regrid(s1_fpath, s1_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
    ds["s1"] = s1_tile
    
    print(s2_fpath)
    s2_tile = format_tile_fpath(tilename_dpath, tilename, s2_fpath)
    gdal_regrid(s2_fpath, s2_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
    ds["s2"] = s2_tile

    tdem_dem_tile = format_tile_fpath(tilename_dpath, tilename, tdem_dem_fpath)
    gdal_regrid(tdem_dem_fpath, tdem_dem_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
    ds["tdem_dem"] = tdem_dem_tile

    tdem_hem_tile = format_tile_fpath(tilename_dpath, tilename, tdem_hem_fpath)
    gdal_regrid(tdem_hem_fpath, tdem_hem_tile, xmin, ymin, xmax, ymax, xres, yres, mode=nmode)
    ds["tdem_hem"] = tdem_hem_tile

    tdem_wam_tile = format_tile_fpath(tilename_dpath, tilename, tdem_wam_fpath)
    gdal_regrid(tdem_wam_fpath, tdem_wam_tile, xmin, ymin, xmax, ymax, xres, yres, mode=cmode)
    ds['tdem_wam'] = tdem_wam_tile

    tdem_com_tile = format_tile_fpath(tilename_dpath, tilename, tdem_com_fpath)
    gdal_regrid(tdem_com_fpath, tdem_com_tile, xmin, ymin, xmax, ymax, xres, yres, mode=cmode)
    ds['tdem_com'] = tdem_com_tile

    cdem_wbm_tile = format_tile_fpath(tilename_dpath, tilename, cdem_wbm_fpath)
    gdal_regrid(cdem_wbm_fpath, cdem_wbm_tile, xmin, ymin, xmax, ymax, xres, yres,mode=cmode)
    ds['cdem_wbm'] = cdem_wbm_tile

    edem_lcm_tile = format_tile_fpath(tilename_dpath, tilename, edem_lcm_fpath)
    gdal_regrid(edem_lcm_fpath, edem_lcm_tile, xmin, ymin, xmax, ymax, xres, yres, mode=cmode)
    ds['edem_lcm'] = edem_lcm_tile

    esawc_tile = format_tile_fpath(tilename_dpath, tilename, esawc_fpath)
    gdal_regrid(esawc_fpath, esawc_tile, xmin, ymin, xmax, ymax, xres, yres,mode=cmode)
    ds['esawc'] = esawc_tile

    esawc_tilex = esawc_tile.replace(".tif", "_x.tif")
    scale_raster(esawc_tile, esawc_tilex, method="minmax")
    ds['esawcx'] = esawc_tilex

    etchm_tile = format_tile_fpath(tilename_dpath, tilename, etchm_fpath)
    gdal_regrid(etchm_fpath, etchm_tile, xmin, ymin, xmax, ymax, xres, yres,mode=cmode)
    ds["etchm"] = etchm_tile

    fbchm_tile = format_tile_fpath(tilename_dpath, tilename, fbchm_fpath)
    gdal_regrid(fbchm_fpath, fbchm_tile, xmin, ymin, xmax, ymax, xres, yres, mode=cmode)
    ds["fbchm"] = fbchm_tile

    fbcha_tile = format_tile_fpath(tilename_dpath, tilename, fbcha_fpath)
    gdal_regrid(fbcha_fpath, fbcha_tile, xmin, ymin, xmax, ymax, xres, yres, mode=cmode)
    ds["fbcha"] = fbcha_tile
    

    ####################################################################
    ##################### GEOID TRANFORMS
    ####################################################################
    #ellipsoid2orthometric,orthometric2orthometric

    tdem_dem_tile_egm = tdem_dem_tile.replace(".tif", "_egm.tif")
    if not os.path.isfile(tdem_dem_tile_egm):
        ellipsoid2orthometric(tdem_dem_tile, egm08_tile, tdem_dem_tile_egm)
    ds["tdem_egm"] = tdem_dem_tile_egm

     # do pdem, ldem to egm

    pdem_tile_egm = pdem_tile.replace(".tif", "_egm.tif")
    if not os.path.isfile(pdem_tile_egm):
        orthometric2orthometric(pdem_tile, lgeoid_tile, egm08_tile,pdem_tile_egm)

    ds["pdem_egm"] = tdem_dem_tile_egm

    ldem_tile_egm = ldar_tile.replace(".tif", "_egm.tif")
    if not os.path.isfile(pdem_tile_egm):
        orthometric2orthometric(ldar_tile, lgeoid_tile, egm08_tile,ldem_tile_egm)

    ds["ldem_egm"] = ldem_tile_egm
    #orthometric2orthometric

    ####################################################################
    ##################### BAD PIXEL REMOVAL 
    ####################################################################

    tdem_void_tile = tdem_dem_tile_egm.replace(".tif", "_void.tif")
    dem_remove_badpixels(tdem_dem_tile_egm,tdem_hem_tile, esawc_tile,tdem_com_tile,tdem_void_tile)
    ds["tdem_egm_void"] = tdem_void_tile

    
    
    # # add if already exist 
    # wbm_lwm_fn = cdem_wbm_tile.replace('cdem_WBM.tif', 'cdem_WBM_LWM.tif')
    # esa_lwm_fn = esawc_tile.replace('_multi_ESAWC.tif', '_ESAWC_LWM.tif')
    # lwm_a_fn = edem_lcm_tile.replace('.tif', '_LWM_A.tif')
    # lwm_b_fn = edem_lcm_tile.replace('.tif', '_LWM_B.tif')
    # fdem_file = tdem_dem_tile.replace('.tif', '_F.tif')
    # mask_file = tdem_dem_tile.replace('.tif', '_M.tif')

    # dem_fw = fdem_file.replace('F.tif', '_Fw.tif')
    # dem_mw = mask_file.replace('M.tif', '_Mw.tif')


    # if not os.path.isfile(wbm_lwm_fn): classify_lwm_CopWBM(cdem_wbm_tile, wbm_lwm_fn)
    # ds['cdem_wbm'] = wbm_lwm_fn

    
    # if not os.path.isfile(esa_lwm_fn): classify_lwm_ESAWC(esawc_tile, esa_lwm_fn,water_code=80)
    # ds['esawc_lwm'] = esa_lwm_fn
 
    
    # if not os.path.isfile(lwm_a_fn): classify_lwm_TanDEMX_LCM(edem_lcm_tile,lwm_a_fn,lwm_b_fn)
    # #elcm_fna, elcm_fnb = classify_lwm_TanDEMX_LCM(edem_lcm_tile,lwm_a_fn,lwm_b_fn)

    # ds['edem_lcm_lwma'] = lwm_a_fn
    # ds['edem_lcm_lwmb'] = lwm_b_fn
    #lcm_lwm_fn = lwm_a_fn

    

    # if not os.path.isfile(dem_fw):
    #     fdem_file, mask_file = filter_tandemx_noise(tdem_dem_tile, 
    #                                                 tdem_hem_tile, 
    #                                                 tdem_com_tile, 
    #                                                 n_iter=1)  
    # if not os.path.isfile(dem_fw):
    #     filter_water(fdem_file, mask_file, lcm_lwm_fn, esa_lwm_fn, wbm_lwm_fn)

    # ds['tdem_dem_fw'] = dem_fw
    # ds['tdem_dem_mw'] = dem_mw

    

    #tname = os.path.basename(lcm_lwm_fn).split('_')[0]
    #combined_mask_file = os.path.join(os.path.dirname(lcm_lwm_fn), f'{tname}_LWM.tif')
    # if not os.path.isfile(combined_mask_file):
    #     combined_mask_file = combine_water_masks(lcm_lwm_fn, esa_lwm_fn, wbm_lwm_fn)
    # ds['lwm'] = combined_mask_file

    
    ####################################################################
    ###################################################################

    ####################################################################
    ######### EXTRACT AND SHIFT GEOID EGM08
    ####################################################################
    #edem_geoid_tile = f'{tilename_dpath}/{tilename}_EDEM_GEOID.tif'
    # raster_calc(edem_egm_tile, edem_wgs_tile, "subtract", edem_geoid_tile)
    # ds['edem_goid'] = edem_geoid_tile

    # egm08p_tile = f'{tilename_dpath}/{tilename}_EGM08p.tif'
    # ds['egm08p'] = egm08p_tile

    # yaml_tile = os.path.join(tilename_dpath, f'{tilename}_ds.yaml')
    # write_yaml(ds, yaml_tile)
    # print('yaml_tile:', yaml_tile)

    
    
    # filelist = [edem_geoid_tile, lwm_b_fn,lwm_a_fn,wbm_lwm_fn,esa_lwm_fn,
    #             fdem_file, mask_file,dem_mw,dem_fw,edem_geoid_tile,
    #             combined_mask_file]
    # filelist = [edem_geoid_tile, lwm_b_fn,lwm_a_fn,wbm_lwm_fn,esa_lwm_fn,
    #             fdem_file, mask_file,dem_mw,dem_fw,combined_mask_file]
    remove_auxfiles(tilename_dpath)
    #remove_aux_tifs(filelist)


   



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
    s1_fpath,s2_fpath,tdem_com_fpath,fbchm_fpath,
    fbcha_fpath,glow_fpath,gtop_fpath,lgeoid_fpath,wsfbh_fpath
):
    tilename = get_tilename_from_tdem_basename(basefile)
    print(os.path.basename(basefile))
    print(tilename)
    tilename_dpath = os.path.join(ds_tiles_dpath, tilename)
    os.makedirs(tilename_dpath,exist_ok=True)
    tile_fpath = format_tile_fpath(tilename_dpath, tilename, tdem_dem_fpath) 
    proj, xres, yres, xmin, xmax, ymin, ymax, w, h = get_raster_info(basefile)
    #print('dst size:', w, h)
    retile_datasets(
        ds_tiles_dpath, tilename, xmin, ymin, xmax, ymax, xres, yres,
        tdem_dem_fpath, tdem_hem_fpath, tdem_wam_fpath, cdem_wbm_fpath,
        dtm_fpath, pdem_fpath, edem_egm_fpath, edem_wgs_fpath,
        edem_lcm_fpath, esawc_fpath, etchm_fpath, egm08_fpath,
        s1_fpath,s2_fpath,tdem_com_fpath,fbchm_fpath,
        fbcha_fpath,glow_fpath,gtop_fpath,lgeoid_fpath,wsfbh_fpath
    )

    
    