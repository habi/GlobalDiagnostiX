# look for all PHP files in current directory
# for each of those, generate an FTP command to transfer them to the camera
for i in `ls *.php`
do curl -T $i ftp://192.168.0.9/var/html/ --user root:pass
done