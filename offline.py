#!/usr/bin/env python
"""
Cron/task queue jobs e.g.
- download the RSS XML every hour or so
- Parse the XML into a usable form every day
- Send out emails to subscribers every day
"""

__author__ = "John Smith, 2012 <code@john-smith.me>"

import logging
import datetime
import pickle
import StringIO
import time

import webapp2


from google.appengine.api import taskqueue
from google.appengine.api import memcache

from handler import LoggingHandler

import app_settings
import models
import grab_latest_feed
import misc_funcs
import simplify_feeds

from feed_model import PyPIRSSXMLGAEModel


class DownloadFeed(LoggingHandler):
    """
    Download the latest RSS from pypi.org and
    save to datastore.  (Does not actually parse
    it.)
    """
    def get(self):
        feed = PyPIRSSXMLGAEModel()
        feed.write()

def get_feeds_covering_date(_date):
    """
    Return a sorted list of XML strings containing all the
    RSS feeds we have covering the _date requested
    (Sorting is earliest first)
    """
    rss_q = models.DownloadedRSS.all()
    rss_q.filter("download_time >=", _date)
    rss_q.order("download_time")
    feeds = rss_q.fetch(100)

    return_list = []
    for feed in feeds:
        return_list.append(feed)
        # We include the first feed of the following day as it
        # likely contains the final items of the day we want -
        # but there's no point continuing further
        dl_day = datetime.date(feed.download_time.year,
                               feed.download_time.month,
                               feed.download_time.day)
        if dl_day > _date:
            break

    return return_list

def make_pickle_string(thing):
    """
    Turn some Python object into a pickle in a string
    """
    pstream = StringIO.StringIO()
    my_pickle = pickle.Pickler(pstream)
    my_pickle.dump(thing)
    retval = pstream.getvalue()
    pstream.close()
    # logging.debug("Pickle is '%s'" % (retval))
    return retval

def unpickle_string(thing):
    """
    Turn a pickled string back into a Python object
    """
    instream = StringIO.StringIO(thing)
    in_pickle = pickle.Unpickler(instream)
    retval = in_pickle.load()
    instream.close()
    return retval

class ProcessFeeds(LoggingHandler):
    """
    Process feeds from a particular date range
    (by default all of the previous day), and
    persist them to the datastore and memcache
    """

    def get(self, daystring=None):
        """
        As this will generally be run via cron, 'get' is the primary handler,
        even though logically this is more of a 'post' action
        """
        daystring, day = misc_funcs.validate_date(daystring)

        ### Get the relevant feeds from datastore
        feeds = get_feeds_covering_date(day)
        logging.debug("Got %d feeds for %s" % (len(feeds), daystring))

        ### Process the feeds
        package_list = simplify_feeds.simplify_feeds([f.xml for f in feeds])
        logging.debug("%d packages/families for %s" % (len(package_list),
                                                       daystring))
        ### Save feeds to datastore
        pkl = make_pickle_string(package_list)
        daypkg = models.DayPackages(key_name = daystring,
                                    day = day,
                                    day_string = daystring,
                                    pickled_data = pkl)
        daypkg.put()

        # Sanity check
        try:
            unpick = daypkg.unpickle()
        except TypeError, e:
            logging.error("TypeError thrown - pickle can't be unpickled [%s]" %
                          (e))
        self.redirect("/updates/" + daystring)

    def post(self, dontcare=None):
        """
        This is just for manual triggering from the admin page.  Unlike the
        HTTP 'get' method version, it takes the date from 3 form inputs, not
        the URL
        """
        # Cast to ints as some perfunctory validation
        daystring = "%04d%02d%02d" % (int(self.request.get("year")),
                                      int(self.request.get("month")),
                                      int(self.request.get("day")))
        logging.debug("ProcessFeeds.post: daystring is '%s'" % (daystring))
        self.get(daystring)


app = webapp2.WSGIApplication(
    [
        (app_settings.OFFLINE_PREFIX + "downloadFeed", DownloadFeed),
        (app_settings.OFFLINE_PREFIX + "processFeeds(.*)", ProcessFeeds)
        ], debug=True)

