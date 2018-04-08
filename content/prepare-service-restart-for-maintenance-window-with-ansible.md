Title: Orchestrate a service restart during a maintenance window with ansible
Date: 2016-06-18 16:39
Tags: ansible
Status: published
Summary: Ansible - Orchestrate changes to restart a service later

![Ansible daemon orchestration]({filename}/images/button.jpg)

## Introduction

Someone recently asked me:

"How do I run all the playbooks as usual, but make sure that ansible **DOESN'T** restart my service, and restart my service later?"

I didn't get the purpose of this question. I suspected it might have to do with how people write their playbooks, and how _possibly long_ playbooks must run to fit in tight maintenance windows.

The goal here was indeed to reduce the length of the maintenance windows by having ansible applying all the changes (like generating a daemon configuration), but handling the notifications for restarts at a later time. Of course, on the future run, most of the tasks should be entirely skipped and only the handler (the service restart) should run.

What you'll learn in this article is how to modify a role to get this behavior, not if it's a good idea or not. (Hint: It's not. Terrible idea. You should properly build your application/architecture to respond to signals, being HA-able and avoid these kind of tricks to **always be in a consistent state**.)

## I can haz code?

You can find all the examples/methods for this exercice in my [PoC repository][ansible-pocs], under the [conditionalhandler][ansible-pocs-service-restart] role.

For the sake of the simplicity, the tasks are tagged with the name of each method they belong to, and have additional tags like ```service_config``` (for the tasks simulating a service configuration generation) or ```service_restart``` (for the tasks simulating a service restart).

With this simple example, a standard task and a handler are enough to represent a real life example. The method here will explain what's needed on top of these two steps to bring this "timely" restart feature.

If you're testing these, please add ```-e "changed=True"``` if you want to simulate a service configuration change.

## How would you do this?

### Method 1: Use an intermediary handler

My initial thought was to trick ansible's handlers/notification systems.

Remember this: if you have a *generate service configuration* task notifying an intermediate handler task named *handling service restart* instead of directly notifying the *service restart* handler task, the only way to have a conditional behavior on the *service restart* task is using a variable (i.e. using a ```when: ``` clause). Using the tags system won't work for this case.

In other words, this:

    ansible-playbook conditional-handler-playbook.yml -t method1 --skip-tags=service_restart -e "changed=True"

will always run the *service_restart* tagged task. So this is not the intended behavior.

### Method 2: Introduce two variables, a task and make the tasks run conditionally on these variables

You can define in your role's default variables the following:


    # Set this to False to deny service restarts after a configuration change
    conditionalhandler_allow_restart: True
    # Set this to True to always restart the service.
    conditionalhandler_force_restart: False

A new task would be required to handle the force restart, while a condition should be added to the *service restart* handler.

For me, this is the least elegant way of doing it. This is really verbose, and requires variables that could be avoided. Readability is possible thanks to proper variable names. Replace the variable names by a and b, and read the code again. It will be far more difficult to read.

Generating the configuration without restart is done by executing:

    ansible-playbook conditional-handler-playbook.yml -t method2 -e "conditionalhandler_allow_restart=False"

Forcing the *service restart*:

    ansible-playbook conditional-handler-playbook.yml -t method2 -e "conditionalhandler_force_restart=True"

### Method 3: Remove the handler, use register and add one variable

In this method, the *service restart* isn't run as a handler, but as a standard task.
This *service restart* task can therefore run traditionally (when *generate service configuration* get its status as "changed") OR
run when the new variable ```conditionalhandler_force_restart``` is set to  ```True``` .

Avoiding/forcing a *service restart* becomes respectively:

    ansible-playbook conditional-handler-playbook.yml -t method3 --skip-tags=service_restart
    ansible-playbook conditional-handler-playbook.yml -t method3 -e "conditionalhandler_force_restart=True"

### Method 4: Using a marking file and flushing handlers (or a post_task)

In this method, we'll have one more task, one more handler. We don't use ansible ```register:``` directive and we don't add additional variables. We just make sure everything runs in two steps, by having either a post_task or a ```flush_handlers``` meta. The ```flush_handlers``` makes possible to execute the handlers, and then continue with the tasks. Here it's what we need to have a temporary file created and/or deleted (depending on the case).

Avoiding/forcing *service restart* is respectively:

    ansible-playbook conditional-handler-playbook.yml -t method4 --skip-tags=service_restart
    ansible-playbook conditional-handler-playbook.yml -t method4 --skip-tags=service_config

## Final Words - What is the most elegant way to do it?

My preferred method is the method 4, because it's far more readable, it avoids variable crawl, the tags are consistent, and it's understandable from a "non ansible" point of view. As I said before, the most elegant method would be to **NOT** do this at all, and make sure the system is always consistent after a run. Don't forget that some services don't require a restart to change their live status. Another signal could be used to take the change into consideration. This signal should be then used in the ansible handler.

[ansible-pocs]: https://github.com/evrardjp/ansible-pocs
[ansible-pocs-service-restart]: https://github.com/evrardjp/ansible-pocs/blob/de0ebf6945ed3df4b26e0c707fde5eb7ef1f86ed/roles/conditionalhandler/tasks/main.yml

*Photo credit: [Maker-9070](http://www.flickr.com/photos/135666453@N07/25128639121)*
