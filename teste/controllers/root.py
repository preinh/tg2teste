# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_

from teste import model

from repoze.what import predicates
from teste.controllers.secure import SecureController

from teste.model import DBSession, metadata

from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController

from teste.lib.base import BaseController
from teste.controllers.error import ErrorController

from teste.controllers.events import EventsController
from teste.controllers.movie import MovieController


__all__ = ['RootController']

from tw2.jqplugins.jqgrid import jqGridWidget
from tw2.jqplugins.jqgrid.base import word_wrap_css
from random import random
from random import randint

r = lambda x: randint(0, x - 1)

# No sample b/c its so difficult to find a datasource.

def generate_data(n):
    fnames = ['S.', 'J.']
    lnames = ['Flanderson', 'Anderson', 'Sanderson', 'Boot', 'Bean', 'Resig']
    intros = ['', 'On the', 'Regarding the', 'On', 'New Developments in',
              'A Survey of the',
             ]
    adjectives = ['Scientific', 'Schmientific', 'Cosmological', 'Astronomical',
                  'Computational', 'Fromputational', 'Mechanical', 'Chemical',
                  'Pythonic', 'Functional', 'Declarative', 'Quantum',
                  'Entanglement', 'Singular', 'Non-negative',
                 ]
    nouns = ['Problems', 'Solutions', 'Ins-and-outs', 'Nuances',
             'Transmogrification', 'Implementation',
            ]
    segues = ['of', 'underlying']
    journals = ['Review', 'Journal', 'Conference']
    for i in range(n):
        authors = ", ".join(["%s %s" % (fnames[r(len(fnames))],
                                        lnames[r(len(lnames))])
                             for j in range(randint(1, 2))])
        title = "%s %s %s %s %s %s." % (
            intros[r(len(intros))],
            adjectives[r(len(adjectives))],
            nouns[r(len(nouns))],
            segues[r(len(segues))],
            adjectives[r(len(adjectives))],
            nouns[r(len(nouns))],
        )
        journal = "The %s of %s %s" % (
            journals[r(len(journals))],
            adjectives[r(len(adjectives))],
            nouns[r(len(nouns))],
        )
        published = randint(1955, 2010)
        yield {'authors': authors,
               'title': title,
               'journal': journal,
               'published_on': published}

class mygrid(jqGridWidget):
    options = {
        'pager': 'module-0-demo_pager',
        'caption': 'All research publications',
        'data': [row for row in generate_data(55)],
        'datatype': 'local',
        'colNames': ['Authors', 'Title', 'Journal', 'Published'],
        'colModel': [
            {
                'name':'authors',
                'width':50,
                'align':'center',
            }, {
                'name':'title',
            }, {
                'name':'journal',
            }, {
                'name':'published_on',
                'width':50,
                'align':'center'
            },
        ],
        'rowNum': 15,
        'rowList': [15, 30, 50],
        'viewrecords': True,
        'imgpath': 'scripts/jqGrid/themes/green/images',
        'width': 920,
        'height': 'auto',
    }
    pager_options = {"search": True, "refresh": True, "add": False, }
    prmSearch = {
        "sopt": ["cn", "bw"],
        "caption": "Search...",
        "multipleSearch": True,
    }
#    custom_pager_buttons = [
#        {
#            "caption":"",
#            "buttonicon":"ui-icon-newwin",
#            'onClickButton': None,
#            'position': "last",
#            'title':"B1",
#            'cursor':"pointer"
#        }, {
#            'caption': "",
#            'buttonicon': "ui-icon-cart",
#            'onClickButton': None,
#            'position': "first",
#            'title': "B2",
#            'cursor': "pointer"
#        },
#    ]

    def prepare(self):
        self.resources.append(word_wrap_css)
        super(mygrid, self).prepare()
            
    
class grdEvents(jqGridWidget):

    def prepare(self):
        self.resources.append(word_wrap_css)
        super(grdEvents, self).prepare()
            
    options = {
        'pager': 'module-0-demo_pager',
        'caption': 'Boletim Sismico Brasileiro',
        'data': model.events.Events().getAll(),
        'datatype': 'local',
        'colNames': ['Id', 'Time', 'Lat', 'Lon', 'Dep'],
        'colModel': [
            {
                'name':'id',
                'width':50,
                'align':'center',
            }, {
                'name':'time',
            }, {
                'name':'lat',
            }, {
                'name':'lon',
            }, {
                'name':'dep',
                'width':50,
                'align':'center'
            },
        ],
        'rowNum': 15,
        'rowList': [15, 30, 50],
        'viewrecords': True,
        'imgpath': 'scripts/jqGrid/themes/green/images',
        'width': 920,
        'height': 'auto',
    }
    pager_options = {"search": True, "refresh": True, "add": False, }
    prmSearch = {
        "sopt": ["cn", "bw"],
        "caption": "Search...",
        "multipleSearch": True,
    }
    

class RootController(BaseController):
    """
    The root controller for the teste application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)

    error = ErrorController()
    #events = EventsController()

    movie = MovieController()


    @expose('teste.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('teste.templates.jgrid')
    def events(self):
        """Handle the events page."""
        grid = grdEvents('bsb')
        return dict(page='events', w=grid)

    
    @expose('teste.templates.stations')
    def stations(self):
        """Handle the stations page."""
        #print "atendi ao events request"
        event_list = model.events.Events().getAll()
        #print event_list
        return dict(page='stations', events=event_list)
    

    @expose('teste.templates.waveform')
    def waveform(self):
        """Handle the waveform page."""
        #print "atendi ao events request"
        event_list = model.events.Events().getAll()
        #print event_list
        return dict(page='waveform', events=event_list)
    

    @expose('teste.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('teste.templates.jgrid')
    def jgrid(self):
        """Handle the 'about' page."""
        w = mygrid("id")
        #print w.super._pager_options
        #print "corinthians 1" + str(w.pager_options)
        return dict(page='jgrid', w=w)


    @expose('teste.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(environment=request.environ)

    @expose('teste.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(params=kw)

    @expose('teste.templates.authentication')
    def auth(self):
        """Display some information about auth* on this application."""
        return dict(page='auth')

    @expose('teste.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Permitido apenas para managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('teste.templates.index')
    @require(predicates.is_user('editor', msg=l_('Permitido apenas para editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('teste.templates.login')
    def login(self, came_from=lurl('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Usuario|Senha invalidos'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect('/login',
                params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Bem vindo novamente, %s!') % userid)
        redirect(came_from)


    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('Esperamos ve-lo novamente em breve!'))
        redirect(came_from)
