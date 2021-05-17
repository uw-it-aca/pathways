# app_name

This is a template repository used for creating Django-Vue applications. Use this template to create a new project repository.

## System Requirements

- Python (3+)
- Docker
- Node

## Development Stack

- Django (2.1 - 2.3)
- Vue (2.x)
- Webpack (5.x)
- Bootstrap (4.5.x)

## Cloning

Clone this template repo as a new repo (command line)

        $ git clone https://github.com/charlon/axdd-django-vue <new-repo>

OR.. using the Gihub interface, click on the "Use this template" button. Github will automatically clone this repo and setup everything for you.

## Configuration

After cloning this repo, find and replace the following instances to match your new repo name.

        'axdd-django-vue' with <new-repo>

Find and replace the following instance of the new Django app_name.

        'app_name' with <new_app>

Copy the sample .env file so that your environment can be run.

        $ cp .env.sample .env

Update any .env variables for local development purposes

## Update README

Replace the README.md file with the README_sample.md

        $ mv README_sample.md README.md
        $ git rm README_sample.md

Make any changes necessary to the new README file.

## Development (using Docker)

Go to your repository

        $ cd new-repo

Docker/Docker Compose is used to containerize your local build environment and deploy it to an 'app' container which is exposed to your localhost so you can view your application. Docker Compose creates a 'devtools' container - which is used for local development. Changes made locally are automatically syncd to the 'app' container.

        $ docker-compose up --build

View your application

        Demo: http://localhost:8000/
