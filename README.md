# yamdb_final
![example workflow](https://github.com/Mr-Qaimaq/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
**REST API** for **YaMDB** service, which stores *reviews* on different *titles*. *Titles* are divided to different *categories* and can extended by admin. Runs using GitHub workflow which: 
1. Checks code for compliance with PEP8 standard (using flake8 package) and running pytest from yamdb_final repository;
2. Assembly and delivery of the dock image for the container web on the Docker Hub;
3. Automatic project module on the battle server;
4. Notification to Telegram that the process has been successfully completed.

## To Get Started
1. Clone repo to your local device
```
git clone <repo>
```
2. Create and activate virtual environement. Then download all required dependences
```
python -m venv venv
pip install -r api_yamdb/requirements.txt
```

### Preparing Virtual Machine
First, you need to install Docker and Docker-Compose on your VM.

Docker installation:
```
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

Docker-Compose installation:
```
apt install docker-compose
```

Create project folder and copy files: docker-compose.yaml and nginx/default.conf from your local machine to VM
```
scp ./<FILENAME> <USER>@<HOST>:/home/<USER>/yamdb_final/
```

### Preparing GitHub repository
Please add following variables in your GitHub Secrets for getting access to your services. Variables were used in .github/workflow/yamdb_workflow.yaml
* DOCKER_USERNAME, DOCKER_PASSWORD - for uploading and downloading image from DockerHub
* HOST, USER, SSH_KEY, PASSPHRASE - for access to VM
* DB_ENGINE, DB_NAME, POSTGRES_PASSWORD, DB_HOST, DB_PORT - for connecting to your DataBase
* TELEGRAM_TO, TELEGRAM_TOKEN - for recieving Telegram notifications

### Application Deployment (workflow instructions)
1. When pushed to main branch application will go throught tests, updates image on DockerHub and deploys to the VM. Next you need to connect to your VM:
```
ssh <USER>@<HOST>
```
2. Open running container's terminal:
```
docker container exec -it <CONTAINER ID> bash
```
3. To have admin access to project, you need to create superuser. Type the code below and follow the instructions:
```
python manage.py createsuperuser
```

## Used technologies 
Python, Django, Django REST Framework, PostgreSQL, Nginx, Docker, Docker Compose, Docker Hub, GutHub Actions

## Author
**Samgar Kali** - Yandex Practicum student in Python Developer Course.

## Badge
![example workflow](https://github.com/Mr-Qaimaq/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Project URLs
* Project can be accessed by the following links: http://158.160.13.69 or http://qaimaq.ddns.net
* Admin panel: http://158.160.13.69/admin or http://qaimaq.ddns.net/admin
* API documentation: http://158.160.13.69/redoc or http://qaimaq.ddns.net/redoc