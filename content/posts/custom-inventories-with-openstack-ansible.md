---
date: '2018-08-31'
status: published
summary: 'You can now easily bring your own OpenStack-Ansible inventory'
tags: ["openstack", "ansible", "OSA"]
title: 'Custom Inventories with OpenStack-Ansible'
---

Over the years, many users of OpenStack-Ansible came to me with simple
requests: How can I add an ansible group into OpenStack-Ansible? How can
I add hosts to this group?

Please allow me to answer this in more detail here, with an explanation
of how OpenStack-Ansible inventories work.

The `openstack-ansible` CLI's inventory
========================================

One of the early steps of an OpenStack-Ansible deployment is ensuring
Ansible is installed, with its right version and environment. This is
done by our `bootstrap-ansible.sh` script.

During this process, we ensure `ansible` and `openstack-ansible`
commands are in the user's `PATH`[^1]. Both commands are, in fact, a
wrapper around Ansible's binaries with a little twist: We load
environment variables from an `openstack-ansible.rc`[^2].

This `openstack-ansible.rc` contains environment variables altering the
runtime behavior of Ansible. This is done thanks to Ansible itself
reading some predefined environment variables[^3]. One of these
environment variables is `ANSIBLE_INVENTORY`.

For your information, ansible<=2.3 only accepts one inventory at a
time. When the OpenStack-Ansible project was created, all the
flexibility had to be built into a single inventory.

That's how OpenStack-Ansible dynamic inventory appeared, with its
`env.d` appeared. The `env.d` is a way to structure the inventory seen
by Ansible. It is a very powerful but unfriendly mechanism. Its usage
has been described in OpenStack-Ansible's documentation for many
branches and releases now[^4].

However, because of the complexity behind it, many deployers struggle
adapting the configuration of the inventory.

This is one of the reasons I very early brought the idea of layering
inventories. My first attempt at it was a dynamic inventory (again!)
loading the usual OpenStack-Ansible dynamic inventory, and merging it
with a user provided static inventory.

This sadly increased complexity of the inventory code, but decreased the
complexity for the users to manage their inventory.

It was very easy to override default OpenStack-Ansible inventory, by
doing `export ANSIBLE_INVENTORY=/opt/my_own_inventory.py`.

Hopefully, this proof of concept never made it into OpenStack-Ansible
tree, as we would have increased the code complexity and made the system
harder to maintain.

After discussing with many people involved in Ansible (and particularily
interested in Ansible's inventory), I realised what we needed in terms
of inventories was matching other requests in the community.

Ansible 2.4 made possible to load and merge multiple inventories in one
command.

So when OpenStack-Ansible was updated to Ansible 2.4, I added the fact
to load, by default, a static `inventory.ini` next to the dynamic
inventory[^5].

How does this static inventory work in Queens?
==============================================

In Queens, you could add your own `inventory.ini` in
`/etc/openstack_deploy` and it would be taken automatically using the
openstack-ansible CLI. That would allow you to extend your inventory
with new hosts, and new host_vars and group_vars using static files,
which is easier to extend than env.d.

In fact, if you don't want to extend your inventory but add extra host
and group vars, the `openstack-ansible` wrapper automatically creates
the `inventory.ini` for you[^6].

However, there is no default structure present in OpenStack-Ansible
Queens, which forced users to a write a complete inventory for
OpenStack-Ansible in their `/etc/openstack_deploy/inventory.ini`.

So, what has improved in Rocky?
===============================

Before Rocky, users had to still rely on the OSA dynamic inventory to
get a basic deployment of Openstack-Ansible, and were only using this
static inventory to extend the dynamic inventory.

In Rocky, I ensured consistency and simplification of the playbooks'
targets.

I also introduced a default inventory file structure[^7], which allow
users to populate those groups to get a working deployment with only a
simple, static, inventory in userspace.

Here is an example for a bare-metal deployment.

``` {.ini}
aio1 ansible_connection=local ansible_host=127.0.0.1
# is_metal=True

## Setup hosts
[physical_hosts]
aio1

## Setup infra
[etcd_all]

[galera_all]
aio1
[haproxy]

[memcached]
aio1
[rabbitmq_all]
aio1
[repo_all]
aio1
[rsyslog]

[unbound]

[utility_all]
aio1

## Setup openstack
[keystone_all]
aio1

# Glance
[glance_api]
aio1
[glance_registry]
aio1

# Neutron
[neutron_agent]
aio1
[neutron_dhcp_agent]
aio1
[neutron_l3_agent]
aio1
[neutron_linuxbridge_agent]
aio1
[neutron_metadata_agent]
aio1
[neutron_server]
aio1

# Cinder
[cinder_api]
aio1
[cinder_backup]
aio1
[cinder_scheduler]
aio1
[cinder_volume]
aio1

# Nova
[nova_conductor]
aio1
[nova_api_placement]
aio1
[nova_console]
aio1
[nova_scheduler]
aio1
[nova_api_os_compute]
aio1
[nova_consoleauth]
aio1
[nova_api_metadata]
aio1
[nova_compute]
aio1

# Heat
[heat_api]
aio1
[heat_api_cfn]
aio1
[heat_api_cloudwatch]
aio1
[heat_engine]
aio1
```

The `openstack_user_config` has extra variables that would then be
missing. You can add them as group vars or extra variables (depending on
your needs). The minimum required variables to set up an
openstack-ansible deployment could look like the following:

``` {.yaml}
---
internal_lb_vip_address: 172.29.236.100
# The external IP is quoted simply to ensure that the .aio file can be used as input
# dynamic inventory testing.
external_lb_vip_address: "10.0.2.15"
rabbitmq_hosts_entries: []
neutron_provider_networks:
  network_types: "vxlan,flat"
  network_mappings: "flat:eth12"
  network_vxlan_ranges: "1:1000"
neutron_local_ip: "{{ ansible_host }}"
```

Conclusion
==========

With this article, I hope that you have enough information to extend the
inventories the way you want for your OpenStack-Ansible version.

[^1]: See also:
    <https://github.com/openstack/openstack-ansible/blob/7189ca7f1ed950944911c3418bf4afee47699315/scripts/bootstrap-ansible.sh#L157-L171>

[^2]: See also:
    <https://github.com/openstack/openstack-ansible/blob/master/scripts/openstack-ansible.rc>

[^3]: The predefined environment variables have changed over time. Check
    for example their definition as of today here:
    <https://raw.githubusercontent.com/ansible/ansible/653d9c0f87f681ac386864bad4cb48f0c5e2ddfe/lib/ansible/config/base.yml>

[^4]: See also:
    <https://docs.openstack.org/openstack-ansible/rocky/reference/inventory/understanding-inventory.html>

[^5]: See also:
    <https://github.com/openstack/openstack-ansible/commit/ba6a3ed899de5f0b98386c20e736f61e58807c9b>

[^6]: <https://github.com/openstack/openstack-ansible/blob/39b718a5c12779bc15d8efc432cbadbe69745323/scripts/bootstrap-ansible.sh#L245-L249>

[^7]: Extra structure for inventory.ini:
    <https://review.openstack.org/#/c/580368/5>
