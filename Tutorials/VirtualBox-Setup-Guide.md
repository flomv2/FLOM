# Installing VirtualBox and Setting up FLOM
## Tutorial by Chris Reed 9/24/19

1. Enable Virtualization in BIOS

..* Most default settings do not allow for virtualization so you will have to manually enable this.  Follow [this link](https://2nwiki.2n.cz/pages/viewpage.action?pageId=75202968) to see how you can do this on your individual computer as this process is different for each manufacturer.

2. Download VirtualBox

..* You can download VirtualBox [here](https://www.virtualbox.org/wiki/Downloads). Click on the link with your respective operating system and follow the installation instructions once the download is complete.

3. Setting Up a VirtualBox

..* Launch the 'Oracle VM VirtualBox' desktop application.  Click the large blue 'New' button to create the virtual machine.  A pop-up menu titled 'Create Virtual Machine' should appear almost immediately.

..* In the box titled 'Name and operating system' do the following:

...a). Set 'Name' to FLOM.
...b). Set 'Machine Folder' to wherever you want to store the virtual machine on your computer.
...c). Set 'Type' to Linux.
...d). Set 'Version' to Ubuntu (64-bit). Note if you cannot find the 64-bit option in the drop down menu then you have not enabled virtualization correctly in your BIOs.  Refer back to step 1. if this is the case.

..* I selected 2048 MB for Memory size.  This will depend slightly on the CPU power of your computer, if there is not enough memory for your CPU function then the box may run very slow. Increase memory size as needed.

..* You are going to need a virtual hard disk file to utilize the virtual machine.  If you already have a file partitioned for this machine then you can select the 'Use an existing virtual hard disk file' option and select that file in the drop down menu.  In most cases though you will just want to create a new hard disk file.  To do this in the click the option 'Create a virtual hard disk now' option in the box labeled 'Hard disk'.

..* Once you have finished configuring the virtual machine click the 'Create' button

..* Immediately after the machine has been configured and created, another menu should appear titled 'Virtual Hard Disk'.  

..* Make sure that the 'File location' is a subset of the file where the virtual machine is located.  This should look something like 'C:\Users\UserName\VirtualBox VMs\FLOM\FLOM.vdi'.  

..* I selected 15.00 GB  for 'File size' but if the virtual machine is running very slow or not at all you may want to increate the file size.

..* Then check to see that the 'VDI (VirtualBox Disk Image)' option is selected under the 'Hard disk file type' box.  

..* Then make sure the 'Storage on physical hard disk' option is set to 'Dynamically allocated'.

..* Once the virtual hard disk has been configured click the 'Create' button. This should finish with a new virtual machine title 'FLOM' on the side menu 'Powered Off'.

..* If you are having issues follow [this link](https://www.virtualbox.org/manual/ch01.html) to VirtualBox's getting started tutorial which has helpful pictures of the interface.

4. Download Linux

..* While the VirtualBox is configured to host Ubuntu's 64-bit Linux Operating System, you still need to download the physical OS from [Ubuntu's site](https://ubuntu.com/download/desktop).

..* There should be a large green 'Download' button you may click. This will start downloading the most recent release of Ubuntu's Linux OS.  At the time of writing this tutorial, the version is 'Ubuntu 18.04.3 LTS'.  You will know if the download was successful if a new DVD Drive (D:) with the version specified appears on your local disk.

..* VirtualBox will help you set up linux on the virtual machine when you start the box for the first time.

5. Starting the VirtualBox for the First Time

..* First to start the up the box hit the large, green arrow labeled 'Start'.  You should then get an immediate pop-up box which instructs you select a start-up disk. There will be a drop down menu and there should be an option that says "Host Drive D".  If you click this then it should go right into setting up the install guide.  This may take a few minutes.  You will know if it is working if you see an Ubuntu loading screen.  

..* Eventually you should see an interface with two main options 'Try Ubuntu' and 'Install Ubuntu'.  Please select 'Install Ubuntu'. From there you will be given some ubuntu installation options.  

..* Chose a language that suites your needs.  

..* From there you will find a page titled 'Updates and other software'. To optimize use select the 'minimal installation' option.  Under 'Other options' make sure 'Download updates while installing Ubuntu' is selected and 'Install third-party software for graphics and Wi-Fi hardware and additional media formats' is not selected.  Then press continue.

..* From there you may select an installation type.  You will most likely want to select the default option 'Erase disk and install Ubuntu'.  Once you have decided on your installation type you can select 'Install Now'.

..* If you get a warning in a screen titled 'Write the changes to disks?' you can just select 'Continue'.

..* Select your location (The Folsom Library is located in New York if you didn't know)

..* Fill out who you are.

...Your name: FLOM-Admin
...Your computer's name: flomadmin-VirtualBox
...Pick a username: flom-admin
...Choose a password: temp-password
...You can select 'Require my password to login'
...Press 'Continue'

..* You are now ready to install, it will take a few minutes to do so

..* Once the installation is done you should get a message asking you to restart the computer in order to use the new installation.  Click the 'Restart Now' button.  If it is taking a while to pop back up with Ubuntu, you may need to restart the machine as well.

..* From here you should come to a 'What's new in Ubuntu' screen.  Just keep hitting the green, 'Next' button in the top right corner until it goes away.

..* If you get a notification from the software updater, feel free to install these updates whenever convenient.  This goes for further use from here on.  These updates most likely not directly affect you so feel free to do this at your convenience.  If you run into an error at any point that you do not understand, I would recommend checking for ubuntu updates first.

6. Downloading the Appropriate Software for FLOM

..* First click the 3 by 3 square in the bottom left corner and open the 'Terminal'

..* The following are command arguments you should copy exactly into the terminal:

...Note: You will need to enter the account password and hit y to complete most of these downloads

```shell
$ sudo apt install git
```

```shell
$ sudo apt install python3-pip
```

7. Clone FLOM to Your Local Repository

```shell
$ git clone https://github.com/flomv2/FLOM.git
```

8. Get FLOM Working

..* Add the config.ini attached to the FLOM/WebApp/WebApp directory so that you can run FLOM

9. Run FLOM

..* Type the following command in the terminal

```shell
$ python3 manage.py runserver
```

..* Check out the app on your local system at http://127.0.0.1:8000/

..* And that's it!

