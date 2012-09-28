# -*- coding: utf-8 -*-
#import os
#import sys

from teste.lib import app_globals as appg


import psycopg2
#from seiscomp3 import Client, IO, Core, DataModel

class Stations(object):

#    debug = False
#
    def __init__(self):
        self.stations_list = []
        
        # Connect to an existing database
        conn = psycopg2.connect(dbname="sc_request", user="sysop", password="sysop", host="10.110.0.130")
        
        # Open a cursor to perform database operations
        cur = conn.cursor()
        
        # Query the database and obtain data as Python objects
        cur.execute("""
                    SELECT          net.m_code as net,
                                    station.m_code as sta,
                                    station.m_description as desc,
                                    station.m_latitude as lat,
                                    station.m_longitude as lon,
                                    station.m_elevation as elev,
                                    count(stream.m_code) as channels
                    FROM            station,
                                    network as net,
                                    sensorlocation as sl LEFT OUTER JOIN stream ON (stream._parent_oid = sl._oid )
                    WHERE            sl._parent_oid = station._oid
                    AND             station._parent_oid = net._oid
                    /* AND          net.m_code = 'BL'
                    AND             station.m_code = 'APOB'
                    */
                    GROUP BY    net.m_code, 
                                    station.m_code, 
                                    station.m_description, 
                                    station.m_longitude, 
                                    station.m_latitude, 
                                    station.m_elevation
                    ORDER BY        net, sta;
                    """)

        for line in cur:
            self.stations_list.append(dict(
                NN = line[0],
                SSSSS = line[1],
                desc = line[2],
                lat = ("%.2f") % line[3], 
                lon = ("%.2f") % line[4],
                ele = ("%.1f") % line[5],
                n_ch = line[6],
            ))
        
        # Close communication with the database
        cur.close()
        conn.close()



#"""
#scheli capture -I "combined://seisrequest.iag.usp.br:18000;seisrequest.iag.usp.br:18001" 
#                --offline --amp-range=1E3 --stream BL.AQDB..HHZ -N -o saida.png
#"""

# scxmldump $D -E iag-usp2012ioiu | scmapcut --ep - -E iag-usp2012ioiu -d 1024x768 -m 5 --layers -o evt.png


    def getAll(self):
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
                    }""" % (sta['NN'], sta['SSSSS'], sta['desc'], float(sta['lat']), float(sta['lon']))
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

        # Connect to an existing database
        conn = psycopg2.connect(dbname="sc_request", user="sysop", password="sysop", host="10.110.0.130")
        
        # Open a cursor to perform database operations
        cur = conn.cursor()
        
        # Query the database and obtain data as Python objects
        cur.execute("""
                    SELECT          net.m_code as net,
                                    station.m_code as sta,
                                    sl.m_code as loc,
                                    stream.m_code as cha,
                                    stream.m_start as cha_sta,
                                    stream.m_end as cha_end,
                                    station.m_description as desc,
                                    station.m_latitude as lat,
                                    station.m_longitude as lon,
                                    station.m_elevation as elev
                    FROM            station,
                                    network as net,
                                    sensorlocation as sl,
                                    stream
                    WHERE           stream._parent_oid = sl._oid
                    AND             sl._parent_oid = station._oid
                    AND             station._parent_oid = net._oid
                    AND             net.m_code = '%s'
                    AND             station.m_code = '%s'
                    ORDER BY        station.m_code;
                    """  % (nn, ss))

        self.details = []
        for line in cur:
            png = "%s.%s.%s.%s.ALL.png" % (line[0], line[1], line[2].replace("","--"), line[3])
            self.details.append(dict(NN=line[0],
                                     SSSSS=line[1],
                                     LL=line[2],
                                     CCC=line[3],
                                     desc = line[6],
                                     lat = ("%.3f") % line[7],
                                     lon = ("%.3f") % line[8],
                                     ele = ("%.1f") % line[9], 
                                     png = "/images/pqlx/%s.%s/%s"% (line[0], line[1], png ),
                                     ))
        
        # Close communication with the database
        cur.close()
        conn.close()

        if self.details == []:
            return dict(error="unable to get streams")
        
        return dict(error="",
                    details=self.details,
                    )

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
        
