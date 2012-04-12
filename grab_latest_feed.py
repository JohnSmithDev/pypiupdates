#!/usr/bin/env python
"""
Pull the 'update' RSS feed from pypi.org and store it somewhere.
No processing is done on the feed itself

"""

__author__ = "John Smith, 2012"

import logging
import urllib 
import os
import datetime

import pypi_cfg
import misc_funcs

class PyPIRSSDownload(object):
    """
    Base class for downloading the RSS feed - you probably
    want to create a subclass with a .write() method to persist
    the downloaded data to a DB, filesystem etc
    """
    def __init__(self, xml_content=None, timestamp=None):
        """
        Create an object either by downloading the XML from PyPI, or
        using presupplied data.  (The latter case is intended just for
        test scenarios.)
        """
        # TODO: some sort of timeout/retry functionality

        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = misc_funcs.make_timestamp()

        if xml_content:
            self.content = xml_content
        else:
            resp = urllib.urlopen(pypi_cfg.UPDATE_RSS)
            # TODO: Check HTTP response code etc
            self.content = resp.read()

    def __repr__(self):
        return "Feed downloaded at %s, %d bytes" % (self.timestamp,
                                                    len(self.content))

class PyPIRSSXMLFile(PyPIRSSDownload):
    """
    Class to save downloaded RSS XML to filesystem
    """
    def write(self, path=".", filename=None):
        if filename:
            pathname = os.path.join(path, filename)
        else:
            pathname = os.path.join(path,
                                    "updates_" + self.timestamp + ".rss")
        with open(pathname, "w") as output:
            output.write(self.content)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)
    feed = PyPIRSSXMLFile()
    feed.write("sample_data")


