# -*- coding: utf-8 -*-
#import os
#import sys

from teste.lib import app_globals as appg

from seiscomp3 import Client, IO, Core, DataModel

class Stations(object):

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
            self.dbAddress="sysop:sysop@10.110.0.130/sc_request"
            self.dbPlugin = "dbpostgresql"
            
        self.dbQuery = self._createQuery()

        self.inventory = appg.singleInventory().inventory


    def getAll(self):
        
        self.stations_list = []
                                                              
        for i in range(self.inventory.networkCount()):
            net = self.inventory.network(i)
            for j in range(net.stationCount()):
                station = net.station(j)
                self.stations_list.append(dict(NN=net.code(),
                                              SSSSS=station.code(),
                                              desc = station.description(),
                                              lat = ("%.3f") % station.latitude(),
                                              lon = ("%.3f") % station.longitude(),
                                              ele = ("%.1f") % station.elevation(), 
                                              ) )

        return self.stations_list



    def getDetails(self, sid=None):
        r = {}
        
        if not sid:
            r = dict(error="Invalid ID")
            return r
        try:
            sid_list = sid.split('.')
            nn = sid_list[0]
            ss = sid_list[1]
    
            if not nn or not ss:
                r = dict(error="Station Not Found")
                return r
        except:
                r = dict(error="Out of pattern NN.SSSSS")
                return r
    
        r = dict(error="",
                 evt = dict(id=nn,
                            desc=ss,
                            ),
                 org = dict(time="2012-00-00 00:00:00",
                            lat="-90",
                            lat_err = "0.2",
                            lon="-180",
                            lon_err="0.3",
                            dep=10,
                            dep_err=0.1,
                            rms = 0.15,
                            preferred=True,
                            status="A",
                            sta_count=15,
                            ),
                 picks=dict(station="BLA",
                            phase="P",
                            value="2012-00-00 00:01:00"
                            ),
                 mags=dict(type="mB",
                           value=7.4,
                           ),
                 amps=dict(type="mB",
                           value=5,
                           ),
                 )
        return r


    def _createQuery(self):

        print 0.88
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
        return ('<Stations: start=%s end=%s>' % str(self.s), str(self.e)).encode('utf-8')

    def __unicode__(self):
        return "Stations"


class StationFilter(object):

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
        
