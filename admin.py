#!/usr/bin/env python
"""
Admin request handlers for Python Package project

Written by John Smith 2010-2012 | http://www.john-smith.me
Licenced under GPL v2           | http://www.gnu.org/licenses/gpl-2.0.html
"""

__author__ = "John Smith, 2012 <code@john-smith.me>"

import logging

import webapp2

import app_settings

from admin_pages import AdminHomePage



app = webapp2.WSGIApplication(
    [
        ("/Admin", AdminHomePage)
        ],
    debug = app_settings.APP_DEBUG)
