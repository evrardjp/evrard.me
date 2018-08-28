Switching to the new gandi mail service
#######################################

:date: 2018-04-22
:modified: 2018-08-28 11:53
:tags: hosting
:status: published
:slug: opinion-on-new-gandi-email
:summary: I welcome the Gandi email service changes, but the web interface is plagued by issues.

If you are a Gandi customer, you probably already know they offer an email service.
What you might have missed, is Gandi's services refactor to be more modern.
Emails are following the same treatment, starting with the replacement of Roundcube.

The `new gandi email service`_ is based on `SOGo`_, and was introduced in January last year in `beta`_.

First, the impact of the change (not mentioning mailpack changes):

* New domains can only have the new service, and only 2 mailboxes are provided by default.
* Existing domains can keep their 5 mailboxes.
* The new service now has 3GB storage per mailbox, instead of the 1GB storage total.
* Switching to the new system prevents you from using the legacy platform and api,
  whether for renewing your domain or for managing your emails.
* The new webmail has a `new address`_.
* SOGo brings new features, namely CalDAV and CardDAV support.

Switching your domain to the new service
----------------------------------------

* Make sure you have a gandi v5 account on https://id.gandi.net
* Go to domains > (your domain name) > Email. There is a switch button
  on the page to use the new service.

If you DNS Servers are outside gandi, ensure you have the following records:

.. code-block:: text

    @ 10800 IN MX 10 spool.mail.gandi.net.
    @ 10800 IN MX 50 fb.mail.gandi.net.
    @ 10800 IN TXT "v=spf1 include:_mailcust.gandi.net ?all"

Next to that, configure CalDAV/CardDAV records for the DAV clients:

.. code-block:: text

    imap              IN CNAME access.mail.gandi.net.
    pop               IN CNAME access.mail.gandi.net.
    smtp              IN CNAME relay.mail.gandi.net.
    _caldavs._tcp     IN SRV 10 1 443 sogo3.gandi.net.
    _carddavs._tcp    IN SRV 10 1 443 sogo3.gandi.net.
    _imaps._tcp       IN SRV 10 1 993 mail.gandi.net.
    _submission._tcp  IN SRV 10 1 587 mail.gandi.net.
    _caldavs._tcp     IN TXT "path=/SOGo/dav/"
    _carddavs._tcp    IN TXT "path=/SOGo/dav/"

With all those records set, it should be easy for SOGo clients to work with your domain,
if they respect RFCs like the `RFC6764`_.

For Android, I strongly suggest you to use f-droid, and DAVDroid.
With the above records set, you can just add your email, and everything
will be auto-discovered.

Feedback
--------

The service's web interface is slow, terribly slow.
It prevents a daily usage as a gmail/google calendar replacement.
If you are only using another interface, like your phone, it is
easier to switch to this new service, as you will not miss
this new web interface.

The web interface option for WebCAL files seems broken.
The import of the `openstack combined releases calendar`_ comes up
just empty, while working perfectly fine in google calendar.

Thanks Gandi for this welcomed change!

.. _new gandi email service: https://news.gandi.net/en/2017/08/introducing-the-new-gandi-mail/
.. _beta: https://news.gandi.net/en/2017/01/introducing-sogo-new-webmail-service-in-beta/
.. _new address: https://sogo3.gandi.net/
.. _RFC6764: https://tools.ietf.org/html/rfc6764#page-4
.. _openstack combined releases calendar: https://releases.openstack.org/schedule.ics
.. _SOGo: https://sogo.nu/
