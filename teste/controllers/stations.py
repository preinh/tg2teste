#from tg import expose, request

from tg import expose, flash, require, url, lurl, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_

from teste.lib.base import BaseController
from teste import model

from itertools import cycle


__all__ = ['StationsController']

class StationsController(BaseController):
    
    _s = model.stations.Stations()

    @expose('teste.templates.stations')
    def index(self):
        """Handle the stations page."""
        stations_list = self._s.getAll()
        json = self._s.getAllJson()
        return dict(page = 'stations', 
                    stations = stations_list,
                    cycle = cycle,
                    json = json)
    
    @expose('teste.templates.stations')
    def stations(self):
        """Handle the events page."""
        #s = model.stations.Stations()
        stations_list = self._s.getAll()
        json = self._s.getAllJson()
        return dict(page='stations', 
                    cycle = cycle,
                    json = json)


    @expose('teste.templates.station')
    def _default(self, came_from=lurl('/')):
        id = came_from
        station_details = self._s.getDetails(id)
        #print "ID::" + str(station_details)
        return dict(page='station',
                    d = station_details)
        