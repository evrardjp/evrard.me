---
date: '2018-04-08'
status: published
summary: 'Quite a few interesting changes in Ansible 2.5.'
tags: ["ansible"]
title: 'My view on Ansible 2.5'
slug: 'My view on Ansible 25'
---

Ansible 2.5 was released last month.

If you didn't read/hear about it, you should first read the [ansible
2.5 release
notes](https://www.ansible.com/blog/ansible-2.5-traveling-space-and-time),
[ansible 2.5
changelog](https://github.com/ansible/ansible/blob/e8beb180e15eff1f54e0ac8a5a5143639794bbdc/CHANGELOG.md#2.5),
and the [ansible 2.5 porting
guide](https://docs.ansible.com/ansible/devel/porting_guides/porting_guide_2.5.html).

Here is what I like and don't like about this release:

-   Each module documentation is far more readable. Look at the stat
    module [in
    2.5](http://docs.ansible.com/ansible/2.5/modules/stat_module.html)
    vs its documentation [in
    2.4](http://docs.ansible.com/ansible/2.4/stat_module.html) .
-   The module index documentation is far harder to automatically
    search. That's a big nuisance if you know your modules and want to
    quickly search for modules parameters for example.
-   While this isn't shown up in the release notes, we finally have an
    etcd module in ansible, for etcd3. The etcd2 module is still in the
    works, so is its lookup.
-   I do not have a strong opinion about using `loop:` vs `with_`. I
    just do not like the fact I will have to do a grep and replace for
    no foreseeable reason. It\'s replacing one evil with another. Same
    goes for replacing the pipe (\|) with [is]{.title-ref} for the
    conditions (Although I agree that the latter is more readable).
-   I like the namespace `ansible_facts`. In fact (*pun intended*), I
    prefer using namespacing in many places. I even suggested using this
    mechanism in `openstack-ansible` for automatic variable loading in
    test environment in a `test` or `required` namespace.
-   The ansible config lookup might be interesting in the future.
-   We now have new modules for InfluxDB, and grafana.
-   A [netns
    module](http://docs.ansible.com/ansible/2.5/modules/ip_netns_module.html)
    was introduced, to have basic functionality of creation/deletion of
    namespaces.
-   An interesting [package\_facts
    module](http://docs.ansible.com/ansible/2.5/modules/package_facts_module.html)
    has been introduced. It automatically registers the list of packages
    installed on the host in the host vars, under the `ansible_facts`
    namespace. Similarily, you can use the [service\_facts
    module](http://docs.ansible.com/ansible/2.5/modules/service_facts_module.html)
    to know the current state of a service.
-   A `vdo` module was added. If you want to know more about it, check
    out this page for [VDO
    install](https://rhelblog.redhat.com/2018/02/05/understanding-the-concepts-behind-virtual-data-optimizer-vdo-in-rhel-7-5-beta/),
    and for checking the [VDO
    benefits](https://rhelblog.redhat.com/2018/02/08/determining-the-space-savings-of-virtual-data-optimizer-vdo-in-rhel-7-5-beta/).

*I'd like to add a big thanks to ricardocarillocruz, gundalow, and
bcoca for their help on irc!*
