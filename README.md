My-Pypi clone [![Build Status](https://travis-ci.com/naormalca/Pypi-clone.svg?branch=master)](https://travis-ci.com/naormalca/Pypi-clone)
===
My clone to Pypi - [Python Packages Index](https://pypi.org/).

Stack: Python, Flask, SqlAlchemy(also alembic for migration) and postgres.


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

Go to 127.0.0.1:5000 :)

Running the tests
---
Currently the project have few simple tests, to run them enter to the container and run them with pytests as follow:
> docker-compose exec my_pypi pytest app/tests/__all_tests.py

Deployment
---
Coming soon

Configuration
---
Coming soon
