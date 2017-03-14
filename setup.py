from setuptools import setup, find_packages

setup(
    name='gnb_geotrellis',
    version='0.0.0',
    description='A Geonotebook extension for working with GeoTrellis',
    long_description='A Geonotebook extension for working with GeoTrellis',
    url='https://github.com/OpenGeoscience',
    author='Kitware Inc',
    author_email='chris.kotfila@kitware.com',
    license='Apache License 2.0',
    install_requires=[
        "geonotebook",
        "findspark"
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
         'geonotebook.wrappers.raster_schema': [
             'geotrellis = gnb_geotrellis.wrappers:GeoTrellisReader'
         ],
         'geonotebook.vis.server': [
            "geotrellis = gnb_geotrellis.vis:GeoTrellis"
         ],
    }
)
