# -*- coding: utf-8 -*-
#import os
#import sys
#
#from datetime import datetime
#from sqlalchemy import Table, ForeignKey, Column
#from sqlalchemy.orm import relation, synonym
#from sqlalchemy.types import Unicode, Integer, DateTime
#
#from teste.model import DeclarativeBase, metadata, DBSession

from seiscomp3 import Client, IO, Core, DataModel
import commands

from datetime import datetime, timedelta

class Events(object):

    debug = False

    def __init__(self):
    
        if self.debug:
            self.dbDriverName="postgresql"
            self.dbAddress="sysop:sysop@localhost/seiscomp3"
            self.dbPlugin = "dbpostgresql"
#            self.dbDriverName="mysql"
#            self.dbAddress="sysop:sysop@localhost/seiscomp3"
#            self.dbPlugin = "dbmysql"
        else:
            self.dbDriverName="postgresql"
            self.dbAddress="sysop:sysop@10.110.0.130/sc_master"
            self.dbPlugin = "dbpostgresql"
        
        self.dbQuery = self._createQuery()        
        
        daysBefore = 20
        
        self.e = Core.Time.GMT()
        self.s = self.e - Core.TimeSpan(daysBefore*24*60*60)
        
#        self.s = Core.Time_FromString("2012-01-01 00:00:00", "%F %T")
#        self.e = Core.Time_FromString("2012-02-01 00:00:00", "%F %T")
    
        self.events_list = []


    def getAll(self):
        
        # query events
        qEvts = self.dbQuery.getEvents(self.s, self.e)
        
        # collect event/p_origin/p_mag
        self.events = []
        for obj in qEvts:
            evt = DataModel.Event.Cast(obj)
            if evt:
                self.events.append( [ evt.publicID(), evt.preferredOriginID(), evt.preferredMagnitudeID()] )
 
        # pra cada evento        
        for evt, p_org, p_mag in self.events:

            _e = self.dbQuery.getEventByPublicID(evt)
            self.dbQuery.load(_e)
            
            if _e.eventDescriptionCount() != 0:
                desc = _e.eventDescription(0).text()
            else:
                desc = "unknown"

            # pior jeito de buscar a preferred_origin
            qOrigin = self.dbQuery.getOrigins(evt)
            for obj_origin in qOrigin:
                origin = DataModel.Origin.Cast(obj_origin)
                if origin.publicID() == p_org:
                    break

            # separate origin from dbInterator
            org = origin
            
            #load origin parameters
            self.dbQuery.load(org)
            
            # get magnitudes
            nmag = org.magnitudeCount()
            if nmag != 0:
                # pior jeito de buscar a preferred_magnitude
                for i in xrange(nmag):
                    mag = org.magnitude(i)
                    if mag.publicID() == p_mag:
                        break
    
                val = mag.magnitude().value()
                typ = mag.type()
                stc = mag.stationCount()
                _mag = ("%.1f %s (%d)") % (val, typ, stc)
            else:
                _mag = "-- (--)" 
                
            d = dict(id=evt,
                     desc= desc,
                     time= str(org.time().value()), 
                     lat= ("%.2f") % org.latitude().value(), 
                     lon= ("%.2f") % org.longitude().value(),
                     dep= ("%d") % org.depth().value(),
                     mag= _mag
                     )        
            self.events_list.append(d)

        return sorted(self.events_list, key=lambda event: event['time'], reverse=True)

        return self.events_list


    def getAllJson(self):
        json=""
        for d in self.events_list[1:]:
            json += """
                {
                    id:     '%s',
                    desc:   '%s',
                    time:   '%s',
                    lat:    %f,
                    lng:    %f,
                    dep:    %f,
                    mag:    '%s'
                },
            """ % (d['id'], d['desc'], d['time'], float(d['lat']), float(d['lon']), float(d['dep']), d['mag'] )

        json = "var businesses = [" + json[ : -1] + "];"
        return json
    
    
    def getLastJson(self):
        json=""
        
        print self.events_list
        d = self.events_list[0]
        
        json = """
            {
                id:     '%s',
                desc:   '%s',
                time:   '%s',
                lat:    %f,
                lng:    %f,
                dep:    %f,
                mag:    '%s'
            },
        """ % (d['id'], d['desc'], d['time'], float(d['lat']), float(d['lon']), float(d['dep']), d['mag'] )

        json = "var last = [" + json[ : -1] + "];"
        return json



    def getDetails(self, eid=None):
        r = {}
        
        if not eid:
            r = dict(error="Invalid ID")
            return r

        evt = self.dbQuery.getEventByPublicID(eid)
        if not evt:
            r = dict(error="Event not Found")
            return r


        cmd = "/home/pirchiner/bin/scbulletin -E %s -3 --extra -d '%s://%s'" % (eid, self.dbDriverName, self.dbAddress)
        out = commands.getstatusoutput(cmd)

        out_lines = out[1]
#        out_lines = out_lines.replace("automatic", "<span style='font-color: red;'>automatic</span>")
#        out_lines = out_lines.replace("manual", "<span color='green'>manual</span>")
    
        out_lines = out_lines.split('\n')
    
        r = dict(error="",
                 eid=eid,
                 t = out_lines,
                 )
        return r


    def _createQuery(self):
        # Get global plugin registry
        self.registry = Client.PluginRegistry.Instance()
        # Add plugin dbmysql
        self.registry.addPluginName(self.dbPlugin)
        # Load all added plugins
        self.registry.loadPlugins()
        # Create dbDriver
        self.dbDriver = IO.DatabaseInterface.Create(self.dbDriverName)
        # Open Connection 
        #dbDriver.Open(dbAddress)   
        self.dbDriver.connect(self.dbAddress)
        # set Query object
        return DataModel.DatabaseQuery(self.dbDriver)

    
    def __repr__(self):
        return ('<Events: start=%s end=%s>' % str(self.s), str(self.e)).encode('utf-8')

    def __unicode__(self):
        return "Events bla bla"


class EventCatalog:
    IAG = 1
    QED = 2
    ISC = 3


class EventFilter(object):

    def __init__(self, 
                start_time = 0, 
                end_time = 0,
        
                min_mag = 0,
                max_mag = 10,
        
                min_dep = 0,
                max_dep = 6300,
        
                min_lat = -90,
                max_lat = +90,
                
                min_lon = -180,
                max_lon = +180,
                
                catalogs = [EventCatalog.IAG]
                ):
        
        self.start_time = start_time 
        self.end_time = end_time

        self.min_mag = min_mag
        self.max_mag = max_mag

        self.min_dep = min_dep
        self.max_dep = max_dep

        self.min_lat = min_lat
        self.max_lat = max_lat
        
        self.min_lon = min_lon
        self.max_lon = max_lon
        
        self.catalogs = catalogs

        