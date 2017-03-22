import findspark
findspark.init()

from pyspark import SparkContext, SparkConf
from pyproj import Proj, transform
from shapely import geometry
from geopyspark.geotrellis.catalog import S3Catalog
from geopyspark.geopycontext import GeoPyContext
from geopyspark.avroregistry import AvroRegistry
import rasterio
from rasterio.io import MemoryFile
from rasterio import mask
import numpy as np

from gnb_geotrellis.globalmaptiles import get_extent

# If sparkcontext already exists use it
try:
    geopysc = GeoPyContext(master='local[*]', appName='Geopyspark')
except ValueError:
    pass

def latLongToWebMercator(lat_long_coords):
    in_proj  = Proj("+init=EPSG:4326")
    out_proj = Proj("+init=EPSG:3857")
    return [transform(in_proj, out_proj, x, y) for (x, y) in lat_long_coords]

def webMercatorToLatLong(mercator_coords):
    in_proj = Proj("+init=EPSG:3857")
    out_proj  = Proj("+init=EPSG:4326")
    return [transform(in_proj, out_proj, x, y) for (x, y) in mercator_coords]

def createCatalogConnection():

    catalog = S3Catalog(geopysc)
    return catalog

def getRdd(catalog, annotation):
    key_type = 'spatial'
    value_type = 'singleband'
    bucket = "kitware-catalog"
    prefix = 'full-catalog'
    layer_name = 'weld'
    layer_zoom = 14
    polygon = geometry.Polygon(
        latLongToWebMercator(list(annotation.exterior.coords)))

    (rdd, schema, metadata) = catalog.query(key_type, value_type, bucket, prefix,
                                            layer_name, layer_zoom, polygon)
    return rdd

def stitchTileArrays(ta):
    arr = None
    c_arr = None
    prev_col = None

    for key, _ta in sorted(ta, key=lambda x: (x[0]['col'], x[0]['row'])):
        # Build up the column
        if prev_col == None:
            c_arr = _ta['data']
        elif prev_col == key['col']:
            c_arr = np.vstack([c_arr, _ta['data']])
        # We've finished with the column,  add it
        # to the array
        else:
            if arr is None:
                arr = c_arr
            else:
                arr = np.hstack([arr, c_arr])

            c_arr = _ta['data']
        prev_col = key['col']

    return np.hstack([arr, c_arr])

def getSubset(annotation):
    catalog = createCatalogConnection()
    ta = getRdd(catalog, annotation).collect()
    rdd_extent = get_extent(14, annotation)
    tilearray = stitchTileArrays(ta)
    width = tilearray.shape[1]
    height = tilearray.shape[0]
    transform_params = (rdd_extent + (width, height))
    transform = rasterio.transform.from_bounds(*transform_params)
    return tilearray, transform

