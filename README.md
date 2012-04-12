# Python Package Updates #

## Overview ##

An App Engine based system to provide information about new and updated
packages in [PyPI](http://pypi.python.org)
(aka The Cheese Shop), that tries to address some of the
issues I have with [the RSS feed](http://pypi.python.org/pypi?%3Aaction=rss)
and the [@pypi](http://twitter.com/pypi) Twitter account.

## The problems with the RSS feed and Twitter account ##

Basically, it's the fact that PyPI is a victim of its own success.
There are so many packages being added and updated, that

1. The RSS update feed lists 40 items at a time, which usually only covers
   a period of a few hours, so you can easily miss stuff
2. The Twitter account is very noisy - it's fine if you're using something
   like TweetDeck, but if you're using the Twitter site or the official
   apps, you may find it drowns out the rest of your feed.

Further, some packages get updated multiple times in quick succession,
and the repeat tweets/RSS items get a bit annoying (especially as there's
no indication of the nature of the changes between versions, not that this
is currently addressed by this app either.)

Also, the RSS and Twitter feeds are ordered solely by time, which isn't
necessarily the best way of grouping packages.

## What this code does ##

1. It pulls the 'update' RSS feed from pypi.org at regular intervals
2. Once a day, it processes the last 24 hours worth of feeds and
   turns it into something a bit more structured
3. This is made available as a webpage
4. **TODO** There'll also be some form of daily email that people can
   subscribe to


