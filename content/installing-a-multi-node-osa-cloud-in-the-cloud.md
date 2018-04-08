Title: Installing an OpenStack-Ansible multi-node cloud in the cloud
Date: 2016-12-29 15:22
Tags: openstack-ansible
Status: published
Summary: It isn't difficult to build your own openstack-cloud with a distributed in cloud control plane.

![Your cloud-based OpenStack-Ansible cloud]({filename}/images/cloud-multi-node-title.png)

## Introduction

Installing openstack is not that hard, but it could be time consuming. When running your first installs, you probably want to prototype on instances instead of hardware, to shave time.
It is basically one of the "cloud" principles: Focus on your goal (a business man would have said "value"), and rely on your providers whenever possible.

So, for me, it makes 100% sense to deploy OpenStack-Ansible in the cloud. So what are the steps?

Note: This post's relevance can change overtime, as OpenStack and OpenStack-Ansible evolves.

## General overview

If you want to deploy your OpenStack-Ansible cloud in the cloud, here are the top level steps.

1. You want to have, like you would in hardware, an "OpenStack-Ansible"-ready operating system.
1. Because currently OpenStack-Ansible requires[^fn-network-requirements-explained] your nodes to be on the same management network, you probably want them connected in some way.
1. You then want to follow the usual steps for deploying ansible.

These steps are similar to steps needed to run OpenStack-Ansible nodes in your datacenter. The "cloud" nature brings more flexibility and constraints at the same time, so let's go through these a little further

In the future I'm presuming you have a host/node that can:

* do git operations (clone)
* run python and ansible
* connect to your cloud provider(s) to create your instances.

This node is NOT the deploy node (but it could), it's simply your laptop or whatever.

## Step 1: Prepare the operating system for OpenStack-Ansible

OpenStack-Ansible requires an Ubuntu 14.04 (up to Newton) or 16.04 (from Newton onwards) with specific packages. CentOS 7 is on the works, but let's focus on Ubuntu 16.04 for this exercice.
Using a cloud provider already makes sense: Ubuntu being popular, you probably don't have to roll your own image, everything is probably already ready to work. Give your ssh keypair, select ubuntu 16.04 and DONE!

Let's say for the sake of the exercice you've created the following instances in your cloud provider:

* deploy
* haproxy01
* haproxy02
* infra01
* infra02
* infra03
* compute01

You probably want to install:

* ``git``, ``python``, and some other ansible dependencies on the deploy node
* ``python2.7`` on haproxy nodes
* a recent kernel, ``python2.7``, enough RAM/disk on the infra nodes.

Please check the current requirements for your version in the OpenStack-Ansible installation/deployment guide.


You could do install these packages manually by running `` apt-get install x`` on each of those nodes.

If you're like me, you probably want to automate it.
Enters the preliminary step: Using ansible to prepare your operating systems.

> Warning: Using Ansible to bootstrap your hosts in order to deploy OpenStack-Ansible on your instances (one of these will be bootstraping Ansible for OpenStack-Ansible) can cause dizziness.
> But don't worry, we are not looping.

### Step 1.0 Preparing ansible inventory

To use Ansible, you better have an inventory. You cannot use the OpenStack-Ansible inventory at this point of the lab yet, so you need to write your own.

Ansible did most of the job for you by providing [dynamic inventories scripts][ansible-dynamic-inventory] for [AWS][ansible-aws-dynamic-inventory] or [OpenStack][ansible-openstack-dynamic-inventory] clouds.
Put these scripts under your ``inventory/`` and ``chmod +x`` them ([^fn-dynamic-inventories-fetching]). I am assuming you're creating your own repo or folder for this([^fn-my-repo-for-this])

The Ansible OpenStack dynamic inventory script relies on shade and your ``clouds.yaml`` (for example ``~/.config/openstack/clouds.yaml``), so make sure they are ready.

For user-friendliness, you may want to add in your `clouds.yaml`:

    ansible:
      use_hostnames: True
      expand_hostvars: False
      fail_on_errors: True

Check your inventory by issuing ``python <your inventory script> --list ``.

### Step 1.1 Targetting the proper nodes

Now that your Ansible inventory is ready, you can see its layout is flat, except if you have given metadata to your instances. This lack of groups could be problematic.

Two ways to fix this:

1. Make sure what you run is targetting the proper nodes by using an in-memory inventory features
1. Use the ansible inventory merge behavior and complete the inventory with a static inventory file to make your life easier.

For the in-memory inventory, you need tasks holding the group/host names. If these tasks are not using variables, you will prevent the reuse of the plays. If using variables, their location would be, in my opinion, far less obvious than the inventory (in play, in a variable file, in group/host vars, ...).

In this case, I think the solution two seems better. The node targetting should be done with an ansible inventory file (like an INI file) and benefit from ansible merge behavior.
So here is an extract of what you'd need in the INI file for this step:

    [pre_osa]
    infra01
    infra02
    infra03
    deploy
    haproxy01
    haproxy02
    compute01

Not that hard, right?

If you skipped the step 1.0, your only choice would be to write an INI file with the following content:

    [pre_osa]
    infra01 ansible_host=xx.xx.xx.xx
    infra02 ansible_host=xx.xx.xx.xx
    infra03 ansible_host=xx.xx.xx.xx
    deploy ansible_host=xx.xx.xx.xx
    haproxy01 ansible_host=xx.xx.xx.xx
    haproxy02 ansible_host=xx.xx.xx.xx
    compute01 ansible_host=xx.xx.xx.xx

Everytime you'd change your cloud node, you'd have to rewrite your ``ansible_host`` value. Tedious but ok for small tests too. Your pick.

### Step 1.2 Installing the OpenStack-Ansible requirements

Now, you need to install the basic requirements for Ansible.
This is technically required on the deploy node, but some other nodes may require them too. For safety, install the packages everywhere!

So, for Ubuntu you need the following:

    ansible pre_osa -m raw -a "test -e /usr/bin/python || (apt-get -y update && apt-get install -y python-minimal)"
    ansible pre_osa -m raw -a "apt-get update -y && apt-get install -y git build-essential python-simplejson libssl-dev libffi-dev bridge-utils"

> Note: The above commands don't specify a user or elevation method, nor the path to the inventory you just created. Adapt it to your needs.

> Note: The above commands only list the packages needed at the time of the writing of this article. Please check what is required in OpenStack-Ansible
  by checking the ``bindep.txt`` file in the root of your openstack-ansible repo. Or just install bindep and use it.

### Step 1.3 Test your ansible installation

You can now run:

    ansible pre_osa -m ping

And move on the real stuff.

### Step 2.0 Configure networking

#### Cloud multi-node problem statement

The odds are really high that your cloud provider will prevent you from having network traffic coming to/from multiple ethernet addresses for one network. In general, you have one tuple (IP, hardware address) per network configured at your provider.
Because OpenStack-Ansible is relying on bridging to put containers together on the same networks, only the host traffic will be able to go outside.
It's perfectly fine from an all-in-one (AIO) standpoint, because in this case the external world will only speak to the load balancer on the host, and the rest of the OpenStack traffic will stay inside the hosts and don't need external world forwarding.
This won't do in our multi-node scenario.

#### The solutions

You can do NAT, but I will not recommend it. This is a radical change from OpenStack-Ansible standard networking. You'll be on your own, probably will have issues with some software, and your future hardware deploy of OpenStack-Ansible will probably not be deployed with NAT for scalability reasons (therefore the reproducibility of this exercice is quite limited). On top of that NAT isn't really a good idea if you plan to have an OpenStack cloud from this century, i.e. with IPv6.

You could deploy all your OpenStack-Ansible components on metal instead of in containers. You'd then multiply the amount of cloud instances you need, and complexity. Also I'd rather have the same configuration for OpenStack-Ansible in my cloud deploy as I would have in my hardware deploy.

The other solution would be to encapsulate your Layer 2 traffic between your cloud instances: Your configuration won't change for OpenStack-Ansible, you'll only have different networking (and a smaller MTU in the case of cloud instances vs the hardware installation).
Keep in mind that there are many roles in the ansible galaxy to configure your networking for your needs.

#### Encapsulation and tunneling using VXLAN

Please note that [the OpenStack-Ansible repo][osa] hides a hidden gem [here, in the bootstrap-host role][bootstrap-host].
OpenStack-Ansible uses this role (located in the tests folder) in its CI testing for configuring many things required to deploy/configure OpenStack.

The bootstrap-host role has the ability to configure basic networking, but also VXLAN encapsulation.
If you want to use this role ([^make sure you have cloned and linked the repo]), you probably want to select only its networking bits. Create your own playbook, target your cloud nodes, include the bootstrap-host role, and run the playbook with the proper tags. It should look like this:

    ansible-playbook osa-cloud-multinode-networking.yml --tags=prepare-networking

> Note: the bootstrap-host role need the excellent ``config_template`` plugin to work. Make sure you have the plugin in your Ansible plugins path.
> You can override the plugins folder location by adapting your ansible.cfg file, or using environment variables.
> Alternatively, you may want to consider that the ``bootstrap-host`` role as a meta dependency to the ``openstack-ansible-plugins`` role, which makes possible to use the ``config_template`` easily.
> That's what I usually prefer.

Adapt variables to trick the ``bootstrap-host`` role into doing your bidding.

For example, my ``osa-cloud-multinode-networking.yml`` looks like this:

    ---
    - hosts: pre_osa
      vars:
        bootstrap_host_aio_config: no
        bootstrap_host_encapsulation_interface: "{{ ansible_default_ipv4.interface }}" #Assuming you only have one interface, a public one, you want to assign this as exit interface and encapsulation carrying interface
        bootstrap_host_public_interface: "{{ ansible_default_ipv4.interface }}"
        bootstrap_host_encapsulation_enabled: True #not really necessary to define it, but hell it doesn't hurt to be explicit.
      roles:
        - bootstrap-host

You probably want to give each of your nodes a ``node_id``. You can either assign the ``node_id`` in the inventory (node per node or in a group var), or defining it in the playbook (set_facts/vars):

    node_id: "{{ groups.pre_osa.index(inventory_hostname) }}"

The trick here is that the bootstrap-host can configure a VXLAN overlay between all your nodes. This will be used to encapsulate traffic for br-mgmt, br-storage, br-vxlan, and br-vlan!

#### Other solutions

There are many other solutions for solving this issue (I think of L2TPv3, L2VPN with MPLS/VPLS, Tinc, GRE, ...). If you're interested on how to do it in more details, contact me!

### Step 2.1 Verify network configuration

That's the simplest of the steps:

     ansible pre_osa -m shell -a "cat /etc/network/interfaces.d/*"
     ansible pre_osa -m setup

Alternatively, you can check the connectivity on the br-mgmt of the nodes by pinging the nodes manually.

### Step 3.0 Deploy and use!

From now on, the nodes will be "like if they were on the same layer 3", which should be enough for your OpenStack-Ansible deployment.

Use your br-mgmt IPs when configuring your conf.d/openstack_user_config and everything should be fine!

## Conclusion

Building overlays accross multiple datacenters/clouds is quite easy, and work by default in OpenStack-Ansible. Make use of it!

[ansible-dynamic-inventory]: http://docs.ansible.com/ansible/intro_dynamic_inventory.html
[ansible-aws-dynamic-inventory]: https://raw.github.com/ansible/ansible/devel/contrib/inventory/ec2.py
[ansible-openstack-dynamic-inventory]: https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/openstack.py
[evrardjp-github-osa-cloud-multinode]: https://github.com/evrardjp/osa-cloud-multinode.git
[osa]: https://github.com/openstack/openstack-ansible
[bootstrap-host]: https://github.com/openstack/openstack-ansible/tree/master/tests/roles/bootstrap-host
[^fn-network-requirements-explained]: We don't really require all the nodes to be in the same management network, but it makes your life quite simpler. This is the path chosen for this article.
[^fn-dynamic-inventories-fetching]: Please remind me to write a tool for that.
[^make sure you have cloned and linked the repo]: To use the bootstrap-host role, you have to clone the role in the appropriate folder!
[^fn-my-repo-for-this]: If you want, you can use mine [here on my github][evrardjp-github-osa-cloud-multinode]. WIP. I may have deleted this repo by the time of your reading. Please contact me if you want to see it.
