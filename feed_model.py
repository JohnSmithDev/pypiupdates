#!/usr/bin/env python
"""
GAE datastore specific version of the RSS/XML model
"""

__author__ = "John Smith, 2012 <code@john-smith.me>"

import logging
import datetime

import models
import grab_latest_feed

def make_datetime(yyyymmddhhmm):
    """
    Return a datetime based on the supplied string
    """
    return datetime.datetime(year=int(yyyymmddhhmm[0:4]),
                             month=int(yyyymmddhhmm[4:6]),
                             day=int(yyyymmddhhmm[6:8]),
                             hour=int(yyyymmddhhmm[8:10]),
                             minute=int(yyyymmddhhmm[10:12]))

class PyPIRSSXMLGAEModel(grab_latest_feed.PyPIRSSDownload):
    """
    Subclass to save the downloaded RSS feed to GAE datastore.
    """
    def write(self):
        rss = models.DownloadedRSS(
            key_name = self.timestamp,
            download_time = make_datetime(self.timestamp),
            xml = self.content)
        try:
            rss.put()
            logging.info("Saved RSS feed to datastore OK (%d bytes)" %
                         (len(self.content)))
        except Exception, e:
            logging.error("Something screwed up saving to datastore [%s/%s]" %
                          type(e), e)


