# Installing and Using PostgreSQL with Django
This guide assumes that you've already installed Python3 to your machine and set up a Django application as detailed in our [Django Install Guide](./DjangoInstallGuide.md).

## Installing PostgreSQL
This guide will teach you how to install PostgreSQL for Ubuntu. If you're running on a different operating system, follow the PostgreSQL install guides available [here](https://www.postgresql.org/download/).

1. Set up your machine to add the PostgreSQL repository. Ubuntu repositories contain snapshot versions of PostgreSQL, so for the latest version setting up an additional repository is required.
```bash
$ sudo apt-get install wget ca-certificates
$ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
$ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
```
2. Install the PostgreSQL packages
```bash
$ sudo apt-get update
$ sudo apt-get install postgresql postgresql-contrib
```

## Setting up a Database
Once you've installed PostgreSQL, you'll need to set up a database in order to link it with Django. For our purposes we'll call the database 'flom' for use with the FLOM project, but if you're setting up a database for another project feel free to change the name.
 1. Log into the `postgres` user that was created during installation of PostgreSQL. You need to do this in order to perform administrative tasks on your databases.
```bash
$ sudo su - postgres
```
2. Once logged in as the `postgres` user, log into a PostgreSQL session.
```bash
$ psql
```
 * You may encounter an error that says:
   ```bash
   psql: could not connect to server: No such file or directory

   Is the server running locally and accepting connections on 
   Unix domain socket "/var/run/postgresql/.s.PGSQL.5432"?
   ```
 * This error has to do with the server being misconfigured before it starts. Follow these steps        to fix this error.
   1. Certify that postgresql service is running, using ```sudo service postgresql start```
   2. Run ```pg_lsclusters``` from your terminal.
   
      The output should be something like:
      
       ```bash
       Ver Cluster Port Status Owner    Data directory              Log file
       11  main    5432 down   postgres /var/lib/postgresql/11/main /var/log/postgresql/postgresql-11-main.log
        ```
    4.  Copy the version and the cluster, and run: ```pg_ctlcluster <version> <cluster> start ```
    5. Now the server should be running and you can verify this by using ```sudo service postgresql start``` again.
3. Once you've started a PostgreSQL session, you'll need to create a database, a user to interact with that database, and set the default expected values for the user that Django expects.
```bash
postgres=# CREATE DATABASE flom;
postgres=# CREATE USER flom_admin WITH PASSWORD 'password';
postgres=# ALTER ROLE flom_admin SET client_encoding TO 'utf8';
postgres=# ALTER ROLE flom_admin SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE flom_admin SET timezone TO 'UTC';
postgres=# GRANT ALL PRIVILEGES ON DATABASE flom TO flom_admin;
```
4. Exit out of the PostgreSQL session and the `postgres` user shell session and get back into your user shell session.
```bash
postgres=# \q
$ exit
```

## Linking a PostgreSQL database to a Django application
At last, link the PostgreSQL database that you created above to your Django application.
1. Change into your project's working directory and enter the virtual enviornment to install `psycopg2`, a library necessary for PostgreSQL to work with Python.
```bash
$ . env/bin/activate
$ pip3 install psycopg2
```
2. Open the `settings.py` module located in the child project directory. Scroll down until you see a section that looks similar to this:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
Change this section to look like the following (change the corresponding information if you changed anything while setting up the databse):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'flom',
        'USER': 'flom_admin',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
After making these changes, save and close the `settings.py`.

4. Change into the Django project directory to create and apply any existing migrations to the database.
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

Congratulations! You have successfully linked a PostgreSQL database to your Django application!
