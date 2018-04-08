Title: ansible-galaxy, my journey to install golang
Date: 2016-10-02 09:22
Tags: ansible
Status: published
Summary: Finding a proper role in ansible-galaxy is painful

![ansible-galaxy install golang -- 404 - proper role not found]({filename}/images/ansible-galaxy-install-golang.png)

## Introduction

I wanted to self-host [transfer.sh][transfer.sh], and didn't want to start using docker or new tech.

**TL:DR;** As usual, I turned to ansible, and (as usual) I was disappointed by the quality of the roles on the [ansible-galaxy website][ansible-galaxy]. I wanted to submit PR to the best role, but at the end I'd have to modify it.

So, what is really the point of [galaxy.ansible.com][ansible-galaxy]? What could we do to make it better?

## The journey

[Transfer.sh][transfer.sh] is a simple tool to upload your files from the command line. It's server side is developped with go.
To install this in a repeatable fashion, I wanted to use the available roles in ansible-galaxy.

### First step: Search a role on the galaxy website.

To find the best role, I trust the other users. I check the download count.
I had 2 targets: one role with 192 downloads and one with 164.
I then asked myself: how is it possible that a popular language like golang doesn't have more download counts?

Obviously there was an issue.

### Second step: Verify if [galaxy website][ansible-galaxy] isn't borked again.

[galaxy.ansible.com][ansible-galaxy] has caused me a lot of pain in the past.
The most memorable for me was this one time where I could not import the latest version of my role, and hoped disabling/enabling it could help the situation. Obviously(?) the role disable worked, but the enable failed, and all shell scripts relying on the presence of this repo started to fail. When this kind of things happen at 6PM, you know you are gonna stay up late to introduce fixes everywhere. All the trust you have for this website is now gone.

Let's get back to the matter here. A simple refresh (or "back") on the page, shows me different results! Interesting.
I wonder how much people tried a terrible role because the best role was not shown in the results.

Let's see what we have now:

<a href="https://raw.githubusercontent.com/evrardjp/evrard.me/2d154fbf31f9666e37b578a5630394a824c08b66/content/images/ansible-galaxy-golang-roles.png">
![this seems a better listing]({filename}/images/ansible-galaxy-golang-roles.png)
</a>

Oh, that's better, 6k downloads! This is where my focus will be.

But before that, should I try once again? Do I really have only 10 records? I suppose I have at least 11 of them, since a new one showed up.
Let's try that search again.

<a href="https://raw.githubusercontent.com/evrardjp/evrard.me/2d154fbf31f9666e37b578a5630394a824c08b66/content/images/ansible-galaxy-golang-24-roles.png">
![There are 24 roles listed]({filename}/images/ansible-galaxy-golang-24-roles.png)
</a>

Finally, a proper list! So, I can now (after multiple tentatives) confirm there are 24 roles listed in the galaxy for golang.

On another note, did you notice that the role with the most downloads did not appear in the first PAGE of results when sorted by relevance?

### Third step: Elect the best role

Obviously [galaxy website][ansible-galaxy] relevance sort was not reliable, so I tried to sort with downloads.
There were 4 of them with more than 100 downloads.

The first one is supporting my distribution and installs the latest release of golang! Sadly, this could stop anytime, because the variables used for the version have to be manually set in default/main.yml . This seems brittle, but it will be fine if the maintainer of the role is answering to the community.

Let's therefore check the PRs!

* 2 open PR. Once from December last year, one in march this year. We are in september. That's a long period for triaging/fixing for a role that small.
* Now the closed PRs. There are many of them, some of them closed recently. A good sign. Many of them are basically jumping the version to a more recent one. It makes sense, that's what I've seen!

At that point, here are my options:

* PR to adapt the role to make it resilient to version changes
* Check the other roles

I decided to check the other roles, maybe the grass is greener on the other side of the fence.

The second in terms of downloads forced me to edit my ``ansible.cfg`` to change the hash_merge behavior. Terrible. It didn't support latest golang version either.

The third is installing latest version, but has a dependant role for something I can't explain yet. It also forces me to ``become:`` and ``become_user: root``, on top of having terrible task readability.

The last one was the debops one. debops has lots of roles, and probably fit use cases which isn't mine: I don't want to have this complex series of roles and dependencies, or being forced to use a playbook. Ansible should be simple.

I give the golang example here, but trust me, it's the same story for every single role I'm trying to install.

### Fourth step: Analyse how long would it take me to adapt the best role vs recreating one

This role has 6 tasks. I can keep 3 of them, and modify the rest.

I've decided to [adapt the role][evrardjp-golang-role] and [submit a PR][pr-to-initial-role]. My own golang role is still [published on the galaxy][evrardjp-golang-role-galaxy], until the PR are merged. It seems a good intermediary.

## Conclusion

Even basic roles that should be properly done are done in a terrible way. IMO, RedHat should now invest in:

*  a proper [galaxy][ansible-galaxy] website
*  implementing a way to cleanup old role based on community feedback on the galaxy website
*  ensuring roles on the [galaxy][ansible-galaxy] website are self-contained and concise. Reduce the relevance of roles based on the amount of dependencies, and at the same time, increase the relevance of roles with a minimum set of tasks.
*  ensuring the community understand and applies the best practices.

[ansible-galaxy]: https://galaxy.ansible.com
[transfer.sh]: https://github.com/dutchcoders/transfer.sh/
[evrardjp-golang-role]: https://github.com/evrardjp/ansible-golang/
[pr-to-initial-role]: https://github.com/jlund/ansible-go/pull/28
[evrardjp-golang-role-galaxy]: https://galaxy.ansible.com/evrardjp/golang/
