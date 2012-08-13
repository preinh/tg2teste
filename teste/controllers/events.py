#from tg import expose, request

from tg import expose, flash, require, url, lurl, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_

from teste.lib.base import BaseController
from teste import model

from itertools import cycle


__all__ = ['EventsController']

class EventsController(BaseController):

    @expose('teste.templates.events')
    def index(self):
        """Handle the events page."""
        e = model.events.Events()
        event_list = e.getAll()
        json = e.getAllJson()
        json_l = e.getLastJson()
        return dict(page = 'events', 
                    events = event_list,
                    cycle = cycle,
                    json = json,
                    json_l = json_l
                    )
    
    @expose('teste.templates.events')
    def events(self):
        """Handle the events page."""
        e = model.events.Events()
        event_list = e.getAll()
        json = e.getAllJson()
        json_l = e.getLastJson()
        return dict(page='events', 
                    events = event_list,
                    cycle = cycle,
                    json = json,
                    json_l = json_l
                    )

    @expose('teste.templates.event')
    def _default(self, came_from=lurl('/')):
        id = came_from
        event_details = model.events.Events().getDetails(id)
        #print event_details
        return dict(page='event',
                    d = event_details)
        #redirect("/events/event&id="+id)
        