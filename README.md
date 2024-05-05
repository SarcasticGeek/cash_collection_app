## Compose sample application

### Use with Docker Development Environments

You can open this sample in the Dev Environments feature of Docker Desktop version 4.12 or later.

[Open in Docker Dev Environments <img src="../open_in_new.svg" alt="Open in Docker Dev Environments" align="top"/>](https://open.docker.com/dashboard/dev-envs?url=https://github.com/docker/awesome-compose/tree/master/django)

### Django application in dev mode

Project structure:
```
.
├── compose.yaml
├── app
    ├── Dockerfile
    ├── requirements.txt
    └── manage.py

```

[_compose.yaml_](compose.yaml)
```
services: 
  web: 
    build: app 
    ports: 
      - '8000:8000'
```

## Deploy with docker compose

```
$ docker compose up -d
```
After the application starts, navigate to `http://localhost:8000` in your web browser:

Stop and remove the containers
```
$ docker compose down
```

## Migrating Data
`python manage.py migrate`

## Testing
`python manage.py test`

## API spec
`./cash_collection_swagger.yaml`

## Model Structure 

- User Model:
This model represents both CashCollectors and Managers in the system.

- Customer Model:
Represents information about customers.


- Task Model:
Represents tasks assigned to CashCollectors, containing customer information.
python

- Transaction Model:
Represents cash transactions between CashCollectors and Managers.

- FrozenCollector Model:
Tracks frozen CashCollectors due to holding over 5000 USD for more than 2 days.

- Manager Log Model:
Logs actions performed by Managers.

These models represent the entities and relationships in your Cash Collection application. You can customize them further based on additional requirements or business logic.
