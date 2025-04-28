saga_cmd_path = "/usr/bin/saga_cmd"
from src.uc_voids import saga_close_gaps_with_spline


fi = tdem_fi = "/media/ljp238/12TBWolf/BRCHIEVE/TILES12/N09E105/N09E105_tdem_dem__Fw.tif"

fo = tdem_fo = "/media/ljp238/12TBWolf/BRCHIEVE/TILES12/N09E105/N09E105_tdem_dem__vfill.tif"

saga_close_gaps_with_spline(
    saga_cmd_path=saga_cmd_path,
    input_grid=fi,
    output_grid=fo,
    max_gap_cells=1000,        # Process gaps up to 1000 cells
    max_points=5000,           # Use up to 5000 points for interpolation
    local_points=50,           # Consider 50 local points
    extended_neighbourhood=True,  # Use extended neighborhood
    neighbours="Moore",        # Use 8 neighbors
    radius=10,                 # Expand search radius
    relaxation=0.1,            # Moderate relaxation
    overwrite=True             # Overwrite existing files
)