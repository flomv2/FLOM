.PHONY: install
install:
	sudo apt-get update
	sudo apt-get -y upgrade
	sudo apt-get install python3
	python3 -V
	sudo apt-get install -y python3-pip
	pip3 -V
	pip3 install virtualenv
	virtualenv --version
	mkdir django-apps
	cd django-apps
	virtualenv env
	. env/bin/activate
	pip install django
	django-admin --version
	
	
	
	
