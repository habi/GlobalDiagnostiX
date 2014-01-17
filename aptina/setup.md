# How to setup DevWareX on Ubuntu 12.04

## Install Python3
- Follow the [instructions] from Aptina on their Atalassian-page, namely
	- `wget http://www.python.org/ftp/python/3.3.2/Python-3.3.2.tar.xz`
	- `tar -xvf Python-3.3.2.tar.xz`
	- `cd Python-3.3.2`
	- `./configure --enable-shared --prefix=/usr && make && make install`
	- `sudo ln -s /Library/Frameworks/Python.framework/Versions/3.3/Python /usr/lib/libpython3.3m.dylib`

# Install DevWare
- `sudo apt-get install libtbb-dev` to install a necessary [library]
- Download a recent version from the [DevSuite]-website, either manually or with this command, which downloads Version 1.4 for Linux32, unpacks it and starts the installation:
  `wget https://aptina.atlassian.net/wiki/download/attachments/11501573/DevWareX_linux32_1_4.tar;tar -xvf DevWare*.tar;./Developer`

# Get sensor and board files
## Very Easy
- Get the files from your Aptina representative, save them to the `data` directory.

## Easy
Since you've probably already checked out the [GlobalDiagnostiX repository][GDXrepo] or are working at PSI, you can just symlink the necessary files.
- `cd` into the `data` directory inside the directory were you installed the DevSuite.
- `ln -s /afs/psi.ch/project/EssentialMed/Dev/aptina/data/* .`

## Harder
You can only check out the files you need from the [GlobaldiagnostiX repository][GDXrepo]. Although you probably want to go the *Very Easy* or *Easy route*...
- `cd` into the directory were you installed the DevSuite.
- `rm -r data` to remove the original `data` directory.
- `git init data;cd data` to make a new Git repository.
- `git remote add -f origin git@github.com:habi/GlobalDiagnostiX.git` to add the original repository as remote.
- `git config core.sparsecheckout true;mkdir .git/info` to enable sparse checkout
- `echo aptina/data/apps_data/ >> .git/info/sparse-checkout;echo aptina/data/board_data/ >> .git/info/sparse-checkout;echo aptina/data/sensor_data/ >> .git/info/sparse-checkout` to add the necessary files to the desired files to checkout.
- `git pull origin master` to get them
- `mv aptina/data/* .;rm -r aptina` to remove some cruft 

# Start the DevSuite
- `cd PATH_TO_DEVSUITE` and start it with `./DevWareX.exe`

[instructions]: https://aptina.atlassian.net/wiki/display/DEVS/DevWareX+Installation+Instructions+-+Linux
[library]: http://packages.ubuntu.com/precise/libtbb-dev
[DevSuite]: https://aptina.atlassian.net/wiki/display/DEVS/Software+Downloads
[GDXrepo]: https://github.com/habi/GlobalDiagnostiX
