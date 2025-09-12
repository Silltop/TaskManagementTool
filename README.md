## Setting up project for development


Creating virtual environment <br />
`python3 -m venv venv`

Activating venv <br />
`source venv/bin/activate`

Installing dependencies for local env <br />
`pip install -r requirements.txt`
`pip install `

## Running tests

You need to install prerequesities first<br />
`pip install pytest`

When you have dependencies simply run:<br />
`pytest`

## Starting application

1. You need to provide api key for geolocation api.

2. Application can be started from docker compose<br />
`docker compose -f docker-compose.yaml up`

