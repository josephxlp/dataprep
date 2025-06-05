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
