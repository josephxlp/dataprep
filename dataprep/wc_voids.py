import subprocess
import os 
import time 

def saga_close_gaps_with_spline(
    saga_cmd_path,
    input_grid,
    mask_grid=None,
    output_grid=None,
    max_gap_cells=0,
    max_points=1000,
    local_points=20,
    extended_neighbourhood=False,
    neighbours="Neumann",
    radius=0,
    relaxation=0.0,
    overwrite=False
):
    """
    Run SAGA GIS Close Gaps with Spline tool using saga_cmd via Python subprocess.

    Parameters:
        saga_cmd_path (str): Path to the saga_cmd executable.
        input_grid (str): Path to the input grid file with gaps (no data values).
        mask_grid (str, optional): Path to the mask grid file. Defaults to None.
        output_grid (str, optional): Path to save the output grid with gaps closed. If not provided,
                                     changes will be applied to the original grid.
        max_gap_cells (int, optional): Only process gaps with fewer cells than this value. Ignored if set to 0. Defaults to 0.
        max_points (int, optional): Maximum points used for interpolation. Defaults to 1000.
        local_points (int, optional): Number of points for local interpolation. Defaults to 20.
        extended_neighbourhood (bool, optional): Whether to use an extended neighbourhood. Defaults to False.
        neighbours (str, optional): Neighbourhood type. Options: "Neumann" or "Moore". Defaults to "Neumann".
        radius (int, optional): Radius (in cells) for neighbourhood consideration. Defaults to 0.
        relaxation (float, optional): Relaxation parameter for spline interpolation. Defaults to 0.0.
        overwrite (bool, optional): Whether to overwrite the output file if it already exists. Defaults to False.
    """
    # Check if the output file exists and handle overwrite logic
    if output_grid and os.path.isfile(output_grid):
        if overwrite:
            print(f"Output file '{output_grid}' exists but overwrite is enabled. Proceeding...")
        else:
            print(f"Output file '{output_grid}' already exists and overwrite is disabled. Skipping execution.")
            return

    # Map neighbour options to their corresponding integer values
    neighbour_options = {"Neumann": 0, "Moore": 1}
    if neighbours not in neighbour_options:
        raise ValueError(f"Invalid neighbours option: {neighbours}. Choose from 'Neumann' or 'Moore'.")
    neighbours_value = neighbour_options[neighbours]

    # Construct the command as a list of arguments
    command = [
        saga_cmd_path,
        "grid_tools", "25",  # Tool ID for Close Gaps with Spline
        "-GRID", input_grid,
        "-MAXGAPCELLS", str(max_gap_cells),
        "-MAXPOINTS", str(max_points),
        "-LOCALPOINTS", str(local_points),
        "-EXTENDED", "1" if extended_neighbourhood else "0",
        "-NEIGHBOURS", str(neighbours_value),
        "-RADIUS", str(radius),
        "-RELAXATION", str(relaxation)
    ]

    # Add optional parameters if provided
    if mask_grid:
        command.extend(["-MASK", mask_grid])
    if output_grid:
        command.extend(["-CLOSED", output_grid])

    # Execute the command using subprocess
    try:
        print("Running SAGA GIS Close Gaps with Spline command...")
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Print the output and error (if any)
        print("SAGA GIS Command Output:")
        print(result.stdout)
        if result.stderr:
            print("SAGA GIS Command Errors:")
            print(result.stderr)

    except subprocess.CalledProcessError as e:
        print("An error occurred while running the SAGA GIS Close Gaps with Spline command.")
        print(f"Return Code: {e.returncode}")
        print(f"Error Output: {e.stderr}")

