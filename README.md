# This is a work-in-progress API for QR ticket management
- Serves as a Python Django API for the application
- Currently only testing functionality and app integration

## API Documentation
**Available on following endpoints after runnning the docker compose:**
- `/swagger/`
- `/swagger.json`
- `/redoc/`

## Available endpoints
- `/dashboard/` - traefik dashboard
- `/add/code` - add a code for a user
- `/add/user` - add a user
- `/get/codes` - get all codes
- `/get/user_codes` - get codes for a user
- `/get/users` - get all users

## SSL certificate generation
- `cd traefik/certs`
- `openssl req -new -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out cert.crt -keyout api.key`
- Fill in all the details
- This is a self-signed certificate compatible with TLS 1.3. It is used so that there is no need for having a domain. When connecting, make sure to add the certificate to trusted ones.

## Project startup
- Make sure you have docker and docker-compose installed and running.
- You can specify the database credentials in .env file **BEFORE STARTING THE PROJECT**.
- Run `sudo docker-compose up -d` in the root directory of the project to start it.
- You can see all the running containers with `sudo docker ps -a`.
- Stop the project with `sudo docker-compose down`.
- Make sure not to modify folders static, traefik and postgres-data in any way. They are mounted to docker containers and serve as persistent data storage for some containers.


## TODO