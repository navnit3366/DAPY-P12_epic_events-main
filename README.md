![epicevents-logo](https://user.oc-static.com/upload/2020/09/22/16007804386673_P10.png)

# EPIC EVENTS CRM

Customer Relationship Management (CRM) system for Epic Events.

## Installation

### PostgreSQL installation

Download and install postgresql by following instructions dedicated to your OS on https://www.postgresql.org/download/. 

On linux:
```
# Install postgresql
sudo apt-get install postgresql postgresql-contrib
# Postgresql x Python dependencies
sudo apt-get install libpq-dev python3-dev
```

### PostgreSQL configuration 

Configuration can be made as follow: 

By default configuration, a user called Postgres is created on your system and is made to have super admin access to PostgreSQL instance. Start PostgreSQL with this user with `sudo -u postgres pqsl`

In PostgreSQL:
```
CREATE DATABASE epicevents_crm;
CREATE USER epicevents_admin WITH ENCRYPTED PASSWORD password;
ALTER ROLE epicevents_admin SET client_encoding TO 'utf8';
GRANT ALL PRIVILEGES ON DATABASE epicevents_crm TO epicevents_admin;
```

"epicevents_crm", "epicevents_admin" and "password" are the default database name and credentials, as defined on the settings file. You will have to edit Django's DATABASES NAME, USER and PASSWORD accordingly if you decide to use other names/credentials. See [this topic on Django Central](https://djangocentral.com/using-postgresql-with-django/)

Type `\q` to exit PostgreSQL;

### Setting up directory and environment 

```
# Clone this repo
git clone https://github.com/mjeammet/DAPY-P12_epic_events.git

# Create and install environment
python -m venv env
pip install -r requirements.txt
```

## Use

```
# Source environment
source env/bin/activate

# Run server 
python manage.py runserver
```

## Log and error tracking

All errors and exceptions encountered by the app are tracked on [the related Sentry project](https://sentry.io/organizations/dapyp12/issues/?project=6180366). 