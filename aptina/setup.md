# How to setup DevWareX on Ubuntu 12.04

- Follow the instructions on the Atalassian-page of [Aptina], namely
	- `wget http://www.python.org/ftp/python/3.3.2/Python-3.3.2.tar.xz`
	- `tar -xvf Python-3.3.2.tar.xz`
	- `cd Python-3.3.2`
	- `./configure --enable-shared --prefix=/usr && make && make install`
	- `sudo ln -s /Library/Frameworks/Python.framework/Versions/3.3/Python /usr/lib/libpython3.3m.dylib`
- `git clone https://github.com/Aptina/DevSuiteSDK.git aptina && cd aptina && git checkout 20e8f8e73a61a1df0b6aea7098fde9b4a91ba8e0` to clone the DevSuite repo and check out the commit in which Aptina did not remove DevWareX.
- `sudo apt-get install libtbb-dev` to install a necessary library
- `cd DevWareX/Linux_32 && sudo ./DevWareX.exe`

[Aptina]: https://aptina.atlassian.net/wiki/display/DEVS/DevWareX+Installation+Instructions+-+Linux
