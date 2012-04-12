#!/usr/bin/env python
"""
Definitions for classes related to packages
"""

__author__ = "John Smith, 2012 <code@john-smith.me>"

import logging
import pdb
import time
import glob
import sys

# Helper functions

def get_package_name_and_version(rss_dict):
    """Return the name and version of a processed item from the RSS feed"""
    # This seems like a really lame way to do it, but I can't see
    # any better alternative from the way the RSS data is structured
    return rss_dict.title.rsplit(" ", 1)

def get_versionless_url(rss_dict):
    """Strip the trailing version from the (first) URL in the RSS feed item"""
    # Again, this is a tad lame, but I can't see an alternative
    full_url = rss_dict.links[0].href
    base_url, dontcare = full_url.split("/", 1)
    return base_url

####

class Version(object):
    """A version of a package"""
    def __init__(self, version, timestamp):
        self.version = version
        self.timestamp = timestamp

    @classmethod
    def init_from_dict(cls, rss_dict):
        """Alternate constructor using feedparser.FeedParserDict"""
        dontcare, version = get_package_name_and_version(rss_dict)
        timestamp = rss_dict.updated_parsed
        return cls(version, timestamp)

    def __cmp__(self, another_version):
        """
        To make life easier for sorting lists of Versions.
        """

        # Prefer to use timestamps over version names as these should be
        # less prone to the vagaries of language
        if self.timestamp and another_version.timestamp:
            return cmp(self.timestamp, another_version.timestamp)
        else:
            # Cast to string just in case a numeric type sneaks in
            return cmp(str(self.version), str(another_version.timestamp))

    def __repr__(self):
        return "%s at %04d/%02d/%02d %02d:%02d" % \
            (self.version, self.timestamp.tm_year, self.timestamp.tm_mon,
             self.timestamp.tm_mday, self.timestamp.tm_hour,
             self.timestamp.tm_min)

class Package(object):
    """
    A package, with all the versions released in the time window we are
    dealing with
    """
    def __init__(self, name, url, description):
        self.name = name
        self.url = url
        if not description or description == "UNKNOWN":
            self.description = None
        else:
            self.description = description
        self.versions = {} # TODO: refactor to be a list?
    
    @classmethod
    def init_from_dict(cls, rss_dict):
        """Alternative constructur using feedparser.FeedParserDict"""
        name, dontcare = get_package_name_and_version(rss_dict)
        url = get_versionless_url(rss_dict)
        desc = rss_dict.description
        return cls(name, url, desc)

    def add_version(self, version, overwrite=False):
        """Add a Version, if it isn't already known (overridable)"""
        if version.timestamp not in self.versions or overwrite:
            self.versions[version.timestamp] = version

    def __cmp__(self, another_package):
        """For sorting lists of packages"""
        return cmp(self.name.lower(), another_package.name.lower())

    @property
    def version_list(self):
        v_list = self.versions.values()
        v_list.sort()
        return "; ".join([str(v) for v in v_list])

    def __repr__(self):
        return "Package %s - %s" % (self.name, self.version_list)

class PackageFamily(object):
    """
    Some packages are part of a bigger set e.g.
    ztfy.i18n, ztyfy.extfile, ztfy.worflow, etc on 2012/03/12
    It's nicer to merge these together
    """
    def __init__(self, name, packages=None):
        self.name = name
        if packages:
            self.packages = packages
        else:
            self.packages = []

    def __cmp__(self, another_family):
        """
        For easy sorting of lists of PackageFamily objects
        TODO: replace with __lt__() for better Py3 compat?
        """
        return cmp(self.name, another_family.name)

    def __repr__(self):
        return "Package family %s containing %d packages" % (self.name,
                                                             len(self.packages))

