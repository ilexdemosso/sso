# SSO Demo Application

## Setup
Replace `DEMO_ENDPOINT` in `docker-compose.yml` with appropriate value and run `docker-compose up`

## Usage
All unauthenticated users will be redirected to ilex login form. If entered credentials are correct, you will be rederected back and authorized in demo application.

## Deploy to Production
It's necessary to pass application endpoint in `DEMO_ENDPOINT` variable in `docker-compose.yml`. Also `ALLOWED_HOSTS` should be changed to include appropriate domain name or IP address.