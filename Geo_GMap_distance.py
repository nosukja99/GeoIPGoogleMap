#!/usr/bin/env python
'''
A library that returns Distance between two IP address on Linux
'''
__author__ = "Hyejeong Kim"
__copyright__ = "Copyright 2018, Hyejeong Kim"
__credits__ = ["Hyejeong Kim"]
__license__ = "GPL v3"
__version__ = "0.2"
__maintainer__ = "Hyejeong Kim"
__email__ = "nosukja99@gmail.com"
__status__ = "beta"


import os, sys
import getopt
import datetime
import GeoIP
import socket
import pytz
from geopy.distance import distance as geopy_distance
from dateutil import parser
from dateutil.relativedelta import *

GEOIP_DB = "/usr/share/GeoIP/GeoIPCity.dat"

class _geo_distance(object):
	_g_geodb  = None
	def is_ip(self, ip):
	    '''Checks for valid IP address'''
	    try:
		socket.inet_aton(ip)
		return True
	    except socket.error:
		return False

	def open_geoip(self, geodb = GEOIP_DB):
		'''Open GeoCity.data'''
		if self._g_geodb is not None: return _g_geodb;
		try:
			self._g_geodb = GeoIP.open(GEOIP_DB,GeoIP.GEOIP_STANDARD)
			return self._g_geodb
		except:
			print "Access Error to GEODB: %s"%(geodb)
			return None
		

	def lookup_ip(self, ip):
		'''return geo location in string'''
		if self.is_ip(ip) is False: 
			print "Invalid IP: %s"%(ip)
			return ("", "", "")
		if self._g_geodb == None: 
			print "Invalid GEODB"
			return ("", "", "")

		gir = self._g_geodb.record_by_addr(ip)
		if gir != None:
			location = ""
			country = ""
			region = ""
			city = ""
			if gir['country_name']: country = gir['country_name']
			if gir['region_name'] : region = gir['region_name'] 
			if gir['city'] : city = gir['city'] 

			return (country, region, city)
		return ("", "", "")


	def get_geo_distance(self, pre_ip, cur_ip):
		'''Caculate a distance in miles and meters with SRC IP and DST IP'''
		if self.is_ip(pre_ip) is False or self.is_ip(pre_ip) is False: return ""
		if self._g_geodb == None: return ""

		pre_gir = self._g_geodb.record_by_addr(pre_ip)
		pre_loc = []
		cur_loc = []
		if pre_gir != None:
			if pre_gir['latitude'] : pre_loc.append(pre_gir['latitude'])
			if pre_gir['longitude']: pre_loc.append(pre_gir['longitude'])
		cur_gir = self._g_geodb.record_by_addr(cur_ip)

		if cur_gir != None:
			if cur_gir['latitude'] : cur_loc.append(cur_gir['latitude'])
			if cur_gir['longitude']: cur_loc.append(cur_gir['longitude'])

		d = geopy_distance(pre_loc, cur_loc)
		return (d.meters, d.miles)

	def get_geo_locs(self, pre_ip, cur_ip):
		'''Caculate Geo lastitude and longitude of two Ip addresses'''
		if self._g_geodb == None: return ""
		pre_gir = self._g_geodb.record_by_addr(pre_ip)
		cur_gir = self._g_geodb.record_by_addr(cur_ip)

		if pre_gir != None and cur_gir != None:
			return (pre_gir['latitude'], pre_gir['longitude'], cur_gir['latitude'], cur_gir['longitude'])

		return None
		
	def get_elapse(self, dtv):
		'''Caculate Current Time with TIMEZONE'''
		dtaccess = parser.parse(dtv)
		elapse = relativedelta( datetime.datetime.now(), dtaccess)
		elapse_output = ""

		if elapse.years > 0:
			elapse_output = str(elapse.years) + " years ";
		if elapse.months > 0:
			elapse_output = str(elapse.months) + " months ";
		if elapse.days > 0:
			elapse_output += str(elapse.days) + " days "
		if elapse.hours > 0:
			elapse_output += str(elapse.hours)+ " hours "
		if elapse.minutes > 0:
			elapse_output += str(elapse.minutes)+ " minutes"


		return elapse_output;

	def get_localtime_by_timezone(self, ip):
		'''Caculate Timezone with IP address'''
		time_location = ""
		if self._g_geodb == None: return ""
		gir = self._g_geodb.record_by_addr(ip)
		if gir['time_zone'] != None:
			time_location = datetime.datetime.now(pytz.timezone(gir['time_zone']))
			return (str(time_location), gir['time_zone']);
		return ("", "")


	def get_gmaplink(self, srcip, dstip):
		'''Create Google Map URL between two IP addresses'''
		if self.is_ip(srcip) is False or self.is_ip(dstip) is False: return ""
		if self._g_geodb == None: return ""

		GMAP_FMT = "https://maps.google.com/maps?saddr=%s,+%s,+%s&daddr=%s,+%s,+%s&hl=en&sll=%s,%s&sspn=%s,%s"
		GLINK  = ""
		(cur_country, cur_region, cur_city)= self.lookup_ip(dstip);
		(country, region, city)= self.lookup_ip(srcip);
		locs = self.get_geo_locs(srcip, dstip)
		if locs is not None:
			GLINK = GMAP_FMT % (city.replace(" ", "+"), region.replace(" ", "+"), country.replace(" ", "+"), cur_city.replace(" ", "+"), cur_region.replace(" ", "+"), cur_country.replace(" ", "+"), str(locs[0]), str(locs[1]), str(locs[2]), str(locs[3]))
		return GLINK


opts_str = \
           'USAGE:\n\
            python geolib_distance.py [-s source IP -d dest IP -g GeoLiteCity.dat location ]\n\
    	    python geolib_distance.py -s 128.220.192.40 -d 74.125.228.198 -g /usr/share/GeoIP/GeoIPCity.dat \n'


if __name__=="__main__":
	
	if len(sys.argv)==1:
		print opts_str
		sys.exit(0)
	sip = ""
	dip = ""
	geodb = ""

    #Parse args
	try:
		options, remainder = getopt.getopt(sys.argv[1:], 's:d:g:', ['sip=', 'dip=', 'geodb'])
		for opt, arg in options:
		    if opt in ('-s', '--sip'):
			sip = arg
		    elif opt in ('-d', '--dip'):
			dip= arg
		    elif opt in ('-g', '--geodb'):
			geodb= arg
	except Exception as e:
		print "\n\n",opts_str
		sys.exit(0)

	geod = _geo_distance()
	if geod.open_geoip() is None: 
		sys.exit(0)
	(country, region, city)= geod.lookup_ip(sip);
	slocation = "%s : %s : %s " % (country , region, city);
	(country, region, city)= geod.lookup_ip(dip);
	dlocation = "%s : %s : %s " % (country , region, city);

	geo_distance = geod.get_geo_distance(sip, dip)
	if geo_distance != None:
		cur_localtime  = ""
		localts = geod.get_localtime_by_timezone(sip) 
		localtd = geod.get_localtime_by_timezone(dip) 

		print "*Geo LOC : %s(%s)  -  %s(%s)"%(sip, slocation, dip, dlocation)
		if localts != None:
			print "SIP date: (%s:%s)"%(localts[1], localts[0])
		if localtd != None:
			print "DIP date: (%s:%s)"%(localtd[1], localtd[0])
	
		print "*Distances : %d miles(%d Kilometers)" %(geo_distance[1], geo_distance[0]/1000)
		print "*Google MAP: %s)"%geod.get_gmaplink(sip, dip)
