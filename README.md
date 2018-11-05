# GeoIPGoogleMap
A modules that provides Geo Information with a distance and Google MAP URI between two IP addresses

Requirement

    PYTZ: https://pypi.python.org/pypi/pytz/
    GEOPY: https://github.com/geopy/geopy.git
    GEOIP: apt-get install python-geoip
    GeoLite City: http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz

USAGE: *python geolib_distance.py [-s source IP -d dest IP -g GeoLiteCity.dat location ]\* *python geolib_distance.py -s 128.220.192.40 -d 74.125.228.198 -g /usr/share/GeoIP/GeoIPCity.dat*"

OUTPUT:

* GEO LOC : 128.220.192.40(United States : Maryland : Baltimore )  -  74.125.228.198(United States : California : Mountain View )**
* SIP date: (America/New_York:2014-10-07 16:33:12.438281-04:00)**
* DIP date: (America/Los_Angeles:2014-10-07 13:33:12.516291-07:00)**
* Distances : 2445 miles(3936 Kilometers)**
* Google MAP: https://maps.google.com/maps?saddr=Baltimore,+Maryland,+United+States&daddr=Mountain+View,+California,+United+States&hl=en&sll=39.3288002014,-76.5967025757&sspn=37.4192008972,-122.057403564")**
