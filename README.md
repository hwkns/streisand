[![pipeline status](https://git.ronzertnert.me/JumpCut/JumpCut/badges/develop/pipeline.svg)](https://git.ronzertnert.me/JumpCut/JumpCut/commits/develop)
[![Build Status](https://travis-ci.com/TheSaltman/JumpCut.svg?token=omojFLEmKUq3bYx2FWE8&branch=develop)](https://travis-ci.com/TheSaltman/JumpCut)
[![Coverage Status](https://coveralls.io/repos/streisand/streisand/badge.svg?branch=develop&service=github)](https://coveralls.io/github/streisand/streisand?branch=develop)
[![coverage Report](https://git.ronzertnert.me/JumpCut/JumpCut/badges/develop/coverage.svg)](https://git.ronzertnert.me/JumpCut/JumpCut/commits/develop)
[![Code Climate](https://codeclimate.com/github/streisand/streisand/badges/gpa.svg)](https://codeclimate.com/github/streisand/streisand)

Jumpcut
=========

A private BitTorrent tracker backend written in python, django, and redis

To get started
---------------

- install [Vagrant](https://www.vagrantup.com/) and [Ansible](http://docs.ansible.com/intro_installation.html)
- `cd` into the project root (next to Vagrantfile)
- `vagrant up`
- `vagrant ssh`

The `vagrant up` step might take a little while, but now you have everything you need to run
jumpcut!  In this environment, several alias commands are set up for your convenience.  To
start with, run this command to generate and run migrations and import initial fixture data:

*If you come across any hanging issues in the Vagrant Up process, specifically during NFS mounting, you will need to make sure the Vagrant box has the necessary priveledges to log in.*

- Per the [Vagrant Website](https://www.vagrantup.com/docs/synced-folders/nfs.html):
> For *nix users, make sure to edit your /etc/sudoers file with visudo. It protects you against syntax errors which could leave you without the ability to gain elevated privileges.
> **For Ubuntu Linux , sudoers should look like this:**
Cmnd_Alias VAGRANT_EXPORTS_CHOWN = /bin/chown 0\:0 /tmp/*
Cmnd_Alias VAGRANT_EXPORTS_MV = /bin/mv -f /tmp/* /etc/exports
Cmnd_Alias VAGRANT_NFSD_CHECK = /etc/init.d/nfs-kernel-server >statusCmnd_Alias VAGRANT_NFSD_START = /etc/init.d/nfs-kernel-server start
Cmnd_Alias VAGRANT_NFSD_APPLY = /usr/sbin/exportfs -ar
%sudo ALL=(root) NOPASSWD: VAGRANT_EXPORTS_CHOWN, VAGRANT_EXPORTS_MV, VAGRANT_NFSD_CHECK, VAGRANT_NFSD_START, VAGRANT_NFSD_APPLY

- `clean_slate`

As the name suggests, that command will always bring you back to that starting state.  Now, for
tinkering, it's fine to use Django's built-in server to run the site and/or the tracker:

- `runserver`
- `runtracker`

But if you want to use a more production-like stack, you can run everything through uWSGI and
nginx:

- `start_tracker_uwsgi`
- `start_www_uwsgi`

If you do this, you will need to collect all the static files under one directory to be served
by nginx:

- `m collectstatic`

You will also need to start `celery` to coordinate background tasks (such as the handling of
announces):

- `start_celery`

All of the `start_<thing>` aliases have `stop_<thing>` counterparts.  Once you have everything
started up, you can visit <http://localhost:8000> in your browser to see the site, and you can
make requests to the tracker at <http://localhost:7070>.

For example, here is an announce request that will work with the fixture data that was loaded in
by the `clean_slate` command: <http://localhost:7070/16fd2706-8baf-433b-82eb-8c7fada847da/announce?info_hash=%89I%85%F9%7C%C2%5C%24n7%A0%7C%D7%C7%85%999%82%A7%CB&peer_id=-UT3400-111122221111&uploaded=721&downloaded=982&left=0&port=1337&ip=192.168.1.4>
