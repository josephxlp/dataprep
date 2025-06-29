import os
import time
import multiprocessing
from config.uvars import brchieve_dpath12, vars_name_path_fn, files_byvariable_fn
from dataprep.wb_tiles import process_tile
from dataprep.rutils import read_yaml

#hem_thr = 0.001#0.2#0.5#0.7#1#1.2#1.5#2  # Threshold for HEM processing, can be adjusted as needed
#[6,7,8,9,10,11,12]:#[0.001, 0.2, 0.5, 0.7, 1, 1.2, 1.5, 2,2.5,3,3.5,4,4.5,5]:
#[3,6] 
if __name__ == "__main__":
    ta = time.perf_counter()
  

    for hem_thr in [3]:
        ti = time.perf_counter()
        print(files_byvariable_fn)
        print(vars_name_path_fn)
        bpaths = read_yaml(files_byvariable_fn)
        gpaths = read_yaml(vars_name_path_fn)
        os.makedirs(brchieve_dpath12, exist_ok=True)
        os.chdir(brchieve_dpath12)

        basefiles = bpaths["tdem_dem"]
        print(f"basefiles: {len(basefiles)}")

        # Assign paths, allowing None if not found in gpaths
        tdem_dem_fpath = gpaths.get("tdem_dem")
        tdem_hem_fpath = gpaths.get("tdem_hem")
        tdem_wam_fpath = gpaths.get("tdem_wam")
        tdem_com_fpath = gpaths.get("tdem_com")

        dtm_fpath = gpaths.get("ldem")
        pdem_fpath = gpaths.get("pdem")
        edem_egm_fpath = gpaths.get("edem_egm")
        edem_wgs_fpath = gpaths.get("edem_wgs")
        edem_lcm_fpath = gpaths.get("edem_lcm")

        esawc_fpath = gpaths.get("esawc")
        etchm_fpath = gpaths.get("etchm")
        cdem_wbm_fpath = gpaths.get("cdem_wbm")

        egm08_fpath = gpaths.get("egm08")
        lgeoid_fpath = gpaths.get("lgeoid")

        
        s1_fpath = gpaths.get("s1")
        s2_fpath = gpaths.get("s2")
        fbchm_fpath = None #gpaths.get("fbchm")
        fbcha_fpath = None #gpaths.get("fbcha")
        
        glow_fpath = None #gpaths.get("gedi_dtm")
        gtop_fpath = None #gpaths.get("gedi_dsm")
        wsfbh_fpath = None #gpaths.get("wsfbh")

        num_processes = int(multiprocessing.cpu_count() * 0.75)
        pool = multiprocessing.Pool(processes=num_processes)

        # The 'vars' tuple is not directly used for the function call, but it's fine to keep it.
        # The individual fpath variables are passed directly to process_tile.
        vars = (tdem_dem_fpath, tdem_hem_fpath, tdem_wam_fpath, cdem_wbm_fpath, cdem_wbm_fpath,
                dtm_fpath, pdem_fpath, edem_egm_fpath, edem_wgs_fpath, edem_lcm_fpath,
                esawc_fpath, etchm_fpath, etchm_fpath, egm08_fpath, s1_fpath, s2_fpath,
                tdem_com_fpath, fbchm_fpath, fbcha_fpath, glow_fpath, gtop_fpath, lgeoid_fpath,
                wsfbh_fpath)

        for i, basefile in enumerate(basefiles):
            print(f"{i}/{len(basefiles)} @{basefile}")
            pool.apply_async(
                process_tile, (basefile, brchieve_dpath12,
                                tdem_dem_fpath, tdem_hem_fpath, tdem_wam_fpath, cdem_wbm_fpath,
                                dtm_fpath, pdem_fpath, edem_egm_fpath, edem_wgs_fpath,
                                edem_lcm_fpath, esawc_fpath, etchm_fpath, egm08_fpath,
                                s1_fpath, s2_fpath, tdem_com_fpath, fbchm_fpath,
                                fbcha_fpath, glow_fpath, gtop_fpath, lgeoid_fpath, wsfbh_fpath,
                                hem_thr)
            )
        pool.close()
        pool.join()

        # for i, basefile in enumerate(basefiles):
        #     print(f"{i}/{len(basefiles)} @{basefile}")
        #     if i > 0 : break
        
        #     process_tile(basefile, brchieve_dpath12,
        #                         tdem_dem_fpath, tdem_hem_fpath, tdem_wam_fpath, cdem_wbm_fpath,
        #                         dtm_fpath, pdem_fpath, edem_egm_fpath, edem_wgs_fpath,
        #                         edem_lcm_fpath, esawc_fpath, etchm_fpath, egm08_fpath,
        #                         s1_fpath, s2_fpath, tdem_com_fpath, fbchm_fpath,
        #                         fbcha_fpath, glow_fpath, gtop_fpath, lgeoid_fpath, wsfbh_fpath)

        print("All tasks completed")
        tf = time.perf_counter() - ti
        print(f'run.time: {tf/60} min(s)')

    ta = time.perf_counter() - ta
    print(f'Total run time: {ta/60} min(s)')
    print("Done")
    #os.system("sync")