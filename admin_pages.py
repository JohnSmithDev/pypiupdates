#!/usr/bin/env python
"""
Request handlers for admin pages
Note that admin pages should never be cached
"""

__author__ = "John Smith, 2012 <code@john-smith.me>"

import logging
import sys

from handler import LoggingHandler

import content


class AdminHomePage(LoggingHandler):
    def get(self):
        content.output_page(self, template_file="admin.html",
                            values={
                "days": ["%02d" % (z + 1) for z in range(31)]
                })
