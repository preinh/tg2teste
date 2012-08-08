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


class Events(object):
    """
    Group definition for :mod:`repoze.what`.

    Only the ``group_name`` column is required by :mod:`repoze.what`.

    """
    def __init__(self):
    
#        print "eh nois nos evento"
        
        #dbDriverName="mysql"
        #dbAddress="sysop:sysop@localhost/seiscomp3"
        #dbPlugin = "dbmysql"
        
        self.dbDriverName="postgresql"
        self.dbAddress="sysop:sysop@10.110.0.130/sc_master"
#        self.dbAddress="sysop:sysop@localhost/seiscomp3"
        self.dbPlugin = "dbpostgresql"
        
        
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
        self.dbQuery = DataModel.DatabaseQuery(self.dbDriver)
        
        self.s = Core.Time_FromString("2012-07-01 00:00:00", "%F %T")
        self.e = Core.Time_FromString("2012-08-15 00:00:00", "%F %T")
    
        self.event_list = []

    def getAll(self):
        
        qEvts = self.dbQuery.getEvents(self.s, self.e)
        
        self.events = []
        self.event_list = []
        for obj in qEvts:
            evt = DataModel.Event.Cast(obj)
            if evt:
                self.events.append( [ evt.publicID(), evt.preferredOriginID() ] )
                
        for evt, org in self.events:
            qOrigin = self.dbQuery.getOrigins(evt)

            for obj_origin in qOrigin:
                origin = DataModel.Origin.Cast(obj_origin)
                if origin.publicID() == org:
                    d = dict(id=evt, 
                             time=str(origin.time().value()), 
                             lat=origin.latitude().value(), 
                             lon=origin.longitude().value(),
                             dep=origin.depth().value())        
                    self.event_list.append(d)
                    break
        
        #print self.event_list
        return self.event_list

    #{ Columns

    #{ Relations

    #{ Special methods

    def __repr__(self):
        return ('<Events: start=%s end=%s>' % str(self.s), str(self.e)).encode('utf-8')

    def __unicode__(self):
        return "Events bla bla"

    #}

        
        #d = dict(id=evt.publicID(), lat=evt.lat(), lon=evt.longitude(), dep=evt.depth()) 
        #events.append(d)
        #print d