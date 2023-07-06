from photutils.datasets import load_star_image
from astropy.stats import sigma_clipped_stats
from astropy.nddata import Cutout2D
from astropy.wcs import WCS
from test import names

from astropy.io import fits


def algo(path):
    image_data = fits.getdata(path, ext=0)
    hdu = load_star_image()
    data, true_wcs = hdu.data, WCS(hdu.header)
    print(hdu.header)
    mean, median, std = sigma_clipped_stats(data, sigma=3.0)

    from twirl import find_peaks

    xy = find_peaks(data)[0:20]

    import numpy as np
    import matplotlib.pyplot as plt
    from photutils.aperture import CircularAperture

    plt.imshow(image_data, vmin=np.median(image_data), vmax=3 * np.median(image_data), cmap="Greys_r")
    _ = CircularAperture(xy, r=10.0).plot(color="y")
    plt.show()

    from astropy.wcs.utils import proj_plane_pixel_scales

    fov = (image_data.shape * proj_plane_pixel_scales(true_wcs))[0]
    center = true_wcs.pixel_to_world(*np.array(image_data.shape) / 2)

    from twirl import gaia_radecs
    from twirl.geometry import sparsify

    all_radecs = gaia_radecs(center, 1.2 * fov)

    # we only keep stars 0.01 degree apart from each other
    all_radecs = sparsify(all_radecs, 0.01)

    from twirl import compute_wcs

    # we only keep the 12 brightest stars from gaia
    wcs = compute_wcs(xy, all_radecs[0:30], tolerance=10)

    from astroquery.simbad import Simbad

    # Set up the SIMBAD query
    customSimbad = Simbad()
    customSimbad.add_votable_fields('typed_id', 'coordinates')  # Adding typed_id and coordinates fields
    customSimbad.remove_votable_fields('names')  # Removing default names field

    # Perform the query
    result_table = customSimbad.query_object("Betelgeuse")

    # Extract the star information from the result table
    star_name = result_table['MAIN_ID'][0].decode('utf-8')
    typed_id = result_table['TYPED_ID'][0].decode('utf-8')
    coordinates = result_table['RA_d'][0], result_table['DEC_d'][0]

    # Print the star information
    print("Star Name:", star_name)
    print("Typed ID:", typed_id)
    print("Coordinates (RA, DEC):", coordinates)

    # plotting to check the WCS
    radecs_xy = np.array(wcs.world_to_pixel_values(all_radecs))
    result = plt.imshow(image_data, vmin=np.median(image_data), vmax=3 * np.median(image_data), cmap="Greys_r")
    _ = CircularAperture(radecs_xy, 5).plot(color="y", alpha=0.5)

    for i, (x, y) in enumerate(radecs_xy):
        if i % 10 == 0:
            plt.text(x, y, f"{names[(i + 1) % len(names)]}", color='w', fontsize=4, ha='center', va='center')

    plt.savefig('plot.png')  # Specify the filename and extension you prefer

    # plt.imsave('output.png',result)

# plt.show()
