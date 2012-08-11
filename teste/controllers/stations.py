#from tg import expose, request

from tg import expose, flash, require, url, lurl, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_

from teste.lib.base import BaseController
from teste import model

from itertools import cycle


__all__ = ['StationsController']

class StationsController(BaseController):

    @expose('teste.templates.stations')
    def index(self):
        """Handle the stations page."""
        stations_list = model.stations.Stations().getAll()
        return dict(page = 'stations', 
                    stations = stations_list,
                    cycle = cycle )
    
    @expose('teste.templates.stations')
    def stations(self):
        """Handle the events page."""
        stations_list = model.stations.Stations().getAll()
        print "ma" 
        return dict(page='stations', 
                    station=stations_list)


    @expose('teste.templates.station')
    def _default(self, came_from=lurl('/')):
        id = came_from
        station_details = model.stations.Stations().getDetails(id)
        print station_details
        return dict(page='station',
                    d = station_details)
        