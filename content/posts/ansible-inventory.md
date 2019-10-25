---
date: '2018-04-09'
slug: 'convert-ansible-inventories-with-ansible-inventory-cli'
status: published
summary: 'ansible-inventory is an overlooked tool. Here is how you can use it.'
tags: ["ansible"]
title: 'ansible-inventory tips'
---

The `ansible-inventory` purpose is to *show Ansible inventory
information*, as stated by its `--help` message.

However, this quite youg CLI has an interesting trick up its sleeve.

Quick reminder, Ansible allows by default 4 kinds of inventories:

-   ini
-   script
-   host\_list
-   yaml

Interesting fact number 1: All the inventory types above can be given as
input of the `ansible-inventory` CLI.

Interesting fact number 2: The output of the `ansible-inventory` CLI is
a valid `json` inventory.

Interesting fact number 3: `ansible-inventory` can output inventories
into the `yaml` format.

You can therefore **use ansible-inventory to chain, merge, or convert
ansible inventories**!

Here is an example of how it can be used:

The first type, `ini` inventories, is the what you probably have seen in
your first usage of ansible, and may look like this:

``` {.ini}
[glance_api]
localhost ansible_connection=local

[glance_registry]
localhost2 ansble_connection=local

[glance_all:children]
glance_api
glance_registry
```

This `ini` file can therefore be converted into a `yaml` file:

``` {.shell-session}
$ ansible-inventory -i inventory.ini -y --list > inventory.yaml
```

The resulting `yaml` file would be:

``` {.yaml}
all:
  children:
    glance_all:
      children:
        glance_api:
          hosts:
            localhost:
              ansible_connection: local
        glance_registry:
          hosts:
            localhost2:
              ansble_connection: local
    ungrouped: {}
```

If the `-y` was omitted, the output would be a `json` inventory:

``` {.shell-session}
$ ansible-inventory -i inventory.ini --list > inventory.json
```

Looking like:

``` {.json}
{
    "_meta": {
        "hostvars": {
            "localhost": {
                "ansible_connection": "local"
            },
            "localhost2": {
                "ansble_connection": "local"
            }
        }
    },
    "all": {
        "children": [
            "glance_all",
            "ungrouped"
        ]
    },
    "glance_all": {
        "children": [
            "glance_api",
            "glance_registry"
        ]
    },
    "glance_api": {
        "hosts": [
            "localhost"
        ]
    },
    "glance_registry": {
        "hosts": [
            "localhost2"
        ]
    },
    "ungrouped": {}
}
```

As you might have noticed, there is **no** `json` inventory type. The
`json` is the standard interface used for the \"script\" inventory type.

A valid inventory \"script\" (also named *dynamic inventory*), is an
executable which, when called with `--list`, outputs a `json` whose
content is following ansible conventions, like the `json` above.

As such, the `json` above can be converted into a dynamic inventory
script, by making it executable and showing its content.

Create a file `yourscript.sh` with the following content:

``` {.bash}
#!/bin/bash
cat <<EOANSIBLESCRIPT
<the content of the yaml above>
EOANSIBLESCRIPT
```

and then `chmod +x yourscript.sh`.

That file can now be converted into `yaml` with:

``` {.console}
$ ansible-inventory -i ./yourscript.sh -y --list > inventory.yaml
```

Hope it helps you understand what can be done with the
`ansible-inventory` CLI!
