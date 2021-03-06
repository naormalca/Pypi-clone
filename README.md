My-Pypi clone [![Build Status](https://travis-ci.com/naormalca/Pypi-clone.svg?branch=master)](https://travis-ci.com/naormalca/Pypi-clone)
===
This repoistory is a REST API service that clones Pypi.org(Python packages index) - [Python Packages Index](https://pypi.org/).

**Part of the REST API exposed and documented here:** https://documenter.getpostman.com/view/6819906/T1LQfR84?version=latest

**Stack:** Python, Flask, SqlAlchemy(also alembic for migration) and postgres.

**Challenges:** Authentication Authorization(JWT), clean code and deployment. 


**UI Repoistory:** https://github.com/naormalca/pypi-react-ui


Backlog
---
Look at the public Trello https://trello.com/b/TTeJNSAv/pypi-clone .

Getting Started
---
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
---
Make sure you [install docker-compose](https://docs.docker.com/compose/install/).

Installing
---
Clone this repoistory.
> git clone https://github.com/naormalca/Pypi-clone.git

> cd Pypi-clone/

Build the images
> docker-compose build

Run the containers

> docker-compose up

Go to 127.0.0.1:80 :)

Running the tests
---
Coming soon

Deployment & Scripts
---
In order to load data to the DB:
> docker-compose exec my_pypi python my_pypi/manage.py load_db

In order to fetch new packages from pypi.org:
> docker-compose exec my_pypi python my_pypi/manage.py fetch

*Deployment Script* comming soon

Configuration
---
Coming soon
