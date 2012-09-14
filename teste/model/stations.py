# -*- coding: utf-8 -*-
#import os
#import sys

from teste.lib import app_globals as appg


import psycopg2
from seiscomp3 import Client, IO, Core, DataModel

class Stations(object):

    debug = False

    def __init__(self):
        if self.debug:
            self.dbDriverName="mysql"
            self.dbAddress="sysop:sysop@localhost/seiscomp3"
            self.dbPlugin = "dbmysql"
#            self.dbDriverName="mysql"
#            self.dbAddress="sysop:sysop@localhost/seiscomp3"
#            self.dbPlugin = "dbmysql"
        else:
            self.dbDriverName="postgresql"
            self.dbAddress="sysop:sysop@10.110.0.130/sc_request"
            self.dbPlugin = "dbpostgresql"
            
        self.dbQuery = self._createQuery()

        self.inventory = appg.singleInventory().inventory

        self.stations_list = []

#"""
#scheli capture -I "combined://seisrequest.iag.usp.br:18000;seisrequest.iag.usp.br:18001" 
#                --offline --amp-range=1E3 --stream BL.AQDB..HHZ -N -o saida.png
#"""

# scxmldump $D -E iag-usp2012ioiu | scmapcut --ep - -E iag-usp2012ioiu -d 1024x768 -m 5 --layers -o evt.png


    def getAll(self):
        
        self.stations_list = []
        
        
        # Connect to an existing database
        conn = psycopg2.connect(dbname="sc_request", user="sysop", password="sysop", host="10.110.0.130")
        
        # Open a cursor to perform database operations
        cur = conn.cursor()
        
        # Query the database and obtain data as Python objects
        cur.execute("""
                        SELECT          pstation.m_publicid as publicid,
                                        station.m_code,
                                        station.m_description,
                                        station.m_latitude,
                                        station.m_longitude,
                                        station.m_elevation
                        FROM            station,
                                        publicobject as pstation
                        WHERE           station._oid = pstation._oid
                        ORDER BY        station.m_code;
                          """)

        for line in cur:
            self.stations_list.append(dict(
            NN = line[0].split("/")[1],
            SSSSS = line[1],
            desc = line[2],
            lat= ("%.2f") % line[3], 
            lon= ("%.2f") % line[4],
            ele= ("%.1f") % line[5],
            ))
        
        # Close communication with the database
        cur.close()
        conn.close()

        return self.stations_list


    def getAllJson(self):
            
        json = ""                                                                  
        for sta in self.stations_list:
                element = """{
                    NN:       '%s',
                    SSSSS:    '%s',
                    desc:     '%s',
                    lat:       %f, 
                    lng:       %f
                    }""" % (sta['NN'], sta['SSSSS'], sta['desc'], sta['lat'], sta['lon'])
                json += element + ","

        json = "var businesses = [" + json[ : -1] + "];"
        #print json
        return json


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

        self.details = []
                                                              
        for i in range(self.inventory.networkCount()):
            net = self.inventory.network(i)
            if nn != net.code(): continue
            for j in range(net.stationCount()):
                station = net.station(j)
                if ss != station.code(): continue
                for l in range(station.sensorLocationCount()):
                    location = station.sensorLocation(l)
                    for s in range(location.streamCount()):
                        stream = location.stream(s)
                        png = "%s.%s.%s.%s.ALL.png" % (net.code(), station.code(), location.code().replace("","--"), stream.code()) 
                        self.details.append(dict(NN=net.code(),
                                                 SSSSS=station.code(),
                                                 LL=location.code(),
                                                 CCC=stream.code(),
                                                 desc = station.description(),
                                                 lat = ("%.3f") % station.latitude(),
                                                 lon = ("%.3f") % station.longitude(),
                                                 ele = ("%.1f") % station.elevation(), 
                                                 png = "/images/pqlx/%s.%s/%s"% (net.code(), station.code(), png ),
                                                 ))
        return dict(error="",
                    details=self.details,
                    )


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
        
