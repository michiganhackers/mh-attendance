# MH Attendance
[![Build Status](https://travis-ci.org/michiganhackers/mh-attendance.svg)](https://travis-ci.org/michiganhackers/mh-attendance)

[![Build Status](https://travis-ci.org/michiganhackers/mh-attendance.svg)](https://travis-ci.org/michiganhackers/mh-attendance)

This repository contains the source code for [Michigan Hackers](http://wwww.michiganhackers.org)' attendance app.

The app uses Twilio to check-in attendees to MH events. It comes with an admin interface so MHers can set-up event-based check-in "sessions", an API for querying and a conversation framework so we can register new members quickly and get to know more about them.


# Getting started

#### Install pip 

    easy_install pip

#### Install Fabric 

    pip install fabric

#### Setup the project

    fab dev setup

#### Setup a mail server
You'll need an smtp server set-up for email handling (or use [Gmail credentials](http://flask.pocoo.org/snippets/85/)). Mail is handled by [flask-mail](https://pythonhosted.org/flask-mail/). If you're on a Mac, the smtp server postfix should come built in. You can start it by running:
```sh
sudo postfix start
```

#### Setup Ngrok
Download [ngrok](https://ngrok.com/download) to test your Twilio app while running a localserver. An excellent guide on doing so can be found [here](https://www.twilio.com/blog/2013/10/test-your-webhooks-locally-with-ngrok.html). Essentially, set-up your Twilio messages URL to point to your Ngrok tunnel url.

#### Run the server!

    fab run_dev

#### Run Ngrok
Next, start up Ngrok so that Twilio messages can be routed properly.
```sh
/path/to/ngrok 5000
```
OR
```sh
/path/to/ngrok -authtoken="authtoken" -subdomain="specificy subdomain" 5000
```
Navigate your browser to the url it lists in your terminal, and there you have it! 
Make sure your Twilio messages url matches your ngrok url.

Enjoy! Access it at `localhost:5000`

#### Run the test!
Before run the test, make sure there is something useful/working at Env/.env-test

    fab run_test


## Deploying to staging

#### Configure SSH

Move your AWS key into ~/.ssh/

Add this to your SSH config (~/.ssh/config). Create it if the file doesn't exist.

	Host mh-attendance
	    Hostname ec2-public-address.compute-1.amazonaws.com
	    User ubuntu
	    port 22
	    IdentityFile ~/.ssh/mh-attendance-keypair-useast1.pem

Verify that the ssh host works

	ssh mh-attendance


#### Deploy

##### Set-up your remote environment

Add this to your instance's /etc/nginx/sites-available/default
```
server {
    #EC2 instance security group must be configured to accept http connections over Port 80 
    listen 80;
    server_name ec2-public-address.compute-1.amazonaws.com;

    access_log  /var/log/nginx/guni-access.log;
    error_log  /var/log/nginx/guni-error.log info;

    keepalive_timeout 5;

    # path for static files
    root /home/ubuntu/mh-attendance/app/static/;

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://127.0.0.1:8000/;


    }
}
```
```
sudo service nginx restart
```

##### Deploy
Add your remote

    git remote add production ubuntu@mh-attendance:~/mh-attendance.git

and push to production...

    git push -f production master

Production runs off of a hook from origin/master, so you must first push to origin for the server to update.

See Matt about getting keys
