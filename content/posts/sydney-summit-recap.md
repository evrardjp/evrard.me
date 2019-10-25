---
title: OpenStack Summit Sydney Recap
date: 2017-11-19
tags: ["openstack"]
status: published
summary: My personal view on the OpenStack Summit that happened in Sydney.
---
# The venue

Due to its remote location, the OpenStack Summit in Sydney was smaller than other summits I attended.
The venue was excellent, it wasn't hard to find the rooms, and everything was provided to be able to work constantly (energy, wifi, food, and the usual beverages!).
Sydney itself was a great location. The only downside was that nightlife in Sydney: it almost becomes a dead city after midnight!

# The sessions

OpenStack summits never lack interesting sessions. You have to balance what you want to attend and be a good time juggler, to capitalize every minute.
For this recap, I will separate my session overview in three tracks: The recorded sessions, the etherpad based conversations, and the hallway track.

## The recorded sessions

I usually skip this track because:

1. Sessions are recorded, so I can see them later
1. You can generally have 1-to-1 with presenters and attendees in the hallway track.

This summit was no different.

Kevin Carter, Amy Marrich, and I had our own recorded session for the OpenStack-Ansible project, named unsurprisingly "OpenStack-Ansible Project Update".
Sadly, due to technical issues, our session didn't run for its full 20 minutes length, and the presentation didn't meet my excellence criteria.
Next time, I'll prepare for the worst! If you want to see the extend of the new features we want to introduce during the Queens cycle, have a look at [this][2] instead.

I also attended the session "Practical k8s on OpenStack-Ansible". I am glad it had a proper attendance, but sad the session wasn't recorded. Well done Florian, I received good feedback from attendees!

## The etherpad based conversations

Those conversations are structured discussions, where the moderator lets the attendance discuss how to improve things on a specific topic, in non-interrupt based conversations.
I generally spend the majority of my time in those sessions.

The first session I attended was the ["OpenStack Health" session][1], talking about its relevance. I learned many things about the future of Zuul v3
dashboard there too, and how things will be improved in the future. I'll stay in touch with the team to learn more about these dashboards.

Our OpenStack-Ansible feedback session had a very good attendance. It had new, as well as existing faces, which is encouraging.
We mainly discussed Ansible's OpenStack modules, and offline installs. Here is what I take from the conversation:

* We need to improve our documentation for offline installs, and make it simpler by removing all external dependencies outside the apt/pip/git parts (LXC download template files, extra packages outside the repositories, cirros images...).
  Having an apt mirror, an PyPI server, and git repos should be enough to deploy OpenStack from source in an offline fashion.
  All of this was already planned for this cycle, so we are in sync with our community.
* We need to extend our test coverage for roles by testing idempotency of Ansible's OpenStack modules.
  Example: Designate role test should test the os_zone and os_recordset modules. On top of that,
  we could extend Ansible's test coverage by automatically testing changes in their OpenStack modules by using our role tests with the help of Zuul v3.

The "Installation Guide" changes session was interesting, talking about its relevance nowadays, and how to improve it.
Because there is no radical change on the installation guide, OpenStack-Ansible won't be impacted: the installation of OpenStack using OpenStack-Ansible is described in the "deploy guide".

The ["skip level upgrade" session][4] ended up by saying "We need a proper cross-project documentation that all projects can apply". Someone volunteered for the documentation, and I suggested to compare their work with our ["Leapfrog" work][5], available in our openstack-ansible-ops repository.

The [Privsep][6] session explained its impact on deployers in the future. Here is a short summary:

* Documentation will be written on how to use privsep (sudo rootwrap that contains privsep or sudo privsep directly). We will need to adapt our roles based on it.
* I conveyed the need to implement this in a standard way accross all the projects, to simplify deployer's life.

The ["stable policy"][7] conversation agreed that deployment tools have different needs than the other projects. We decided to make sure NO deployment project should have this tag,
and each deployment project can pick and choose what's best for its customers, because they are already opiniated.

A [Self-Healing SIG][8] was created, with as first action points creating mailing lists and IRC communication channels. There was a divergence of use cases already: Telcos wanted the self-healing to go as far as inside the openstack hosted applications. The group will first focus on the openstack applications themselves.
I reminded the group we should not be re-writing a monitoring solution, but instead creating a common base and/or modifying projects to fullfill our self-healing needs. The first item would be to implement a proper health checking system, usable by monitoring solutions and inside the self-healing framework.

The "Ansible Onboarding" session was a full house. The audience was split between Ansible beginners, OpenStack-Ansible beginners, and OpenStack-Ansible experienced users.
We covered the topic by browsing the docs, telling how it installs Ansible, and how everything works together, mentionning all the pain points people usually see.
I hope this will help those new contributors!

The "Ansible State of the Union" session was explaining where Ansible was, and is heading towards.
I currently don't see anything conflicting with our strategy. We can improve Ansible's modules by bringing real use cases, as mentionned above.

The "Neutron Pain Points" session was unsuccessful to me on one topic: Failure to agree there was a pain point for people who want to use OpenStack with Neutron like they would use VMware.
The rest of the session required some in-depth Neutron knowledge I didn't have.

Last, but not least, the (in my opinion, controversial) "Upstream LTS" session. I suggest you to visit the [etherpad of the conversation][9], and the etherpad of the ["after conversation"][10] to get a solid understanding of the issues.
I had plenty of hallway conversations about these topics, sharing my concerns on how things can go wrong, and how hard it will be to do it right.
There are other ways to solve the initial problem that spawned the need of an "LTS" for our users, but that's probably worth another blog post, and another series of discussions.

## The "hallway track"

The "hallway track" is my favorite part. Every OpenStack gathering (summit/PTG/mid-cycles) allows you to meet more and more people, whether they are long time contributors or
new community members. This summit was no exception. I got the chance to meet with people from my own country, from the other side of the world, and
this time also with people from down under which don't usually get the chance to travel to Europe or America. It was very nice to meet all of you!

Here are a few highlights of some "hallway track" conversations:

* Explained how to increase test coverage of the telemetry stack, with the hope of seeing the test matrix increased in roles and our integrated gates.
* Discussed with Miguel Lavalle (Neutron PTL) about the inclusion of OpenStack-Ansible neutron testing as non-voting jobs, like we do for Keystone, nova-lxd, and Dragonflow already. There was no opposition to this idea. With the addition of Glance and Neutron, only Cinder would be missing to have a compute starter kit fully tested with our deployment tooling before it even get tested in our integration repository.
* Talked with Jay Bryant (Cinder PTL) about how we can help him having a "standalone cinder" test in our cinder role.
* Launched the idea of a collaboration channel with the Ansible's team with the help of Ricardo Carrillo Cruz. This has to be followed up after the summit.
* Drafted "battle plans" on how to improve Dragonflow in Pike for Ubuntu. (Includes an etcd3 conversation).
* Prepared the work to spin off "config_template" outside of our plugins repo, to be able to use it as a meta dependency for any role, not only the OpenStack-Ansible ones (for example Sebastien Han's ceph-ansible, or Flavio Percoco's projects).

# Conclusion

I am glad people are still interested in Ansible, and using it with OpenStack. OpenStack-Ansible has a sweet spot for deployers that don't want to go for the full k8s experience to deploy OpenStack. We've proven once more our flexibility, by showing we are in line with our deployer needs, and demonstrating kubernetes can still be used (on top of your OpenStack-Ansible deployed cloud!).

[1]: https://etherpad.openstack.org/p/SYD-forum-openstack-health-feedback
[2]: https://git.openstack.org/cgit/openstack/election/plain/candidates/queens/OpenStackAnsible/evrardjp.txt
[4]: https://etherpad.openstack.org/p/SYD-forum-fast-forward-upgrades
[5]: https://github.com/openstack/openstack-ansible-ops/tree/master/leap-upgrades/
[6]: https://etherpad.openstack.org/p/SYD-forum-privsep
[7]: https://etherpad.openstack.org/p/SYD-stable-policy
[8]: https://etherpad.openstack.org/p/self-healing-rocky-forum
[9]: https://etherpad.openstack.org/p/SYD-forum-upstream-lts-releases
[10]: https://etherpad.openstack.org/p/LTS-proposal
