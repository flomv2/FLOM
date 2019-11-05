# Installing Python and Django
1. Install Python and Pip
	* We have to first update the local APT repository. 
````shell
$ sudo apt-get update && sudo apt-get -y upgrade
````
2. Install Python 3 
````shell
$ sudo apt-get install python3
````
3. Verify that Python was installed correctly.
````shell
$ python3 -V
````
4. Install pip which is used to install packages from PyPi (Python's package repository)
```` shell
$ sudo apt-get install -y python3-pip
````
5. Verify that pip was intalled
````shell
$ pip3 -V
````
6. Install virtualenv
	* This is a virtual environment where you can install software and python packages in a contained development space.
 ````shell
 $ pip3 install virtualenv
 ````
 7. Verify that virtualenv is installed
 ````shell
 $ virtualenv --version
 ````
 8. Install Django
	 1.  Make a new directory and then switch into that new directory.
	 ````shell
	$ mkdir django-apps
	$ cd django-apps
	 ````
	 2. While inside the django-apps directory create a new virtual environment which we called env.
	 ````shell
	 $ virtualenv env
	 ````
	 3. Now activate the virtual environment
	 ````shell
	 $ . env/bin/activate
	 ````
	 You can tell that it is activated if you see something similar to this:
	 ````shell
	 (env) sylvee@DESKTOP-RFPF6M7:
	 ````
	 4. Now intall the Django package with pip3
	 ````shell
	 $ pip3 install django
	 ````
	 5. Verify that Django installed
	 ````shell
	 $ django-admin --version
	 ````

# Django Test Project

1. Genrating the intial setup code if this is your first time using Django.
 ````shell
 $ django-admin startproject mysite
 ````

These files are:
* The outer `mysite/` root directory is just a container for your project. Its name doesn’t matter to Django; you can rename it to anything you like.
* -   `manage.py`: A command-line utility that lets you interact with this Django project in various ways. You can read all the details about  `manage.py`  in  [django-admin and manage.py](https://docs.djangoproject.com/en/2.2/ref/django-admin/).
* -   The inner  `mysite/`  directory is the actual Python package for your project. Its name is the Python package name you’ll need to use to import anything inside it (e.g.  `mysite.urls`).
* -   `mysite/__init__.py`: An empty file that tells Python that this directory should be considered a Python package. If you’re a Python beginner, read  [more about packages](https://docs.python.org/3/tutorial/modules.html#tut-packages "(in Python v3.7)")  in the official Python docs.
* -   `mysite/settings.py`: Settings/configuration for this Django project.  [Django settings](https://docs.djangoproject.com/en/2.2/topics/settings/)  will tell you all about how settings work.
* -   `mysite/urls.py`: The URL declarations for this Django project; a “table of contents” of your Django-powered site. You can read more about URLs in  [URL dispatcher](https://docs.djangoproject.com/en/2.2/topics/http/urls/).
* -   `mysite/wsgi.py`: An entry-point for WSGI-compatible web servers to serve your project. See  [How to deploy with WSGI](https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/)  for more details.
2. Verify that the project works by running the devserver.
````shell
$ python manage.py runserver
````

You should see something like this. Note for now ignore the erros about unapplied migrations.

````shell
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.

July 16, 2019 - 17:07:09
Django version 2.2.3, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
 ````
 3. Visit http://127.0.0.1:8000/ and you should see a rocket.
 4. For more in depth tutorial checkout [Django's Tutorial](https://docs.djangoproject.com/en/2.2/intro/tutorial01/)
 5.  Now you are ready to begin development of your project.
 
 
 





