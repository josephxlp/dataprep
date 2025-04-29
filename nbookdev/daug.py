import os
import shutil
import rasterio
from rasterio.windows import from_bounds


def daug_isolate_data_by_bbox(tls_fn, vrt_files, temp_dir):
    """
    Reads data from VRT files, aligning their spatial information and pixel counts
    with a GeoTIFF file, and saves the extracted data as new GeoTIFF files.

    Args:
        tls_fn (str): Path to the reference GeoTIFF file.
        vrt_files (list): List of paths to the VRT files to process.
        temp_dir (str): Path to the directory where the output GeoTIFF files will be saved.
    """
    # Ensure the output directory exists
    os.makedirs(temp_dir, exist_ok=True)
    ylist, nlist = [],[]

    try:
        # Open the reference GeoTIFF file to get spatial information
        with rasterio.open(tls_fn) as tls_dataset:
            # Get the bounding box, transform, width, and height of the reference GeoTIFF
            bbox = tls_dataset.bounds
            transform = tls_dataset.transform
            out_width = tls_dataset.width
            out_height = tls_dataset.height
            print(f"Reference GeoTIFF: {tls_fn}")
            print(f"  Bounding box: {bbox}")
            print(f"  Transform: {transform}")
            print(f"  Width: {out_width}, Height: {out_height}")

            # Process each VRT file
            for vrt_file in vrt_files:
                try:
                    # Open the VRT file
                    with rasterio.open(vrt_file) as vrt_dataset:
                        print(f"\nProcessing {vrt_file}...")

                        # Calculate the window based on the bounding box and transform of the reference GeoTIFF
                        window = from_bounds(bbox.left, bbox.bottom, bbox.right, bbox.top, vrt_dataset.transform)

                        # Read the data within the calculated window
                        # Specify the desired output shape to ensure alignment
                        try:
                            data = vrt_dataset.read(window=window, out_shape=(vrt_dataset.count, out_height, out_width))
                        except ValueError as e:
                            print(f"  Error reading data from {vrt_file} within the window: {e}")
                            print("  This might indicate a significant spatial mismatch.")
                            data = None

                        if data is not None:
                            # Update the metadata for the output GeoTIFF file
                            out_meta = vrt_dataset.meta.copy()
                            out_meta.update({
                                "driver": "GTiff",
                                "height": out_height,
                                "width": out_width,
                                "transform": transform,
                                "dtype": data.dtype,
                            })

                            # Check for valid dimensions before writing
                            if out_height > 0 and out_width > 0:
                                # Create the output file name
                                output_filename = os.path.join(temp_dir, f"aligned_{os.path.basename(vrt_file)}")
                                output_filename = os.path.splitext(output_filename)[0] + ".tif"
                                ylist.append(output_filename)

                                # Write the data to a new GeoTIFF file
                                with rasterio.open(output_filename, "w", **out_meta) as dst:
                                    dst.write(data)
                                print(f"  Saved aligned data to {output_filename}")
                            else:
                                print(f"  Skipping {vrt_file}: Output dimensions are invalid (height={out_height}, width={out_width}).")
                                output_filename = os.path.join(temp_dir, f"aligned_{os.path.basename(vrt_file)}")
                                output_filename = os.path.splitext(output_filename)[0] + ".tif"
                                shutil.copyfile(tls_fn, output_filename)
                                print(f"  Copied {tls_fn} to {output_filename} as a fallback.")
                                nlist.append(output_filename)
                        else:
                            print(f"  Skipping {vrt_file} due to issues reading data.")
                            output_filename = os.path.join(temp_dir, f"aligned_{os.path.basename(vrt_file)}")
                            output_filename = os.path.splitext(output_filename)[0] + ".tif"
                            shutil.copyfile(tls_fn, output_filename)
                            print(f"  Copied {tls_fn} to {output_filename} as a fallback.")

                except rasterio.RasterioIOError as e:
                    print(f"  Error processing {vrt_file}: {e}")
                    print(f"  Skipping {vrt_file} and continuing. Check if the file exists and is a valid raster.")
                except Exception as e:
                    print(f"  An unexpected error occurred while processing {vrt_file}: {e}")

    except rasterio.RasterioIOError as e:
        print(f"Error opening {tls_fn}: {e}")
        print("Please ensure the file path is correct and the file is a valid GeoTIFF.")
    except Exception as e:
        print(f"An unexpected error occurred with the reference GeoTIFF: {e}")

    return ylist,nlist

