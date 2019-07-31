# Qualitas Server

Home to any tools or dashboards used by the OpenStax QA team.



### External Services

The following external services are required:

  - PostgreSQL 9.6

## Get Started

It's expected that you'll be running the application and external services with docker.

We recommend you install them using Docker and Docker Compose.
This should work on any OS that docker can be installed on:

1.  Install Docker and Docker Compose by following the instructions on the
    [Docker website](https://docs.docker.com/compose/install/)
    
    If you have Homebrew installed you can install both docker and docker-compose with:
    
    `brew install docker`

2.  Run Docker Compose:

    `docker-compose up`

    You will now have two containers running PostgreSQL and the main application.
    `docker container ls` will show the running containers.

    When you want to shut the containers down you can interrupt the `docker-compose` command.
    If you would rather run them in the background, you can run `docker-compose up -d`.

3.  If not running Docker Compose in detached mode, open a new terminal window.

4.  Copy/Rename the `qualitas.env.example` file to `qualitas.env` and fill out the values:

    `cp qualitas.env.example qualitas.env`

5.  Initialize the database by running:

    `make initdb`

As you make changes to the source code you should see the gunicorn server restart. 
This works because docker has mounted the source code into the container.
