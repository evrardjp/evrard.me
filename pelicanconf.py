#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os
import glob
import yaml


AUTHOR = u'Jean-Philippe Evrard'
COPYRIGHT = AUTHOR
SITENAME = u'dd if=/dev/brain of=/var/log/this.site'
SITEURL = 'https://evrard.me'

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
TWITTER_USERNAME = USERNAME
TWITTER_URL = 'https://twitter.com/' + TWITTER_USERNAME
LINKEDIN_URL = 'https://www.linkedin.com/in/' + USERNAME
GITHUB_URL = 'https://github.com/' + USERNAME
SOCIAL = (
    ('', LINKEDIN_URL),
    ('', GITHUB_URL),
    ('', TWITTER_URL),
    ('', 'https://evrard.me/feeds/all.atom.xml'),
)
# LINKS = (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'))

FOOTERTEXT = '<a href="%s/pages/license.html">© 2017 %s</a>' % (SITEURL, AUTHOR)

# Plugins config
PLUGIN_PATHS = ['plugins']
PLUGINS = [
    'deadlinks',
    'tag_cloud',
]
## Deadlinks
if os.environ.get('DEADLINK_VALIDATION', True) != "False":
    DEADLINK_VALIDATION = True
DEADLINK_OPTS = {
    "classes": ['deadlink'],
}
## Comments with Staticman
STATICMAN_COMMENTS = True
COMMENTS_PATH = "./content/comments"

def loadyamlcomment(file):
    with open(file) as stream:
        return yaml.load(stream)

COMMENTS = [loadyamlcomment(f) for f in glob.glob(COMMENTS_PATH + '/*.yml')]
