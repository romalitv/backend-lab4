# Backend-lab4

### Variant: 11%3 = 2 : Custom expense categories

### To start the project:

You had to have installed python3 and docker.

Clone the repo: git clone https://github.com/romalitv/backend-lab4

Enter in the root directory of program and type:

```
python3 -m venv env
source ./env/bin/activate
pip install flask
pip freeze > requirements.txt
```

Also set up your JWT KEY by using this commands:

```
import secrets
secrets.SystemRandom().getrandbits(128)
```

Write `export JWT_SECRET_KEY = your_jwt_key`

After uncomment 2 line in init.py and add jwtkey.py file into "lab" path 

The content in jwtkey must be like this:

```
import os

os.environ["JWT_SECRET_KEY"] = "your_jwt_key"
```

After build docker-compose and run the image:

```
docker-compose build
docker-compose up
```

(If you have ubuntu like I do, type before each command "sudo")

Choose 172.20.0.1 IP-address