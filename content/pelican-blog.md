Title: Auto deployment of Pelican webpages to github user pages
Date: 2016-06-05 22:30
Tags: python, blog
Status: published
Summary: Here is how I build my static website using tox and pelican

![Mon calepin ecrit avec pelican]({filename}/images/pelican.jpg)

# Introduction

As you may already have seen, this website is static html. I want to share how I do it.
My goals:

- have the technical out of the way when writing content
- have an automated way of publish content
- be simple to use wherever I am

**TL;DR**: I have a [tox configuration][tox.ini] that does the heavy lifting for publishing content written with pelican, check how it's done on the appropriate [github repo](https://github.com/evrardjp/evrardjp.github.io-sources/)

# Pelican

# Multiple solutions for the automation

So I had multiple choices:

1. Integrate with a CI/CD like [Travis CI](http://zonca.github.io/2013/09/automatically-build-pelican-and-publish-to-github-pages.html), semaphore (my two favorites) or jenkins.
2. Work in a [manual way](http://mathamy.com/migrating-to-github-pages-using-pelican.html).
3. Use git hooks.
4. Use [tox][tox]

The first solution is simple to setup and relies on a lot of different parties ("vendors").

The second seems more tedious on the long run.

The git hooks is more contained (it's pure git without fuss!) but requires to either have a proper git server that will handle my python builds, or a way to setup the client hooks and/or dependencies on the node that is used for writing the blog.

As I'll host everything on a public git (github in my case), I decided to go for the last one. The github server hooks are limited to curl things, So I can't have proper testing there. And because I want an easy clone/work way of things, I can't use use client side hooks. That's why I'll use [tox][tox] for testing.

# Tox to the rescue

If you don't know [tox][tox], I invite you to look at this wonder. In our case here, it's basically a python's virtualenv-aware make command. It's a good python automation & testing tool.

Thanks to tox behavior, I can just focus on content: The tox.ini will hold the information about the commands to run (I'll definitely forget these, so having one ini file as a reminder is good for me!) and run each test in its own virtualenv, which I find good for avoiding pollution on your "writing node".
The requirements for this "writing node" is simple: python, tox, and virtualenv.
If you really want to reduce your host dependencies, you could even run tox in a virtualenv.

So, I have one repo with my environment, holding the pelican and tox configuration files, the markdown-rst-whatever files and other static content.
When I want to work, I clone this repository and use my text editor to write in content/. Simple, right?

Let's have a look at my [tox.ini configuration file][tox.ini]:

## sdist

One of the first steps invoked when running tox is ``python setup.py sdist``, that should generate your `package.zip`.

In our case, we don't have a `setup.py` or `setup.cfg` holding our code. We're barely using python stuff.
So, we can skip this step by setting:

    skipsdist = true

## the virtual envs creation

Tox then creates the virtualenvs. There are lots of ways to affect this, I invite you to check at the [tox documentation][tox].
Tox, by default, creates its virtualenvs in `.tox/` folder. Every tox command will create its own virtualenv inside this folder.

I defined two different virtual environments, one for the linting (facultative), and one for pelican jobs. I want to keep them separate because they can have different dependencies.

## Inside the virtualenvs

So, the next steps for tox is to calculate/install the dependencies.

tox reads the `deps` section of each environment configuration (if any). This overrides the default `testenv` deps configuration.

tox then installs the result of the ``python setup.py sdist`` (for example, a `package.zip`). Here this step is skipped.

tox reads the `command` section relative to the virtualenv to run the job.

### The linters case

I have a "linters" test command (``tox -e linters``), that is used for ... linting the restructured text files, obviously.

The linter tool is not being nice with the others, and like I said before, I've isolated the linter tool from the others. It has therefore its own configuration section, to setup a different list of dependencies. For the linters, I just needed [restructuredtext_lint](https://pypi.python.org/pypi/restructuredtext_lint) as dependency.

For the `command` part, I wrote a small python script that dumps (in a friendly manner) my next mistake.

### the pelican virtualenv

My main `testenv` section is for my pelican work. This section has multiple commands: one that can generates the content with the testing profile (`build`), watch for saves changes (`watch`), serve the web content using [twisted][twisted] (`serve`) and finally deploy to production (`publish`).

To avoid having multiple virtualenvs (one per command), I make sure that all the commands have the same environment by setting `envdir` in `testenv`:

    envdir = {toxinidir}/.tox/functional

Because `testenv` is the parent and `testenv:linters` inherit from it, the previous change made linters' virtualenv the same as the others.
Thefore, I need to override the linters's envdir configuration:

    envdir = {toxinidir}/.tox/linters

It means that the linters virtualenv is now unlinked (again) from the "functional" virtualenv.

## Last words

With the fact that python can easily be found on most OSes, I think this workflow is quite simple to follow.

[tox]:https://tox.readthedocs.io/en/latest/
[tox.ini]:https://github.com/evrardjp/evrardjp.github.io-sources/blob/9ae74fd7b532ca33c2aa14cbcd79a4d704bd802a/tox.ini
[twisted]:https://twistedmatrix.com/trac/

*Photo credit: [MDreibelbis](https://www.flickr.com/photos/68704638@N04/26835201760)*
