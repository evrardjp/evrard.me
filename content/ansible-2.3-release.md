Title: My view on Ansible 2.3 release notes
Date: 2017-04-21 23:28
Category: ansible
Tags: ansible, release
Status: published
Summary: WHOA, a lot of changes in this release. Again.

![Shutup and take my money]({filename}/images/Shut-up-and-take-my-money.jpg)


Ansible 2.3 was released. I'm pretty sure you've seen things online about it, and probably read the changelog.

Networking modules were a big thing this release.

So big, it's easy to overlook the rest.
Here are, in my opinion, many other things worth glancing over for 2.3 (discovered from commits, or from the [changelog][changelog]):

* ``ansible_user`` [doesn't work anymore][1] if you don't have a variable explicitly set (depends on your connection plugin). If you have facts gathered, you may want to use ```ansible_user_id```. This bug has already been fixed in the 2.3 branch and will probably be shipped in version 2.3.0.1
* [Vars precedence and inheritence][7] have changed. Please have a look at the docs for variable precedence. I have to test if it broke my ``vars_plugins``.
* module_utils for custom modules can be shipped with roles. \o/
* a ```passwordstore``` lookup was introduced (see also passwordstore.org). Maybe it was there before, but I can't remember it, and I love it.
* a ```keyring``` lookup was introduced.
* You can now have a more terse run output with the new ``dense`` callback plugin.
* ``YAML`` and ``pickle`` cache support! Interesting, I think I will prefer YAML compared to all of the existing cache plugins.
* There are new ```combinations``` and ```permutations``` filters.
* We now finally have ```archive```, long after ```unarchive```.
* New/Updated toys (modules) are available for ansible stats, wait for connection, nginx, openssl,
  jenkins groovy scripts, parted, tempfile, zfs, Clear Linux, HP ILO, FreeIPA, iso extraction,
  ldap, logstash, netapp, omapi, ovirt, serverless, openbsd, let's encrypt, the usual clouds, ...
* Time to flatten your package lists yourself again! _removed 'package' from default squash actions as not all package managers support it and it creates errors when using loops,
  any user can add back via config options if they don't use those package managers or otherwise avoid the errors._
  **Great**. Moar slowness.
* _Blocks can now have a name field_. I like this improved readability.
* SO MUCH WOW with strategies: _Default strategy is now configurable via ansible.cfg or environment variable_.
  That's a change I love, mainly because I now have a different way to use a strategy I wrote (with the help of Kevin Carter, see in [openstack-ansible-plugins][4]) without changing my playbook.
* There are changes in the way multiple ```--tags``` given in the CLI behave. On this note, if you're tired of all of these changes, you can use my/our tag filtering strategy ;)
* _restructured how async works to allow it to apply to action plugins that choose to support it_. Great, we'll have to adapt config-template action plugin, if need be.
* I am now forced to have a look at our custom connection plugin because of the multiple connection/retry behavior changes. For example:

    * _On platforms that support it, use more modern system polling API instead of select in the ssh connection plugin. This removes one limitation on how many parallel forks are feasible on these systems_
    * _added optional 'piped' transfer method to ssh plugin for when scp and sftp are missing, ssh plugin is also now 'smarter' when using these options_
    * On top of that, there were [other][6] [changes][8] [linked to connections/retries][10].

*  **I. FEEL. THE. DANGER.** : _Fixed issues with inventory formats not handling 'all' and 'ungrouped' in an uniform way_.
* ```Yum state: list``` now works with disable repo and enable repo.
* [Split on newlines when searching become prompt][5].
* LXC module doesn't have a problem with HOSTNAME in bashrc anymore.
* The ansible-galaxy init can now take a skeleton argument, and/or read env vars for skeleton role location.
* The message "skipping: no hosts matched" has returned!
* The apt_repository module got [a bug][9] fixed.

[1]: https://github.com/ansible/ansible/issues/23530
[changelog]: https://github.com/ansible/ansible/blob/v2.3.0.0-1/CHANGELOG.md#23-ramble-on---2017-04-12
[4]: https://github.com/openstack/openstack-ansible-plugins
[5]: https://github.com/ansible/ansible/commit/4a9c5d9574038b80d199daafc9d1273f8a659831
[6]: https://github.com/ansible/ansible/commit/eed240797aed30a0e42a9d2cb6cdded16d75fb5c
[7]: https://github.com/ansible/ansible/commit/a2599cab794e9a2b8af88c012028ef45756cc973
[8]: https://github.com/ansible/ansible/commit/1fe67f9f436595003f7951dd88159731e6d82498
[9]: https://github.com/ansible/ansible/commit/577d0e43ba339788989ecdf9a9da97477596ec6d
[10]: https://github.com/ansible/ansible/commit/d1a6b07fe1ceb8099abf763ac7e4bb4ebfaf1d3f
