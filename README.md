# Qualitas Server

Home to any tools or dashboards used by the OpenStax QA team.


## Get Started

The following external services are required:

  - PostgreSQL 11

We recommend you install them using Docker and Docker Compose.
This should work on any OS that docker can be installed on:

1.  Install Docker and Docker Compose by following the instructions on the
    [Docker website](https://docs.docker.com/compose/install/)
    
    If you have Homebrew installed you can install both docker and docker-compose with:
    
    `brew install docker`

2.  Run Docker Compose:

    `docker-compose up`
    
    or for "detached" mode:
    
    `docker-compose up -d`

    You will now have two containers running PostgreSQL and the main application.
    `docker-compose ps` will show the running containers. If you are not running in
    detached mode you'll need to open a new terminal.

    When you want to shut the containers down you can interrupt the `docker-compose` command.
    If you are running in detached mode you can run `docker-compose stop`.

3.  If not running Docker Compose in detached mode, open a new terminal window.

4.  Copy/Rename the `env-qualitas.env.example` file to `env-qualitas.env` and fill out the values:

    `cp env-qualitas.env.example env-qualitas.env`
5.  Copy/Rename the `postgres.env.example` file to `env-postgres.env= and fill out the values:

    `cp env-postgres.env.example env-postgres.env`
    
    The values in the `env-postgres.env.example` file can used as-is for development purposes.

5.  Initialize the database by running:

    `make initdb`
    
    You will be prompted for the password to the database. You can find the password by 
    using the value used in `env-postgres.env` file.

As you make changes to the source code you should see the gunicorn server restart. 
This works because docker has mounted the source code into the container.
