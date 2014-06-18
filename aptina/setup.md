# How to setup DevWareX on Ubuntu 12.04

## Install Python 3
- Follow the [LinuxInstructions] from Aptina on their Atalassian-page, namely
	- `wget http://www.python.org/ftp/python/3.3.2/Python-3.3.2.tar.xz`
	- `tar -xvf Python-3.3.2.tar.xz`
	- `cd Python-3.3.2`
	- `./configure --enable-shared --prefix=/usr && make && make install`
	- `sudo ln -s /Library/Frameworks/Python.framework/Versions/3.3/Python /usr/lib/libpython3.3m.dylib`

## Install DevWare
- `sudo apt-get install libtbb-dev` to install a necessary [library]
- Download a recent version from the [DevSuite]-website, either manually or with this command, which downloads Version 1.4 for Linux32, unpacks it and starts the installation:
  `wget https://aptina.atlassian.net/wiki/download/attachments/11501573/DevWareX_linux32_1_4.tar;tar -xvf DevWare*.tar;./Developer`

## Get sensor and board files
### Very Easy
- Get the files from your Aptina representative, save them to the `data` directory.

### Easy
Since you've probably already checked out the [GlobalDiagnostiX repository][GDXrepo] or are working at PSI, you can just symlink the necessary files.
- `cd` into the `data` directory inside the directory were you installed the DevSuite.
- `ln -s /afs/psi.ch/project/EssentialMed/Dev/aptina/data/* .`

### Harder
You can only check out the files you need from the [GlobaldiagnostiX repository][GDXrepo]. Although you probably want to go the *Very Easy* or *Easy route*...
- `cd` into the directory were you installed the DevSuite.
- `rm -r data` to remove the original `data` directory.
- `git init data;cd data` to make a new Git repository.
- `git remote add -f origin git@github.com:habi/GlobalDiagnostiX.git` to add the original repository as remote.
- `git config core.sparsecheckout true;mkdir .git/info` to enable sparse checkout
- `echo aptina/data/apps_data/ >> .git/info/sparse-checkout;echo aptina/data/board_data/ >> .git/info/sparse-checkout;echo aptina/data/sensor_data/ >> .git/info/sparse-checkout` to add the necessary files to the desired files to checkout.
- `git pull origin master` to get them
- `mv aptina/data/* .;rm -r aptina` to remove some cruft 

## Start the DevSuite
- `cd PATH_TO_DEVSUITE` and start it with `./DevWareX.exe`

[LinuxInstructions]: https://aptina.atlassian.net/wiki/display/DEVS/DevWareX+Installation+Instructions+-+Linux
[library]: http://packages.ubuntu.com/precise/libtbb-dev
[DevSuite]: https://aptina.atlassian.net/wiki/display/DEVS/Software+Downloads
[GDXrepo]: https://github.com/habi/GlobalDiagnostiX

# How to setup DevWareX on Mac OS X
## Install Python 3
- Follow the [MacInstructions] from Aptina on their Atalassian-page, namely
	- `cd; cd Downloads`
	- `wget https://www.python.org/ftp/python/3.3.2/python-3.3.2-macosx10.6.dmg; open python-3.3.2-macosx10.6.dmg`
	- Double-click on "Python.mpkg" and install Python 3.
	- `sudo ln -s /Library/Frameworks/Python.framework/Versions/3.3/Python /usr/lib/libpython3.3m.dylib`

## Install DevWare
- `cd; cd Downloads`
- `wget https://aptina.atlassian.net/wiki/download/attachments/11501573/DevWareX_MacOSX_1_8.dmg; open DevWareX_MacOSX_1_8.dmg`
- Double-click on "Developer" ton install DevWare
- `cd` into the `data` directory inside the directory were you installed the DevSuite.

## Get sensor and board files
### Very Easy
- Get the files from your Aptina representative, save them to the `data` directory.

### Easy
Since you've probably already checked out the [GlobalDiagnostiX repository][GDXrepo] or are working at PSI, you can just symlink the necessary files.

- `cd` into the directory inside the directory were you installed the DevSuite, probably something like `cd /Applications/Aptina_DevWare`
- If you're (always) connected to AFS, you can just enter `ln -s /afs/psi.ch/project/EssentialMed/Dev/aptina/data/* .`
- Otherwise, if you're not connected to AFS, you just symlink the [data] directory of your checked out repository to the base directory of the DevWare installation.

## Start the DevSuite
- `/Applications/Aptina_DevWare/DevWareX.app/Contents/MacOS/DevWareX`, because you'll need the command-line output!

You'll also need to associate the INI and SDAT files to "TextEditor" for various DevWareX features to work correctly:

- Select any .ini file
- `⌘+i` and select "Open With" and under "Applications" select "TextEdit".
- Repeat these steps on any .xsdat file.

[MacInstructions]: https://aptina.atlassian.net/wiki/display/DEVS/DevWareX+Installation+Instructions+-+MacOS
[data]: https://github.com/habi/GlobalDiagnostiX/tree/master/aptina/data

