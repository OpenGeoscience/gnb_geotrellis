from geonotebook.vis import Ktile

class GeoTrellis(Ktile):
    def ingest(self, data, name=None, **kwargs):
        # Verify that a kernel_id is present otherwise we can't
        # post to the server extension to add the layer
        kernel_id = kwargs.pop('kernel_id', None)
        if kernel_id is None:
            raise Exception(
                "KTile vis server requires kernel_id as kwarg to ingest!")

        options = {
            'name': data.name if name is None else name
        }

        options.update(kwargs)

        # Make the Request
        base_url = '{}/{}/{}'.format(self.base_url, kernel_id, name)

        r = requests.post(base_url, json={
            "provider": {
                "name": "proxy",
                "url": "{}/tiles/{}/\{Z\}/\{X\}/\{Y\}.png".format(base_url, options['name'])
            }
        })

        if r.status_code == 200:
            return base_url
        else:
            raise RuntimeError(
                "KTile.ingest() returned {} error:\n\n{}".format(
                    r.status_code, ''.join(r.json()['error'])))
