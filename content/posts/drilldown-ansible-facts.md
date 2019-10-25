---
title: Usage of ansible local facts
date: 2017-08-05
tags: ["ansible"]
status: published
summary: Drill down into facts.d usage
---

![facts-are-easy-to-check](/images/fact-check.jpg)


If you haven't looked at [ansible 'local' facts][1] yet, maybe this article will encourage you to do so.
Ansible 'local' facts is a very powerful tool to get information, statically or dynamically, on your hosts
WHEN the hosts are the authoritative source of truth.

The example in the documentation is so simple it could be overlooked. You should use it
if you don't already use facter or ohai.

# First usage

Let's start with the example of the documentation:

If you write a file named ``something.``**fact** into ``/etc/ansible/facts.d/``, you may use its
content as local fact by using:

    {{ ansible_local.something }}
after running the ``setup`` module.

So, if you have a file, named ``a.fact``, containing:

    [b]
    c=True

You could use ``{{ ansible_local.a.b.c }}`` for anything. Tasks, conditionals... (Remember you
could use set_fact for caching in your local play!)

As long as this file is readable under a json or a ini form, ansible will take it.

# So, when is it useful, and what could I use it for?

If you have to configure a software depending on its state, and that software doesn't
report to a centralized state management system, that's where your local fact will shine.

Example, you want to ensure your Galera cluster is in a correct state, and erase the state
of an incorrect node. For that, you may need to compare what each node "sees", and
therefore a centralized view can't help you.

You can write a script (let's call it ``galera.fact``) with the simple following content[^fn-galera]:

```sh
#!/bin/bash
echo '[cluster_status']
mysql mysql -e "SHOW GLOBAL STATUS LIKE 'wsrep_cluster_status'\G" | awk '/Value/{print "status="$2}'
```

Don't forget to mark it as executable.

You can now see the status of your node(s) by looking at
``{{ ansible_local.galera.cluster_status.status }}"``.

Very useful.

# What's the catch?

## Slowness

The local facts will slow up your playbooks!

Calling the setup module (which happens by default on a playbook unless
``gather_facts`` is set to ``no``) will trigger the "local" data generation.
If your script is slow to execute, you will have to face the slowdown.

On top of that, you'll carry extra variables in your vars/hostvars, which burdens
ansible on very large environments.

The alternative approach would be that your script pushes to a central local location,
like a redis k/v store, or etcd.

## Unfriendliness

To do an action when your galera cluster status is not "Primary", you'd have to ensure
the full fact chain is set. If you are not sure about whether your fact is
defined or not, you could end up writing a waterfall of checks just to
be able to read ``{{ ansible_local.galera.cluster_status.status }}``.

Example:
```yaml
  when:
    - ansible_local is defined
    - ansible_local.galera is defined
    - ansible_local.galera.cluster_status is defined
    - ansible_local.galera.cluster_status.status is defined
    - ansible_local.galera.cluster_status.status != "Primary"
```

Hopefully here, if you can install jmespath[3], ansible got you covered with the ``json_query`` filter.

You can run in this case:
```
  when: "{{ ansible_local | json_query('galera.cluster_status.status') | default('Error',True) != 'Primary' }}"
```

For your information, json_query will return an empty string, not an error, if the element is not found.
That's why I am using ``default('something',``**True**``)``.

# Recap

Ansible local facts is a double-edged sword.
It's very powerful to get a complete a view of your environment if you don't already
use another method. However, it comes with slowness.

I would still recommend use local facts as much as possible if you can't use a central approach, they
are more flexible and faster to write than writing an inventory, a var plugin, or an inventory plugin!


[1]: http://docs.ansible.com/ansible/latest/playbooks_variables.html#local-facts-facts-d
[2]: http://galeracluster.com/documentation-webpages/notificationcmd.html
[3]: http://jmespath.org/
[^fn-galera]: I know this example isn't the best, because you could use [galera notification scripts][2] better, but that's just an example.
