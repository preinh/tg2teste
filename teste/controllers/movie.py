#from tg import expose, request

from tg import expose, flash, require, url, lurl, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_

from teste.lib.base import BaseController
from teste import model

__all__ = ['MovieController']

import tw2.core
import tw2.forms

class MovieForm(tw2.forms.FormPage):
    title = 'Movie Corinthians!!'
    resources = [tw2.core.CSSLink(link='/css/teste.css')]
    class child(tw2.forms.TableForm):
        title = tw2.forms.TextField(validator=tw2.core.Required)
        director = tw2.forms.TextField()
        genres = tw2.forms.CheckBoxList(options=['Action', 'Comedy', 'Romance', 'Sci-fi'])
        class cast(tw2.forms.GridLayout):
            extra_reps = 5
            character = tw2.forms.TextField()
            actor = tw2.forms.TextField()


class MovieController(BaseController):

    @expose('teste.templates.movie')
    def movie(self, *args, **kw):
        w = MovieForm(redirect='/movie/').req()
        return dict(widget=w, page='movie')
