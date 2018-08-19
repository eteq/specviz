import numpy as np
from astropy.wcs import WCS

from glue.app.qt import GlueApplication

from glue.core import Data
from glue.core.component import Component
from glue.core.coordinates import WCSCoordinates

from ..viewer_single_spectrum import SpecvizSingleDataViewer


class TestSpecvizSingleDataViewer(object):

    def setup_method(self, method):

        # Set up simple spectral WCS
        wcs_1d = WCS(naxis=1)
        wcs_1d.wcs.ctype = ['VELO-LSR']
        wcs_1d.wcs.set()

        # Set up a spectral cube WCS
        wcs_3d = WCS(naxis=3)
        wcs_3d.wcs.ctype = ['RA---TAN', 'DEC--TAN', 'VELO-LSR']
        wcs_3d.wcs.set()

        # Set up glue Coordinates object
        coords_1d = WCSCoordinates(wcs=wcs_1d)
        coords_3d = WCSCoordinates(wcs=wcs_3d)

        self.data_1d = Data(label='spectrum', coords=coords_1d)
        self.data_3d = Data(label='spectrum', coords=coords_3d)

        # FIXME: there should be an easier way to do this in glue
        x = np.array([3.4, 2.3, -1.1, 0.3])
        y = np.array([3.2, 3.3, 3.4, 3.5])
        self.data_1d.add_component(Component(x, units='Jy'), 'x')
        self.data_1d.add_component(Component(y, units='Jy'), 'y')
        self.data_3d.add_component(Component(np.broadcast_to(x, (6, 5, 4)), units='Jy'), 'x')
        self.data_3d.add_component(Component(np.broadcast_to(x, (6, 5, 4)), units='Jy'), 'y')

        self.app = GlueApplication()
        self.session = self.app.session
        self.hub = self.session.hub

        self.data_collection = self.session.data_collection
        self.data_collection.append(self.data_1d)
        self.data_collection.append(self.data_3d)

    def test_init_viewer(self):
        self.app.new_data_viewer(SpecvizSingleDataViewer)

    def test_add_data_1d(self):
        viewer = self.app.new_data_viewer(SpecvizSingleDataViewer)
        viewer.add_data(self.data_1d)
        assert viewer.layers[0].plot_data_item.visible

    def test_add_data_3d(self):
        viewer = self.app.new_data_viewer(SpecvizSingleDataViewer)
        viewer.add_data(self.data_3d)
        assert viewer.layers[0].plot_data_item.visible

    def test_define_subset(self):
        viewer = self.app.new_data_viewer(SpecvizSingleDataViewer)
        viewer.add_data(self.data_3d)
        self.data_collection.new_subset_group(subset_state=self.data_3d.id['x'] > 0, label='Subset')
        assert viewer.layers[0].plot_data_item.visible
        assert viewer.layers[0].plot_data_item.zorder == 1
        assert viewer.layers[1].plot_data_item.visible
        assert viewer.layers[1].plot_data_item.zorder == 2
