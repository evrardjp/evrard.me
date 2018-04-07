#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jean-Philippe Evrard'
COPYRIGHT = AUTHOR
SITENAME = u'dd if=/dev/brain of=/var/log/this.site'
SITEURL = 'https://evrard.me'
GOOGLE_ANALYTICS = "UA-79230364-1"

PATH = 'content'

STATIC_PATHS = ['images', 'pdfs','extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}

TIMEZONE = 'Europe/London'
DEFAULT_LANG = u'en'

FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_ATOM = 'feeds/atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Themes config
THEME = 'themes/JustRead'
USERNAME = 'evrardjp'
LINKEDIN_URL = 'https://www.linkedin.com/in/' + USERNAME
GITHUB_URL = 'https://github.com/' + USERNAME
SOCIAL = (
    ('', LINKEDIN_URL),
    ('', GITHUB_URL),
    ('', 'https://twitter.com/evrardjp'),
    ('', 'https://evrard.me/feeds/all.atom.xml'),
)
# LINKS = (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'))

# Plugins config
PLUGIN_PATHS = ['plugins']
PLUGINS = [
    'deadlinks',
    'tag_cloud',
]
## Deadlinks
DEADLINK_OPTS = {
    'timeout_is_error':    True,
}