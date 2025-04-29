import os
import time
from multiprocessing import Pool
from dataprep.wa_vrts import loadfiles_byvariable, save_yaml, create_vrt_file, create_text_file
from config.uvars import archieve_dpath, outdir

def process_key(key_files):
    key, files = key_files
    outdpath = os.path.join(outdir, key)
    os.makedirs(outdpath, exist_ok=True)

    print(f"Processing '{key}': {len(files)} file(s)")
    
    txt_path = create_text_file(key, files, outdpath, overwrite=True)
    vrt_path = create_vrt_file(key, txt_path, outdpath, epsg="4749", overwrite=False)

    return key, txt_path, vrt_path

def main():
    # outdir
    start_time = time.perf_counter()
    
    ds, _ = loadfiles_byvariable(archieve_dpath, outdir)

    cpu_count = 10
    d_txt, d_vrt = {}, {}

    with Pool(cpu_count) as pool:
        results = pool.map(process_key, ds.items())

    for key, txt_path, vrt_path in results:
        d_txt[key] = txt_path
        d_vrt[key] = vrt_path

    save_yaml(data=d_txt, file_path=os.path.join(outdir, "vars_txts.yaml"))
    save_yaml(data=d_vrt, file_path=os.path.join(outdir, "vars_vrts.yaml"))
    
    elapsed_minutes = (time.perf_counter() - start_time) / 60
    print(f"Finished loadfiles_byvariable in {elapsed_minutes:.2f} minute(s)")

if __name__ == "__main__":
    main()

import os 
from dataprep.wa_vrts import (loadfiles_byvariable,save_yaml,
                         create_vrt_file,create_text_file)
from config.uvars import archieve_dpath,outdir
from multiprocessing import Pool
import time 


ti = time.perf_counter()
#outdir = outdir+"V2"
ds, ds_yaml = loadfiles_byvariable(archieve_dpath, outdir)

d1, d2 = {}, {}

def process_key(key):
    outdpath = os.path.join(outdir, key)
    os.makedirs(outdpath, exist_ok=True)
    
    txt_path = os.path.join(outdpath, f"{key}.txt")
    files = ds[key]
    
    print(f"{key} {len(files)} tif files")
    
    txt_path = create_text_file(key, files, outdpath, overwrite=True)
    vrt_path = create_vrt_file(key, txt_path, outdpath, epsg="4749", overwrite=False)
    
    return key, txt_path, vrt_path

cpu = 10
# Use Pool to parallelize the process
with Pool() as pool:
    results = pool.map(process_key, ds.keys())

for key, txt_path, vrt_path in results:
    d1[key] = txt_path
    d2[key] = vrt_path

vars_vrts_yaml = os.path.join(outdir, "vars_vrts.yaml")
vars_txts_yaml = os.path.join(outdir, "vars_txts.yaml")

save_yaml(data=d1, file_path=vars_vrts_yaml)
save_yaml(data=d2, file_path=vars_txts_yaml)
tf = time.perf_counter() - ti 
print(f"loadfiles_byvariable @{tf/60} min(s)")

