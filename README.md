# FLOM

### Folsom Library Occupancy Manager

FLOM is a web application created by a group of RPI students that allows the students and library staff at RPI to visualize the occupancy and gather usage statistics of the Folsom Library Occupancy Monitor.

## Getting Started
To get started all you need to do is clone the repository onto your local machine
by typing ```git clone https://github.com/flomv2/FLOM.git``` in your terminal.

Before you can run the web application, you will need to complete the Django install tutorial that is located on our GitHub in the Tutorials folder.

Please refer to this [Django tutorial](https://docs.djangoproject.com/en/2.2/intro/tutorial01/) or simply the 
[Django 2.2 documentation](https://docs.djangoproject.com/en/2.2/) for information about using our framework. Django provides a robust templating framework for HTML (that means please use it).

## Build Instructions

Once the URI is cloned, you can then run Django by moving into the WebApp directory in flom and running ```python3 manage.py runserver``` . This will start the web application on your localhost. In later versions you may need to install and setup Postgresql database which we will have tutorials on.

## Code of Conduct and Style Guidelines

Our developers pride ourselves on writing beautiful and efficient code. Contributers should follow standard good style practices such as: useful commenting, proper indentation, and portability. Our Web Application directory looks like this

    `Tutorials/`        - Tutorials on how to set up different aspcts of the flom project 
    `WebApp/`           - Main source code in which apps of each web page are created and urls are connected
    `License.md`  		- MIT License 
    `README.md`         - This file

## Website/Communication
https://rcos.io/projects/flomv2/flom/profile      
Contact any of the contributors on this page and we can add you to our Mattermost chat! This is also where you can find our blog.
   
## Git Branching Model

When making a new feature or a bug fix, please make a new branch from **Master** (or branch you are trying to modify). On your command line, run 

`git checkout **(original branch name)**` \
`git branch [new branch name]` \
`git checkout [new branch name]` 

Branch names should be concise and self-explanatory. Please make your branch names lowercase and use hyphens (-) for spaces. You don't need to prepend your branch name with or include other details such as your name. For example, a feature branch for updating the about page UI might be called `about-styles` or `about-page-ui`. 

When you have changes to your local code base in your new branch, commit push them with 

`git commit -m [Commit message]` \
`git push` 

Commit messages should be concise and self-explanatory, just like branch names. 

Once your have completed your feature or fixed you bug, please perform a **Pull Request** into master, even if you are an admin. Pull requests provide a more readable commit log, highlighting major features and changes. On the Github repository website, click new pull request and select `"master" <- "your branch name"`. This requires an admin to approve your changes before they are live on the develop branch. 
