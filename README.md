# pathways

[![Build Status](https://github.com/uw-it-aca/pathways/workflows/Build%2C%20Test%20and%20Deploy/badge.svg?branch=main)](https://github.com/uw-it-aca/pathways/actions)
[![Coverage Status](https://coveralls.io/repos/github/uw-it-aca/pathways/badge.svg?branch=main)](https://coveralls.io/github/uw-it-aca/pathways?branch=main)

## System Requirements

- Python (3+)
- Docker
- Node

## Development Stack

- Django (3.x)
- Vue (3.x)
- Webpack (5.x)
- Bootstrap (5.x)

## Cloning

Clone this template repo as a new repo (command line)

        $ git clone git@github.com:uw-it-aca/pathways.git

## Development (using Docker)

Go to your repository

        $ cd pathways

Docker/Docker Compose is used to containerize your local build environment and deploy it to an 'app' container which is exposed to your localhost so you can view your application. Docker Compose creates a 'devtools' container - which is used for local development. Changes made locally are automatically syncd to the 'app' container.

        $ docker-compose up --build

View your application using your specified port number in the .env file

        Demo: http://localhost:8000/
