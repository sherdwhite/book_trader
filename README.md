# VoltronFlamingo
Below you will find basic setup and deployment instructions for the voltronflamingo project.

## The Python/Django Tasks
1. Build an endpoint for creating user ratings on books
2. Add an average_rating field that comes back from GET requests on books (both list and detail endpoints are fine)

## The Javascript/React Tasks (optional)
Many of our backend services have a corresponding frontend component. If you
have time and the inclination to demonstrate your abilities with with frontend
applications below are some tasks you may choose to perform:

1. Update the BookItem component to enable a user to rate a book.
2. Create a component that displays publishers.

## Setup

The setup steps below assume you have just cloned the git repo and are in the directory with this `README`.

### Docker Setup (preferred)

#### Install Docker

* [Docker For Linux](https://docs.docker.com/engine/installation/linux/ubuntu/)
* [Docker For Mac](https://docs.docker.com/docker-for-mac/)
* [Docker For Windows](https://docs.docker.com/docker-for-windows/)

#### Very first time

```
$ docker-compose build
$ docker-compose run --rm web manage.py migrate
$ docker-compose run --rm web manage.py loaddata initial_data_MANUAL
$ docker-compose run --rm web manage.py createsuperuser
```

#### Start the container

`$ docker-compose up`

This will start the web container and run the tests.

If you followed the installations steps above, the site should now be
accessible at http://localhost:8000/ if you have installed docker in a
different way then you should substitute `localhost` for the IP of your
docker machine which you can obtain by running `docker-machine ip default`.

## Javascript (Node / NPM)

The Javascript side is run locally, outside of a docker container.

### Very First Time

This assumes that you've already installed node and have a fairly recent version.

```
$ npm install
$ npm run build
```

Note that running the Django application will return an HTML view that pulls in `main.js` from the above build command. The application should be accessible from http://localhost:8000/ at this point.

### Other commands

* `npm run watch` -- Have npm watch for changes and build automatically.
* `npm run eslint` -- Lint the JS according to the local .eslintrc.json.
* `npm run test` -- Run the JS test suite.

## Tests

A docker container exists for running the python tests, you can run this container directly with:

`docker-compose run --rm tests`

Or if you're not using Docker, just use the default Django test runner:

`python manage.py test`

To run the JS tests use:

`npm run test`

## Utilities
To generate random ratings on all books from all users use the
`generate_random_strings` management command. Note that this is destructive
(it will delete all existing ratings.):

`docker-compose run --rm web manage.py generate_random_ratings`
