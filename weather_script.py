#!/usr/bin/python2
# -*- coding: utf-8 -*-
# Copyright (c) 2015 Gris Ge
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#     The above copyright notice and this permission notice shall be included
#     in all copies or substantial portions of the Software.
#
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#     OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#     MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#     IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#     CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#     TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#     SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#
# Author: Gris Ge <cnfourt@gmail.com>

# Code was edit based on
# https://github.com/mpetroff/kindle-weather-display.git
# Which is also MIT license.
#
# Kindle Weather Display
# Matthew Petroff (http://mpetroff.net/)
# September 2012

import codecs
import time
import datetime
import os
import sys

from weather_api import WeatherAPI
from argparse import ArgumentParser

CODE_FOLDER = os.path.dirname(os.path.realpath(__file__))
OUTPUT = "/var/www/html/weather/weather.png"
SVG_PORTRAIT_FILE = "%s/weather-script-preprocess.svg" % CODE_FOLDER
SVG_LANSCAPE_FILE = "%s/weather-script-preprocess-landscape.svg" % CODE_FOLDER
SVG_FILE = SVG_PORTRAIT_FILE
SVG_OUTPUT = "%s/weather-script-output.svg" % CODE_FOLDER
MAX_WEATHER_DAY_COUNT = 3

if len(sys.argv) < 4:
    print("Need 3 or more argument for API key, latitude, longitud, "
          "[is_landscape]")
    exit(1)

weather_obj = WeatherAPI(sys.argv[1], sys.argv[2], sys.argv[3])

print weather_obj.__dict__

if len(sys.argv) >= 5 and sys.argv[4] != 0:
    SVG_FILE = SVG_LANSCAPE_FILE

# Open SVG to process
output = codecs.open(SVG_FILE, "r", encoding="utf-8").read()

_MAP = {
    "$I": WeatherAPI.dayPic,
    "$N": WeatherAPI.nightPic,
    "$H": WeatherAPI.weather,
    "$L": WeatherAPI.temperature,
}
for x in _MAP.keys():
    for i in range(MAX_WEATHER_DAY_COUNT + 1):
        output = output.replace("%s%d" % (x, i),
                                "%s" % _MAP[x](weather_obj, i))

# Replace refresh time
output = output.replace("$TIME",
                        datetime.datetime.now().strftime("%b %d %a %H:%M"))

# Updaet AQI. TODO(Gris Ge): still place holder yet.
output = output.replace("$AQI", "AQI:"+weather_obj._aqi)

# CITY NAME.
output = output.replace("$CITY", weather_obj._currentCity)

day_one = weather_obj.today

# Insert days of week
one_day = datetime.timedelta(days=1)
days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

for i in range(MAX_WEATHER_DAY_COUNT + 1):
    output = output.replace("$D%s" % i,
                            days_of_week[(day_one + i * one_day).weekday()])

# Write output
codecs.open(SVG_OUTPUT, "w", encoding="utf-8").write(output)

os.system("rsvg-convert --background-color=white -o "
          "%s %s" % (OUTPUT, SVG_OUTPUT))

os.system("pngcrush -c 0 -ow %s 1>/dev/null 2>&1" % OUTPUT)
