Title: Group and host variables overriding in OpenStack-Ansible
Date: 2017-08-15 17:28
Tags: openstack-ansible, ansible
Status: published
Summary: How to override group/host variables into OpenStack-Ansible

![group-overrides]({filename}/images/Sergey_Svechnikov_large_buttons-small.jpg)


You probably know it already, Ansible has different means of overriding a
variable, and also different levels of precedence.
OpenStack-Ansible is no different, and ships with different levels itself.
I'll talk about the group and host variables here.

If you manage your own Ansible configurations, you probably have
roles (inside their defaults and vars folders) variables, playbook
variables, and you probably tie all of these up with group and
host vars. You probably have noticed that these variables are
often modified, and are the core of your Ansible installation.

Editing those is something highly inconvenient for an Ansible based
project that ships its own group/host variables: it
means your users have to edit the code of your project (for example,
OpenStack-Ansible), to match their needs.

We still have ways to override group and host vars in OpenStack-Ansible, but
it depends on what you need, and which branch you are on. Let's talk about that.

# For Pike

During Pike cycle, we moved the group variables into a [different folder][1].
This allowed us to use our [variables plugin][2], loading group and host
variables from different folders, with the precedence completely up to
the deployer (wiring can be seen [here][3], if you want to replicate this
in your own environment)

This series of commits allows you to override any group or host variable,
surgically. See also our [upstream documentation][4].

As usual, you could still use OpenStack-Ansible user variables, if you
want to set a variable for all your nodes. This has the highest level
of precedence, because it passes the user variable file in the CLI,
like you would if you were using
``ansible-playbook <...> -e @filename.yml``.

# For Newton, and Ocata

There was no consensus (yet) on whether or not OpenStack-Ansible
community should allow this backport of the variables into
the different folder. Newton and Ocata being
stable branches, it's unlikely that you'll be able to override
OpenStack-Ansible variables surgically, like you would in Pike.

The variable plugin is still loaded, which means you can still
have extra group variables and extra host variables, if need be.
It's a convenient way to add new variables, properly scoped, but
that won't help you if you want to override, for example
[lxc_container_config_list][5], for one or a group of hosts.

Let's see what is possible.

## The lxc_container_config_list example

For this example, we want to override ``lxc_container_config_list``
for ``cinder_api`` nodes.

The task creating the container and using this list uses
[two variables][6] you can technically override:
``lxc_container_default_config_list`` and ``lxc_container_config_list``.

### The simplest case

If you want to keep the ``lxc_container_config_list`` (the existing group
variable override), and add something on top, you could simply redefine
your ``lxc_container_default_config_list`` into your
``/etc/openstack_deploy/group_vars/cinder_api.yml`` (please double
check that the vars plugin is loaded for you, by having a look at
your ``in your /usr/local/bin/openstack-ansible.rc``).

### Overriding the group variable, elegantly.

Overriding the ``lxc_container_config_list`` would be different, because
the precedence would force you to use our user variables.

You could add into your own user variable file (let's say
``/etc/openstack_deploy/user_cinder.yml``):

    lxc_container_config_list: "{{ properties.lxc_container_config | default(['lxc.aa_profile=lxc-openstack']) }}"

So, you will be updating the lxc_config_list for all containers to the
lxc-openstack aa profile, but at the same time, you allow a container
property to override it!

You can then create your ``/etc/openstack_deploy/env.d/cinder.yml`` with
the following content:

    container_skel:
      cinder_api_container:
        properties:
          lxc_container_config: [ "lxc.aa_profile=unconfined" ]

However, you still need to ship env.d content for each of the groups
requiring a different value than ``lxc-openstack``. In other words,
in this case, you need to override the env.d content
for the cinder_volume and neutron_agent groups.

### Overriding the group variable, centrally.

There is an alternative:

You could directly use group membership inside your user variables!

Example:

    cinder_lxc_container_config_list: [ "lxc.aa_profile=override" ]
    others_lxc_container_config_list:  [ "lxc.aa_profile=lxc-openstack" ]
    lxc_container_config_list: "{% if 'cinder_api' in group_names %}{{ cinder_lxc_container_config_list }}{% else %}{{ others_lxc_container_config_list }}{% endif %}"

Or even better, if you want to add the cinder config list on top of the
existing ones:

    lxc_container_config_list: |-
      {% set config_list =  [] %}
      {% set _ = config_list.extend(others_lxc_container_config_list) %}
      {% if 'cinder_api' in group_names %}
      {% set _ = config_list.extend(cinder_lxc_container_config_list) %}
      {% endif %}
      {{ config_list }}

## Overriding a host variable.

What would you do if you need to override the cinder backends per host
on the storage hosts, and define their limit_container_types amongst
other data?

For that you can configure your ``conf.d/cinder.yml``:

    storage_hosts:
      aio1:
        ip: 172.29.236.100
        container_vars:
          cinder_backends: "{{ cinder_backends_per_host.get(inventory_hostname) }}"


After that, you have to configure a user variable, where
``cinder_backends_per_host`` is a dictionary, and each host of your inventory
would be a key:

    cinder_backends_per_host:
      aio1_aodh_container-c065ea73:
        limit_container_types: cinder_volume
        lvm:
          volume_group: cinder-volumes
          volume_driver: cinder.volume.drivers.lvm.LVMVolumeDriver3
          volume_backend_name: LVM_iSCSI
          iscsi_ip_address: "172.29.236.100"

# Conclusion

It is possible to override your group variables and host variables
in every version of OpenStack-Ansible. The more recent your version
is, the more streamlined and user-friendly your experience will be.
Stay up to date, because Ansible 2.4 will
probably bring changes improving things even further...

[1]: https://review.openstack.org/#/c/466379/
[2]: https://review.openstack.org/#/c/445447/
[3]: https://review.openstack.org/#/c/445437/
[4]: https://docs.openstack.org/openstack-ansible/latest/contributor/inventory-and-vars.html#variable-precedence
[5]: https://github.com/openstack/openstack-ansible/blob/73ee3eb9ae18add9c5c8a7872b736dddb129d8ce/playbooks/inventory/group_vars/all_containers.yml#L18-L19
[6]: https://github.com/openstack/openstack-ansible-lxc_container_create/blob/258dad41ced7f9511d4e388470a759f46d9509fa/tasks/container_create.yml#L143-L153
