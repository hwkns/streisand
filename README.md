[![pipeline status](https://git.ronzertnert.me/JumpCut/JumpCut/badges/develop/pipeline.svg)](https://git.ronzertnert.me/JumpCut/JumpCut/commits/develop)
[![Build Status](https://travis-ci.com/TheSaltman/JumpCut.svg?token=omojFLEmKUq3bYx2FWE8&branch=develop)](https://travis-ci.com/TheSaltman/JumpCut)
[![coverage Report](https://git.ronzertnert.me/JumpCut/JumpCut/badges/develop/coverage.svg)](https://git.ronzertnert.me/JumpCut/JumpCut/commits/develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/e01280e1514e22ae0497/maintainability)](https://codeclimate.com/github/TheSaltman/JumpCut/maintainability)

# Jumpcut

A private BitTorrent tracker backend written in python, django, and redis

## To get started


- Install docker and docker-compose (TODO link)
- Run `docker-compose run api invoke clean-slate` to load up the default db data
- Run `docker-compose run api src/manage.py passwd admin` to set yourself a password for the admin
  user
- Run `docker-compose run api invoke fixtures` to load up the development fixtures (see bellow)

The `docker-compose` builds all the containers and sets up the database with our core fixtures.
This may take a while, but afterwards subsequant commands will be much faster

It is highly recommended that you add the following lines or simillar to your `~/.bashrc`:

    alias jc_i="docker-compose run api invoke"
    alias jc_m="docker-compose run api src/manage.py"
    alias jc_f="docker-compose run frontend"

## Starting a dev server

To start all the services and the development servers for the frontend and backend run:

    docker-compose up

This will bring up everything

You can find the api/django-admin server on <localhost:8000>, the frontend server on
<localhost:3000> and the tracker server on <localhost:7070>.

## Rebuilding containers

If you change 

a) The python requirements file in backend

b) Any frontend files not in frontend/src/ (this is because the place node_modules is installed
means we cannot mount the whole frontend directory as a volume)

you need to rebuild your local containers
by running:

    docker-compose build

There is no need to do this if you just change the source code for either the frontend or backend
(they are on docker volumes and changes should be loaded immediately)

## Useful Commands

- `jc_i clean-slate` or `docker-compose run web invoke clean-slate` without alias

This command resets the db and loads the core fixtures to revert to a starting state.

Currently the admin user password it creates is hashed and salted using argon2. It is reccomended 
that you use the function:

- `jc_m change-password admin` or `docker-compose run web backend/manage.py changepassword ` without
  alias

To run the dev server, tracker and frontend and the services needed for it.

`docker-compose up`

The main backend site/api is accessible on `localhost:8000`.

To enter a new password for testing. 

You may also add in fixtures to add in dummy forums, and 2 more users.

you can do this by entering:

- `jc_m loaddata dev` or `docker-compose run web backend/manage.py loaddata dev` (you should see
  now why the aliases are useful).

The users are api, and user1.

## Out of date - todo change

You will also need to start `celery` to coordinate background tasks (such as the handling of
announces):

- `start_celery`

All of the `start_<thing>` aliases have `stop_<thing>` counterparts.  Once you have everything
started up, you can visit <http://localhost:8000> in your browser to see the site, and you can
make requests to the tracker at <http://localhost:7070>.

For example, here is an announce request that will work with the fixture data that was loaded in
by the `clean_slate` command: <http://localhost:7070/16fd2706-8baf-433b-82eb-8c7fada847da/announce?info_hash=%89I%85%F9%7C%C2%5C%24n7%A0%7C%D7%C7%85%999%82%A7%CB&peer_id=-UT3400-111122221111&uploaded=721&downloaded=982&left=0&port=1337&ip=192.168.1.4>
