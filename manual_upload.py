#!/usr/bin/env python
"""
Hack *for dev_appserver only* to take previously downloaded RSS files
and store them in the datastore.

To bulk upload a bunch of saved XML, use something like:
[john@hamburg sample_data]$ for X in *
> do
> curl --form file=@${X} "http://localhost:12346/uploadRSS"
> done

"""

__author__ = "John Smith, 2012 <code@john-smith.me>"

import logging
import sys
import os
import datetime
import re

from handler import LoggingHandler

import app_settings

import grab_latest_feed
import misc_funcs
import content

from feed_model import PyPIRSSXMLGAEModel

def get_timestamp(filename, return_datetime=False):
    """
    Given a filename of the form something_yyyymmddhhmm.something, return
    an appropriate datetime
    """
    date_bits = re.search("^.*_(\d\d\d\d)(\d\d)(\d\d)(\d\d)(\d\d).*$", 
                          filename)
    if date_bits:
        if return_datetime:
            return datettime.datetime(int(date_bits.group(1)), # year
                                      int(date_bits.group(2)), # month
                                      int(date_bits.group(3)), # day
                                      int(date_bits.group(4)), # hour
                                      int(date_bits.group(5))) # minute
        else:
            return "%s%s%s%s%s" % (date_bits.group(1),
                                     date_bits.group(2),
                                     date_bits.group(3),
                                     date_bits.group(4),
                                     date_bits.group(5))
    else:
        raise ValueError("%s does not seem to include a timestamp" % (filename))

def sniff_xml_encoding(xml_string):
    """
    Return an encoding (e.g. "utf-8") from the heading of an XML doc,
    or None if one could not be found
    """
    if xml_string[:5].lower() != "<?xml":
        # This is too strict I think, a valid XML could begin with whitespace
        # or maybe even comments?
        return None
    tag_end = xml_string.find("?>")
    if tag_end < 0:
        return 0
    header_tag = xml_string[:tag_end]
    encoding_stuff = re.search('.*encoding\s*=\s*[\'"]([^"\']*)[\'"]',
                               header_tag, re.IGNORECASE)
    if encoding_stuff:
        return encoding_stuff.group(1)
    else:
        return None

class UploadFeedFile(LoggingHandler):
    def post(self):
        """Accept a file upload and store it in the datastore"""
        if not content.is_dev_appserver():
            self.error(403) # Forbidden
            return

        file_arg = "file"
        if self.request.get(file_arg):
            file_ = self.request.POST[file_arg]
            if file_ is not None:
                # logging.debug("file_.value is type %s" % (type(file_.value)))
                encoding = sniff_xml_encoding(file_.value)
                if encoding:
                    unicode_content = file_.value.decode(encoding)
                rss = PyPIRSSXMLGAEModel(unicode_content,
                                         get_timestamp(file_.filename))
                rss.write()
                self.redirect("/Admin")
            self.error(400) # Bad Request
