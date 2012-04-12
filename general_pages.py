#!/usr/bin/env python
"""
Request handlers for general pages
"""

__author__ = "John Smith, 2012 <code@john-smith.me>"

import logging
import sys

from handler import MemcachablePageHandler, memcachable, HeadersAndContent

import models
import content
import misc_funcs

###
### A couple of static pages
###

class HomePage(MemcachablePageHandler):
    @memcachable
    def get(self):
        rendered = content.output_page(self, pagename="main")
        return HeadersAndContent(content=rendered)

class AboutPage(MemcachablePageHandler):
    @memcachable
    def get(self):
        rendered = content.output_page(self, pagename="about")
        return HeadersAndContent(content=rendered)

class UpdatesPage(MemcachablePageHandler):
    """
    Render a page showing the list of packages for the given date.
    If no date supplied, show the most recent set of updates
    If we have no data for an otherwise valid date, show a "sorry" page
    Otherwise return an HTTP error
    """

    @memcachable
    def get(self, daystring=None):
        daystring, day = misc_funcs.validate_date(daystring)

        # Grab the raw data for the date requested
        logging.debug("daystring is '%s'" % (daystring))
        pkg_model = models.DayPackages.get_by_key_name(daystring)
        if not pkg_model:
            self.error(400) # Bad Request
            return None
        pkg_list = pkg_model.unpickle()

        # Render it to a template

        rendered = content.output_page(self, template_file="update.html",
                                       values={
                "packages": pkg_list,
                "date": daystring}
                                       )
        return HeadersAndContent(content=rendered)
