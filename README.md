# app_name

Replace this description for your new application... lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eget pulvinar est.

## System Requirements

- Python (3+)
- Docker
- Node

## Development Stack

- Django (2.1 - 2.3)
- Vue (2.x)
- Webpack (4.x)
- Bootstrap (4.6.x)

## Development (using Docker)

Go to your repository

        $ cd new-repo

Docker/Docker Compose is used to containerize your local build environment and deploy it to an 'app' container which is exposed to your localhost so you can view your application. Docker Compose creates a 'devtools' container - which is used for local development. Changes made locally are automatically syncd to the 'app' container.

        $ docker-compose up --build

View your application using your specified port number in the .env file

        Demo: http://localhost:8000/
