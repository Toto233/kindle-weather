#!/usr/bin/python2
# Copyright (C) 2015 Gris Ge
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; If not, see <http://www.gnu.org/licenses/>.
#
# Author: Gris Ge <cnfourt@gmail.com>
import sys
import time
import datetime
import json
from urllib2 import urlopen


def _fetch_json(url):
    json_str = urlopen(url).read()
    return json.loads(json_str)


def _parse_forecast(data_json):
    """
    return [WeatherData]
    """
    tmp_list = []
    for data in data_json["results"][0]["weather_data"]:
        #print data["date"], data["dayPictureUrl"],data["nightPictureUrl"],data["weather"],data["wind"],data["temperature"]
        tmp_list.append(WeatherData(data["date"], data["dayPictureUrl"],data["nightPictureUrl"],data["weather"],data["wind"],data["temperature"]))
    return tmp_list


class WeatherData(object):
    def __init__(self, date, dayPictureUrl, nightPictureUrl,weather,wind,temperature):
        self.date = date
        self.dayPictureUrl = dayPictureUrl
        self.nightPictureUrl = nightPictureUrl
        self.weather = weather
        self.wind = wind
        self.temperature = temperature


class WeatherAPI(object):

    _BASE_API_URL = "http://api.map.baidu.com/telematics/v3/weather?output=json"
    def __init__(self, api_key, lat, lon):
        url_api_key = "&ak=%s" % api_key
        url_location = "&location=%s,%s" % (lat, lon)
        forecast_json = _fetch_json(
            "%s%s%s" %
            (WeatherAPI._BASE_API_URL, url_api_key, url_location))

        self._data = _parse_forecast(forecast_json)
        self._today = datetime.date.today()
        self._currentCity=forecast_json["results"][0]["currentCity"]
        self._aqi=forecast_json["results"][0]["pm25"]
    def temperature(self, day):
        """
        Input day as integer, 0 means today, 1 means tomorrow, max is 3.
        """
        if day > 3:
            raise Exception("Invalid day, should less or equal to 3")

        return self._data[day].temperature

    def date(self, day):
        if day > 3:
            raise Exception("Invalid day, should less or equal to 3")
        return self._data[day].date

    def weather(self, day):
        if day > 3:
            raise Exception("Invalid day, should less or equal to 3")
        return self._data[day].weather

    def nightPic(self, day):
        if day > 3:
            raise Exception("Invalid day, should less or equal to 3")
        return self._data[day].nightPictureUrl
#===============
    def getPic(self, day):
        if day > 3:
            raise Exception("Invalid day, should less or equal to 3")
        dic={"mai":"hazy","qing":"clear","duoyun":"cloudy","yin":"cloudy","wu":"fog","xiaoxue":"snow","zhongxue":"snow","daxue":"snow"}
        org=""
        now=time.localtime()
        str_now = time.strftime("%m", now )   
        if(int(str_now)>7&int(str_now)<19):
            org =self._data[day].dayPictureUrl.split('/')[-1][0:-4]
        else:
            org =self._data[day].nightPictureUrl.split('/')[-1][0:-4]
        
        if day > 0:
            print self._data[day].dayPictureUrl.split('/')[-1][0:-4],dic[self._data[day].dayPictureUrl.split('/')[-1][0:-4]]
            return dic[self._data[day].dayPictureUrl.split('/')[-1][0:-4]]
        
        if(int(str_now)>7&int(str_now)<19):
            print org,dic[org]
            return  dic[org]
        else:
            print org,dic[org]
            return  dic[org]
        
        
#=============



    
    @property
    def today(self):
        """
        Return a object of datetime.date
        """
        return self._today

if __name__ == "__main__":
    weather = WeatherAPI( sys.argv[1],sys.argv[2],sys.argv[3])
