A review of OpenStack's LOCI and its extensibility
##################################################

:date: 2018-08-28
:tags: openstack
:status: published
:slug: openstack-loci-how-it-works
:summary: A review of the OpenStack LOCI project: how it works as of today, and how it can be adapted to your needs.

`LOCI`_ is a very simple openstack project focusing on building OCI images for OpenStack Services using a Dockerfile and a series of shell scripts.

Currently, 9 projects (Cinder, Glance, Heat, Horizon, Ironic, Keystone, Neutron, Nova, and Octavia) can be built with it.

Flexibility and extensibility
-----------------------------

`LOCI`_ is relying on passing arguments to the Docker image building for its flexibility.
It requires you to pass at least the "PROJECT" as CLI argument, to tell which OpenStack project you want to build.

The other parameters are optional. You can pass a base image as starting point (``FROM``) in argument if you do not want to build from the ubuntu base image.
Other variables can be provided, like your personal pip 'links' web mirror, or proxy settings.

The image building's shell scripts receives the appropriate arguments as environment variables.
Many shell scripts do not need any updating to leverage this flexibility. If your use case is not met, I doubt it would be a problem to change the scripts to adapt your use case.

On top of that, you can of course build a child image to your needs.

The build process
-----------------

The build process currently behaves like this:

1. *python* and *virtualenv* are installed on the base image, using distribution packages.
2. A system user is created for the project.
3. *virtualenv* is upgraded, unconstrained, in a virtualenv. I suppose if you want to have fully reproducible builds with no surprise on the virtualenv version, you could implement a bypass using a docker build argument.
4. *pip* get installed in previous virtualenv, unconstrained again. Previous comment applies here.
5. The *bindep* pip package and extra pip packages based on the project + profile (coming from a *pydep.txt* file at the root of the LOCI repo) are installed.

   If a wheel built image was created, its upper constraints file is used for the installation of those ``pydeps`` + *bindep* pip packages.
   These packages are installed in a binary form (only), from your pip mirror of choice.

   If no pip mirror can be trusted, it would be technically possible to implement a bypass by having an argument that flips the ``--only-binary`` parameter to ``--no-binary``, and copying your own constraints file.
6. The destination project is cloned with the user provided reference (default is master branch's HEAD).
7. The destination project, and any extra *PIP_PACKAGES* (should *PIP_PACKAGES* be not empty), are installed based on projects' *setup()* content.
8. Distribution packages are installed at this point using *bindep.txt* file.
9. Cleanup of installed distro packages (and other extra artifacts) happen, and allows the system to use global packages.

Security and reproducibility
----------------------------

While I did not have the chance to do a thorough security review, here is my opinion:
The "requirements" building, while optional, is in my opinion necessary for security.

`LOCI`_ can build wheels for all the openstack requirements' upper-constraints in your environment, which can then be published in a secure location for your next project building. It means you would rely on OpenStack security team's work, which would
eventually update the requirements/constraints of an upstream project by blacklisting an insecure python package.
If you do not build the wheels with the *LOCI requirements* project, there is no reason to think you will pass a constraints file matching your OpenStack projects versions. Therefore, you are probably using anything from PyPI matching each project's requirements, which can be very variable.

Build speed
-----------

The image building itself is quite fast, due to the simplicity of the process.
If you have a CI pipeline, you can first build your 'requirements' image, then use its artifact for all the other projects building in parallel, which should take around a total of 10 to 20 minutes maximum.

Gating expectations
-------------------

It is expected in the current gating process to expose the wheels built in the 'requirements' image on a web server. You cannot use locally built files, unless you carry your own patch changing the base Dockerfile.

Learning pace
-------------

Because the project itself is very simple, it is easy to track what is happening there.
It is easy to contribute, and a few minutes/hours should be enough to get a grip of the whole codebase.

Conclusions
-----------

`LOCI`_ is a very simple and efficient way to build OpenStack images. It relies on Dockerfiles, simple shell scripts, and the power of bindep to install OpenStack software from sources.

If you are looking for a way to build images based on distribution packages, there is little to no point of using `LOCI`_, as you could as well build your image with a simple Dockerfile and a command like ``zypper install ${PACKAGE_LIST}``.
But that would also mean you will have to package your software and its dependencies (maybe for two different versions of Python), handle package conflicts, and other packaging work.

The packaging can be completely avoided if you build from source relying on the python ecosystem, OpenStack creation of upper constraints, and bindep management by upstream team(s).

.. _LOCI: https://github.com/openstack/loci
