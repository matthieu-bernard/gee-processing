""" small utility functions

This is hugely inpired by eefolium codebase.
"""
import os
import zipfile
import sys

import ee
import requests
import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s',
                     level=logging.INFO, stream=sys.stdout)

LOG = logging.getLogger()


def ee_export_image(ee_image: ee.Image,
                    filename: str,
                    scale: int = None,
                    crs: str = None,
                    region=None,
                    file_per_band: bool = False):
    """Exports an ee.Image as a GeoTIFF.

    :param ee_object (object): The ee.Image to download.
    :param filename (str): Output filename for the exported image.
    :param scale (float, optional): A default scale to use for any bands that do not specify one; ignored if crs and crs_transform is specified. Defaults to None.
    :param crs (str, optional): A default CRS string to use for any bands that do not explicitly specify one. Defaults to None.
    :param region (object, optional): A polygon specifying a region to download; ignored if crs and crs_transform is specified. Defaults to None.
    :param file_per_band (bool, optional): Whether to produce a different GeoTIFF per band. Defaults to False.
    """
    if not isinstance(ee_image, ee.Image):
        raise TypeError('The ee_image must be an ee.Image.')

    filename = os.path.abspath(filename)
    basename = os.path.basename(filename)
    name = os.path.splitext(basename)[0]
    filetype = os.path.splitext(basename)[1][1:].lower()
    filename_zip = filename.replace('.tif', '.zip')

    if filetype != 'tif':
        print('The filename must end with .tif')
        return

    try:
        logging.info('Generating URL ...')
        params = {'name': name, 'filePerBand': file_per_band}
        params['scale'] = scale or ee_image.projection().nominalScale(
        ).multiply(10)
        params['region'] = region or ee_image.geometry()
        if crs is not None:
            params['crs'] = crs

        url = ee_image.getDownloadURL(params)
        print('Downloading data from {}\nPlease wait ...'.format(url))
        r = requests.get(url, stream=True)

        if r.status_code != 200:
            print('An error occurred while downloading.')
            print(r.text)
            return

        with open(filename_zip, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)

    except Exception as e:
        print('An error occurred while downloading.')
        print(e)
        return

    try:
        z = zipfile.ZipFile(filename_zip)
        z.extractall(os.path.dirname(filename))
        z.close()
        os.remove(filename_zip)

        if file_per_band:
            print('Data downloaded to %s' % os.path.dirname(filename))
        else:
            print('Data downloaded to %s' % filename)
    except Exception as e:
        print(e)



def ee_export_image_collection(ee_image_collection: ee.ImageCollection,
                               out_dir: str,
                               scale: float = None,
                               crs: str = None,
                               region=None,
                               file_per_band: bool = False) -> None:
    """Exports an ImageCollection as GeoTIFFs.

    Args:
        ee_image_collection (object): The ee.ImageCollection to download.
        out_dir (str): The output directory for the exported images.
        scale (float, optional): A default scale to use for any bands that do not specify one; ignored if crs and crs_transform is specified. Defaults to None.
        crs (str, optional): A default CRS string to use for any bands that do not explicitly specify one. Defaults to None.
        region (object, optional): A polygon specifying a region to download; ignored if crs and crs_transform is specified. Defaults to None.
        file_per_band (bool, optional): Whether to produce a different GeoTIFF per band. Defaults to False.
    """

    if not isinstance(ee_image_collection, ee.ImageCollection):
        raise TypeError(
            'The ee_image_collection must be an ee.ImageCollection.')

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    try:
        print('here')
        count = int(ee_image_collection.size().getInfo())
        print("Total number of images: {}\n".format(count))

        images = ee_image_collection.toList(count)
        for i in range(count):
            image = ee.Image(images.get(i))
            name = image.get('system:index').getInfo() + '.tif'
            filename = os.path.join(os.path.abspath(out_dir), name)
            print('Exporting {}/{}: {}'.format(i + 1, count, name))
            ee_export_image(image,
                            filename=filename,
                            scale=scale,
                            crs=crs,
                            region=region,
                            file_per_band=file_per_band)

    except Exception as e:
        print(e)
