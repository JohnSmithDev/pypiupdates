#!/usr/bin/env python
"""
Models for the Python Package notifications app
"""

__author__ = "John Smith, 2012 <code@john-smith.me>"

import StringIO
import pickle
import logging

from google.appengine.ext import db

class DownloadedRSS(db.Model):
    """The XML downloaded from pypi.org's RSS feed"""
    download_time = db.DateTimeProperty(auto_now_add=True)
    xml = db.TextProperty()

class DayPackages(db.Model):
    """
    Pickled list of all the Packages/PackageFamilies updated
    on a particular day
    """
    day = db.DateProperty()
    day_string = db.StringProperty() # same as 'day' really
    pickled_data = db.TextProperty()

    def unpickle(self):
        """
        Turn pickled_data property into something Python code
        can use
        """
        # Without casting self.pickled_data to string, you're liable
        # to get TypeError: decoding Unicode is not supported.
        # It's possible this isn't properly fixing the problem - but
        # the sample data I have doesn't seem to have genuine Unicode
        # characters in it; with the evidence I've got so far I can
        # only assume it's a quirk of datastore_types.Text
        
        instream = StringIO.StringIO(str(self.pickled_data))
        in_pickle = pickle.Unpickler(instream)
        retval = in_pickle.load()
        instream.close()
        return retval
