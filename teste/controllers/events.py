#from tg import expose, request

from tg import expose, flash, require, url, lurl, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_

from teste.lib.base import BaseController
from teste import model

__all__ = ['EventsController']

class EventsController(BaseController):
    @expose('teste.templates.events')
    def events(self):
        """Handle the events page."""
        #print "atendi ao events request"
        event_list = model.events.Events().getAll()
        #print event_list
        return dict(page='events', events=event_list)
    
        #return dict(page='events')