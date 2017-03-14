from geonotebook.wrappers.file_reader import validate_index

class GeoTrellisReader(object):
    def __init__(self, uri, band_names=None):
        self.uri = uri
        self.band_names = []
        self._dataset = None

    @property
    def dataset(self):
        pass

    @property
    def path(self):
        return self.uri


    def index(self, *args, **kwargs):
        pass

    def read(self, *args, **kwargs):
        pass

    # Dataset level API
    @property
    def count(self):
        pass

    @property
    def height(self):
        pass

    @property
    def width(self):
        pass

    @property
    def bounds(self):
        pass

    def get_band_ix(self, indexes, x, y):
        pass

    # Band level API
    @validate_index
    def get_band_min(self, index, **kwargs):
        pass

    @validate_index
    def get_band_max(self, index, **kwargs):
        pass

    @validate_index
    def get_band_mean(self, index, **kwargs):
        pass

    @validate_index
    def get_band_stddev(self, index, **kwargs):
        pass

    @validate_index
    def get_band_nodata(self, index):
        pass

    @validate_index
    def get_band_name(self, index, default=None):
        pass

    @validate_index
    def get_band_data(self, index, window=None, masked=True, **kwargs):
        pass
