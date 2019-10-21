# This is a work-in-progress API for QR ticket management
- Serves as a Python Django API for the application
- Currently only testing functionality and app integration

## API Documentation
**Available on following endpoints after runnning the docker compose:**
- <pre>/swagger/</pre>
- <pre>/swagger.json</pre>
- <pre>/redoc/</pre>

## Available endpoints
- <pre>/dashboard/</pre> - traefik dashboard
- <pre>/add/code</pre> - add a code for a user
- <pre>/add/user</pre> - add a user
- <pre>/get/codes</pre> - get all codes
- <pre>/get/user_codes</pre> - get codes for a user
- <pre>/get/users</pre> - get all users

## SSL certificate and user generation
- <pre>cd traefik/certs</pre>
- <pre>openssl req -new -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out cert.crt -keyout api.key</pre>
- <pre><code>echo $(htpasswd -nb <b>USER PASSWORD</b>) >> authfile</pre>
- Fill in all the details
- This is a self-signed certificate compatible with TLS 1.3. It is used so that there is no need for having a domain. When connecting, make sure to add the certificate to trusted ones.

## Project startup
- Make sure you have docker and docker-compose installed and running.
- You can specify the database credentials in .env file **BEFORE STARTING THE PROJECT**.
- Run <pre>sudo docker-compose up -d</pre> in the root directory of the project to start it.
- You can see all the running containers with <pre>sudo docker ps -a</pre>
- Stop the project with <pre>sudo docker-compose down</pre>
- Make sure not to modify folders static, traefik and postgres-data in any way. They are mounted to docker containers and serve as persistent data storage for some containers.


## TODO