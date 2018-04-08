My view on Ansible 2.5
######################

:date: 2018-04-08
:tags: ansible
:status: published
:summary: Quite a few interesting changes in Ansible 2.5

Ansible 2.5 was released last month.

If you didn't read/hear about it, you should first read
the `ansible 2.5 release notes`_,
`ansible 2.5 changelog`_, and the `ansible 2.5 porting guide`_.


Here is what I like and don't like about this release:

* Each module documentation is far more readable. Look at the
  stat module `in 2.5`_ vs its documentation `in 2.4`_ .

* The module index documentation is far harder to automatically search.
  That's a big nuisance if you know your modules and want to quickly
  search for modules parameters for example.

* While this isn't shown up in the release notes, we finally have
  an etcd module in ansible, for etcd3. The etcd2 module is still
  in the works, so is its lookup.

* I don't have a strong opinion about using ``loop:`` vs ``with_``.
  I just don't like the fact I will have to do a grep and replace for
  no foreseeable reason. It's replacing one evil with another.
  Same goes for replacing the pipe (|) with `is` for the conditions
  (Although I agree that the latter is more readable).

* I like the namespace ``ansible_facts``. In fact (*pun intended*),
  I prefer using namespacing in many places. I even suggested using this
  mechanism in ``openstack-ansible`` for automatic variable loading
  in test environment in a ``test`` or ``required`` namespace.

* The ansible config lookup might be interesting in the future.

* We now have new modules for InfluxDB, and grafana.

* A `netns module`_ was introduced, to have basic functionality
  of creation/deletion of namespaces.

* An interesting `package_facts module`_ has been introduced.
  It automatically registers the list of packages installed on the
  host in the host vars, under the ``ansible_facts`` namespace.
  Similarily, you can use the `service_facts module`_ to know
  the current state of a service.

* A ``vdo`` module was added. If you want to know more about it,
  check out this page for `VDO install`_, and for checking
  the `VDO benefits`_.

.. _ansible 2.5 release notes: https://www.ansible.com/blog/ansible-2.5-traveling-space-and-time
.. _ansible 2.5 changelog: https://github.com/ansible/ansible/blob/devel/CHANGELOG.md#2.5
.. _ansible 2.5 porting guide: https://docs.ansible.com/ansible/devel/porting_guides/porting_guide_2.5.html
.. _in 2.5: http://docs.ansible.com/ansible/2.5/modules/stat_module.html
.. _in 2.4: http://docs.ansible.com/ansible/2.4/stat_module.html
.. _netns module: http://docs.ansible.com/ansible/2.5/modules/ip_netns_module.html
.. _package_facts module: http://docs.ansible.com/ansible/2.5/modules/package_facts_module.html
.. _service_facts module: http://docs.ansible.com/ansible/2.5/modules/service_facts_module.html
.. _VDO install: https://rhelblog.redhat.com/2018/02/05/understanding-the-concepts-behind-virtual-data-optimizer-vdo-in-rhel-7-5-beta/
.. _VDO benefits: https://rhelblog.redhat.com/2018/02/08/determining-the-space-savings-of-virtual-data-optimizer-vdo-in-rhel-7-5-beta/