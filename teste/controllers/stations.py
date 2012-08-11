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
        station_list = model.stations.Stations().getAll()
        return dict(page = 'stations', 
                    events = station_list,
                    cycle = cycle )
    
    @expose('teste.templates.stations')
    def events(self):
        """Handle the events page."""
        station_list = model.stations.Stations().getAll()
        return dict(page='stations', 
                    station=station_list)


    @expose('teste.templates.station')
    def _default(self, came_from=lurl('/')):
        id = came_from
        station_details = model.stations.Stations().getDetails(id)
        print station_details
        return dict(page='station',
                    d = station_details)
        