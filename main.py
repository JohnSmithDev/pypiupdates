#!/usr/bin/env python
"""
Main request handlers for Python Package project

Written by John Smith 2010-2012 | http://www.john-smith.me
Licenced under GPL v2           | http://www.gnu.org/licenses/gpl-2.0.html
"""

__author__ = "John Smith, 2012 <code@john-smith.me>"

import logging

import webapp2

import app_settings

# from user_pages import ConfirmPage, UserSettingsPage
from general_pages import UpdatesPage, AboutPage, HomePage
from manual_upload import UploadFeedFile

app = webapp2.WSGIApplication(
    [
        # URLs for registered/registering users
        # TODO
        # ("/confirm/", ConfirmPage),
        # ("/unsubscribe/(.*)", UserSettingsPage),
        # ("/settings/(.*)", UserSettingsPage),

        # Testing
        ("/uploadRSS", UploadFeedFile),

        # URLs for everyone
        ("/updates/(.*)", UpdatesPage),
        ("/about.*", AboutPage),
        ("/.*", HomePage)
        ],
    debug = app_settings.APP_DEBUG)
