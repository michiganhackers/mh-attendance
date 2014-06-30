MH Attendance 
======

This repository contains the source code for [Michigan Hackers](http://wwww.michiganhackers.org)' attendance app.

The app uses Twilio to check-in attendees to MH events. It comes with an admin interface so MHers can set-up event-based check-in "sessions", an API for querying and a conversation framework so we can register new members quickly and get to know more about them.

Installation
===
Getting started is easy. We suggest installing [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/). Once you've got that taken care of, take the following steps in your terminal:

1) Create a virtual environment where the app's dependencies will reside
```sh
mkvirtualenv mh-attendance-venv
```
You should now be working in this virtual environment. To check, make sure your terminal shows the following:
```sh
(mh-attendance-venv)username$
```
If not, simply type ```workon mh-attendance-venv```

2) After you've created your env, CD to the directory you want the app to be in and clone the Git repo for the app
```sh
cd Developer
git clone https://github.com/michiganhackers/mh-attendance.git
```
3) Navigate to the app
```sh
cd mh-attendance
```
4) Pip install of the project dependencies by running the following:
```sh
pip install -r requirements/dev.txt
```
5) You're all set. :) Refer to the usage.


Usage
===

Current Version
===
0.01

Tech
===
mh-attendance uses a number of open source projects to work properly:




