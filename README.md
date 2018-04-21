[![pipeline status](https://git.ronzertnert.me/JumpCut/JumpCut/badges/develop/pipeline.svg)](https://git.ronzertnert.me/JumpCut/JumpCut/commits/develop)
[![Build Status](https://travis-ci.com/TheSaltman/JumpCut.svg?token=omojFLEmKUq3bYx2FWE8&branch=develop)](https://travis-ci.com/TheSaltman/JumpCut)
[![coverage Report](https://git.ronzertnert.me/JumpCut/JumpCut/badges/develop/coverage.svg)](https://git.ronzertnert.me/JumpCut/JumpCut/commits/develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/e01280e1514e22ae0497/maintainability)](https://codeclimate.com/github/TheSaltman/JumpCut/maintainability)

# Jumpcut

A private BitTorrent tracker backend written in python, django, and redis

## To get started

- Install docker and docker-compose (TODO link)
- Run `docker-compose run web invoke clean-slate`

The `docker-compose` step might take a little while, but now you have everything you need to run
jumpcut!  In this environment, several alias commands are set up for your convenience.  To
start with, run this command to generate and run migrations and import initial fixture data:

- `docker-compose run web invoke clean-slate`

As the name suggests, that command will always bring you back to that starting state.

Currently the admin user password it creates is hashed and salted using argon2. I would recomment that you use the function:

- `docker-compose run web streisand/manage.py changepassword admin`

To run the dev server

`docker-compose up`

## Out of date - todo change

To enter a new password for testing. 

You may also add in fixtures to add in dummy forums, and 2 more users.

you can do this by entering:

- `m loaddata dev`

The users are api, and user1.

Now, for tinkering, it's fine to use Django's built-in server to run the site and/or the tracker:

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
