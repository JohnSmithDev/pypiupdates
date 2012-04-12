#!/usr/bin/env python
"""
Settings specific to PyPI that aren't anything to do with this app as such
"""

__author__ = "John Smith http://www.john-smith.me"


UPDATE_RSS = "http://pypi.python.org/pypi?%3Aaction=rss"
NEWEST_RSS = "http://pypi.python.org/pypi?%3Aaction=packages_rss"

# Just FYI (well my info)....
# XML-RPC docs:
# http://wiki.python.org/moin/PyPiXmlRpc
# http://wiki.python.org/moin/PyPiJson

# Example JSON request:
#  curl "http://pypi.python.org/pypi/bake/json"
# returns (as of 2012/03/11):
EXAMPLE_JSON_RESPONSE = """

{
    "info": {
        "maintainer": null, 
        "docs_url": "", 
        "requires_python": null, 
        "maintainer_email": null, 
        "cheesecake_code_kwalitee_id": null, 
        "keywords": null, 
        "package_url": "http://pypi.python.org/pypi/bake", 
        "author": "Jordan McCoy", 
        "author_email": "mccoy.jordan@gmail.com", 
        "download_url": "UNKNOWN", 
        "platform": "UNKNOWN", 
        "version": "1.0.0a1", 
        "cheesecake_documentation_id": null, 
        "_pypi_hidden": false, 
        "description": "UNKNOWN", 
        "release_url": "http://pypi.python.org/pypi/bake/1.0.0a1", 
        "_pypi_ordering": 1, 
        "classifiers": [
            "Development Status :: 3 - Alpha", 
            "Environment :: Console", 
            "Intended Audience :: Developers", 
            "License :: OSI Approved :: BSD License", 
            "Operating System :: OS Independent", 
            "Programming Language :: Python", 
            "Topic :: Software Development :: Build Tools", 
            "Topic :: Utilities"
        ], 
        "name": "bake", 
        "bugtrack_url": null, 
        "license": "BSD", 
        "summary": "A project scripting and build utility.", 
        "home_page": "http://github.com/jordanm/bake", 
        "stable_version": null, 
        "cheesecake_installability_id": null
    }, 
    "urls": [
        {
            "has_sig": false, 
            "upload_time": "2012-03-11T17:59:25", 
            "comment_text": "", 
            "python_version": "source", 
            "url": "http://pypi.python.org/packages/source/b/bake/bake-1.0.0a1.tar.gz", 
            "md5_digest": "f307d8e2a49ed39433ffbec05f31e5ce", 
            "downloads": 0, 
            "filename": "bake-1.0.0a1.tar.gz", 
            "packagetype": "sdist", 
            "size": 19765
        }
    ]
}"""


