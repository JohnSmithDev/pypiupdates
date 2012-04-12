#!/usr/bin/env python
"""
Take a bunch of PyPI 'update' RSS feeds, and
turn them into a cleaned up structure, e.g. no-dupes,
sorted a couple of different ways etc
"""

__author__ = "John Smith, 2012 <code@john-smith.me>"

import logging
import pdb
import time
import glob
import sys
import os

from thirdparty import feedparser

from package_classes import Version, Package, PackageFamily
from package_classes import get_package_name_and_version

def find_families(pkg_list):
    """
    Given a *sorted* list of Packages, return a dictionary of
    family names->[sub-packages], and a dict of packages->families.
    (The latter can be derived from the former, but lets avoid making work, eh?)
    Note that for our purposes, a family must have 2 or more packages
    """

    # First make a dict of family_name -> [Package(s)]
    family_dict = {} 
    for pkg in pkg_list:
        for sep in [".", "-"]:
            if pkg.name.find(sep) >= 0:
                fam, subpkg = pkg.name.split(sep, 1)
                if fam not in family_dict:
                    family_dict[fam] = []
                family_dict[fam].append(pkg)

    # Now:
    # a. Filter out the families with only one package
    # b. Build a reverse-lookup dict of package->family
    packages_in_families = {}
    families = []
    for fam_name in family_dict:
        if len(family_dict[fam_name]) > 1:
            family_dict[fam_name].sort()
            fam_obj = PackageFamily(fam_name, family_dict[fam_name])
            families.append(fam_obj)
            for pkg in family_dict[fam_name]:
                packages_in_families[pkg] = fam_obj

    return families, packages_in_families

def make_deduplicated_list_of_packages(feeds, filter_func=None):
    """
    Given a bunch of feeds, return a dict of package-name -> Package
    filter_func is an optional filter to ignore certain Packages e.g.
    if their date is outside a particular range.
    """

    processed_items = {}
    for f in feeds:
        d = feedparser.parse(f)
        for i, item in enumerate(d.entries):
            name, version = get_package_name_and_version(item)
            if name not in processed_items:
                pkg = Package.init_from_dict(item)
                processed_items[name] = pkg
            else:
                pkg = processed_items[name]
            if version not in pkg.versions:
                pkg.versions[version] = Version.init_from_dict(item)

    if filter_func:
        return filter(filter_func, processed_items.values())
    else:
        return processed_items.values()


def same_day_check(a_time, another_time):
    """Helper function to compare two time.time_structs"""
    return a_time.tm_year == another_time.tm_year and \
            a_time.tm_mon == another_time.tm_mon and \
            a_time.tm_mday == another_time.tm_mday

"""
Example of a filter that could be used in make_deduplicated_list_of_packages
Note that this is not just a pure True/False filter - it will also trim
out Versions that aren't from today.  (Is this bad style?)
"""

def filter_packages_by_day(day=None):
    """
    day is a time.time_struct, or leave undefined for today
    """
    if not day:
        day = time.gmtime()

    def filter_inner(pkg):
        """
        Closure function
        """
        filtered_versions = {}
        for ver in pkg.versions:
            if same_day_check(pkg.versions[ver].timestamp, day):
                filtered_versions[ver] = pkg.versions[ver]

        if len(filtered_versions) > 0:
            pkg.versions = filtered_versions
            return True
        else:
            return False

    return filter_inner


def simplify_feeds(feeds, filter_func=None):
    """
    Take bunch of feeds and return a (sorted) list that's more
    useful for us.
    'feeds' is a list of whatever feedparser.parse() accepts - could
    be a URL, file object or string
    """

    package_list = make_deduplicated_list_of_packages(feeds, filter_func)
    package_list.sort()

    # Work out what families are involved
    families, packages_in_families = find_families(package_list)

    # Now build a single sorted list that's a mix of Packages and
    # PackageFamilies as appropriate
    finalized_list = []
    processed_families = []
    for pkg in package_list:
        if pkg not in packages_in_families:
            finalized_list.append(pkg)
        else:
            fam = packages_in_families[pkg]
            if fam not in processed_families:
                finalized_list.append(fam)
                processed_families.append(fam)
    return finalized_list

def render_packages(package_list):
    """
    Simple text output
    """
    for thing in package_list:
        print(thing)
        if hasattr(thing, "packages"):
            for pkg in thing.packages:
                print("  %s" % pkg)

def main():
    feed_files = glob.glob(os.path.join("sample_data", "updates_*.rss"))
    yesterday = time.gmtime(time.time() - (24 * 60 * 60))
    yesterday_filter = filter_packages_by_day(yesterday)
    pkg_list = simplify_feeds(feed_files, yesterday_filter)
    render_packages(pkg_list)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)
    main()


