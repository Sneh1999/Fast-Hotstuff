# Fast-Hotstuff

This would be the prototype for Fast Hotstuff protocol

## Virtual Env setup

`python3 -m venv .venv`
`source .venv/bin/activate`

## To install the dependencies within venv

`pip3 install -r requirements.txt`

## Kill all running docker containers

`docker stop $(docker ps -aq)`
`docker rm $(docker ps -aq)`
