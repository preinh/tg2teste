#from tg import expose, request

from tg import expose, flash, require, url, lurl, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_

from teste.lib.base import BaseController
from teste import model

from itertools import cycle

__all__ = ['EventsController']

import tw2.core as twc
import tw2.forms as twf
import tw2.dynforms as twd
import tw2.jqplugins.ui as jqui



class EventFilterForm(twf.FormPage):
    title = None
    class child(twf.TableForm):
        submit = None
        
        de1 = jqui.widgets.DateTimePickerWidget(
                                          options={},
                                          events={
                                              'onClose': """ 
                                                    var startDateTextBox = $('#eventfilterform\\\\:de1');
                                                    var endDateTextBox = $('#eventfilterform\\\\:de2');
                                                    function(dateText, inst) {
                                                        if (endDateTextBox.val() != '') {
                                                            var testStartDate = startDateTextBox.datetimepicker('getDate');
                                                            var testEndDate = endDateTextBox.datetimepicker('getDate');
                                                            if (testStartDate > testEndDate)
                                                                endDateTextBox.datetimepicker('setDate', testStartDate);
                                                        }
                                                        else {
                                                            endDateTextBox.val(dateText);
                                                        }
                                                    }"""
                                                    ,
                                                'onSelect': """
                                                    var startDateTextBox = $('#eventfilterform\\\\:de1');
                                                    var endDateTextBox = $('#eventfilterform\\\\:de2');
                                                    function (selectedDateTime){
                                                        endDateTextBox.datetimepicker('option', 
                                                                                      'minDate', 
                                                                                      startDateTextBox.datetimepicker('getDate') 
                                                                                      );
                                                    }"""
                                                }
                                          )

        de2 = jqui.widgets.DateTimePickerWidget(
                                          options={},
                                          events={
                                              'onClose': """ 
                                                    var startDateTextBox = $('#eventfilterform\\\\:de1');
                                                    var endDateTextBox = $('#eventfilterform\\\\:de2');
                                                    function(dateText, inst) {
                                                         if (startDateTextBox.val() != '') {
                                                            var testStartDate = startDateTextBox.datetimepicker('getDate');
                                                            var testEndDate = endDateTextBox.datetimepicker('getDate');
                                                            if (testStartDate > testEndDate)
                                                                startDateTextBox.datetimepicker('setDate', testEndDate);
                                                        }
                                                        else {
                                                            startDateTextBox.val(dateText);
                                                        }
                                                }"""
                                                    ,
                                                'onSelect': """
                                                    var startDateTextBox = $('#eventfilterform\\\\:de1');
                                                    var endDateTextBox = $('#eventfilterform\\\\:de2');
                                                    function (selectedDateTime){
                                                        startDateTextBox.datetimepicker('option', 
                                                                                        'maxDate', 
                                                                                        endDateTextBox.datetimepicker('getDate') 
                                                                                        );
                                                    }
                                                    """
                                                }
                                          )
        
        de = jqui.widgets.DatePickerWidget()
        ate = jqui.widgets.DatePickerWidget()
        
        mag = jqui.widgets.SliderWidget(options={
                                        'range': True,
                                        'min' : -5,
                                        'max' : 12,
                                        'step' : 0.01,
                                        'values' : [0, 10],
                                                 },
                                        events={
                                                'slide' : """  
                                                        function( event, ui ) {
                                                            $( "#eventfilterform\\\\:mag_de"  ).val(ui.values[ 0 ]);
                                                            $( "#eventfilterform\\\\:mag_ate" ).val(ui.values[ 1 ]);
                                                        }
                                                        """,
                                                })
        mag_de = twf.HiddenField()
        mag_ate = twf.HiddenField()
        
        lat = jqui.widgets.SliderWidget(options={
                                        'range': True,
                                        'min' : -90,
                                        'max' : 90,
                                        'step' : 0.01,
                                        'values' : [-35, 6],
                                                 },
                                        events={
                                                'slide' : """  
                                                        function( event, ui ) {
                                                            $( "#eventfilterform\\\\:mag_values" ).val( "de " + ui.values[ 0 ] + " - ate " + ui.values[ 1 ] );
                                                        }
                                                        """,
                                                })
                                           
        lon = jqui.widgets.SliderWidget(options={
                                        'range': True,
                                        'min' : -180,
                                        'max' : 180,
                                        'step' : 0.01,
                                        'values' : [-90, -35],
                                                 },
                                        events={
                                                'slide' : """  
                                                        function( event, ui ) {
                                                            $( "#eventfilterform\\\\:mag_values" ).val( "de " + ui.values[ 0 ] + " - ate " + ui.values[ 1 ] );
                                                        }
                                                        """,
                                                })
        dep = jqui.widgets.SliderWidget(options={
                                        'range': True,
                                        'orientation': 'vertical',
                                        'min' : 0,
                                        'max' : 6500,
                                        'step' : 1.0,
                                        'values' : [0, 800],
                                                 },
                                        events={
                                                'slide' : """  
                                                        function( event, ui ) {
                                                            $( "#eventfilterform\\\\:mag_values" ).val( "de " + ui.values[ 0 ] + " - ate " + ui.values[ 1 ] );
                                                        }
                                                        """,
                                                })
        filtrar = twf.SubmitButton(value="Filtrar")

#        
#        class cast(tw2.forms.GridLayout):
#            extra_reps = 5
#            character = tw2.forms.TextField()
#            actor = tw2.forms.TextField()


class EventsController(BaseController):

    @expose('teste.templates.events')
    def index(self, *args, **kw):
        """Handle the events page."""
        e = model.events.Events()
        event_list = e.getAll()
        json = e.getAllJson()
        json_l = e.getLastJson()

        print "1 -- index "
        if kw != {}:
            print kw
            print kw['eventfilterform:de']
            print kw['eventfilterform:ate']
#            print kw['eventfilterform:mag']
#            print kw['eventfilterform:lat']
#            print kw['eventfilterform:lon']
#            print kw['eventfilterform:dep']

       
        f = EventFilterForm().req()
        
        return dict(page = 'events', 
                    filterForm = f,
                    events = event_list,
                    cycle = cycle,
                    json = json,
                    json_l = json_l
                    )
    
    @expose('teste.templates.events')
    def events(self, *args, **kw):
        """Handle the events page."""
        e = model.events.Events()
        event_list = e.getAll()
        json = e.getAllJson()
        json_l = e.getLastJson()

        print "2 -- events "
        if kw != {}:
            print kw['eventfilterform:de']
            print kw['eventfilterform:ate']
       
        
        
        f = EventFilterForm().req()
        return dict(page='events', 
                    filterForm = f,
                    events = event_list,
                    cycle = cycle,
                    json = json,
                    json_l = json_l
                    )

    @expose('teste.templates.event')
    def _default(self, came_from=lurl('/'), *args, **kw):
        id = came_from
        event_details = model.events.Events().getDetails(id)
        #print event_details
        f = EventFilterForm().req()
        
        print "3 -- default "
        if kw != {}:
            print kw['eventfilterform:de']
            print kw['eventfilterform:ate']
       

        
        return dict(page='event',
                    filterForm=f,
                    d = event_details)
        #redirect("/events/event&id="+id)
        