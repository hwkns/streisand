[![Build Status](https://travis-ci.org/streisand/streisand.svg?branch=develop)](https://travis-ci.org/streisand/streisand)
[![Coverage Status](https://coveralls.io/repos/streisand/streisand/badge.svg?branch=develop&service=github)](https://coveralls.io/github/streisand/streisand?branch=develop)
[![Code Climate](https://codeclimate.com/github/streisand/streisand/badges/gpa.svg)](https://codeclimate.com/github/streisand/streisand)

streisand
=========

A private BitTorrent tracker backend written in python, django, and redis

To get started:
---------------

- install [Vagrant](https://www.vagrantup.com/) and [Ansible](http://docs.ansible.com/intro_installation.html)
- `cd` into the project root (next to Vagrantfile)
- `vagrant up`
- `vagrant ssh`

The `vagrant up` step might take a little while, but now you have everything you need to run
streisand!  In this environment, several alias commands are set up for your convenience.  To
start with, run this command to generate and run migrations and import initial fixture data:

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
