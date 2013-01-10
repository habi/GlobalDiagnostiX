# Switching the Network configuration so we can connect the camera

echo "Setting Network interface to IP 192.168.0.1"
sudo ifconfig eth0 192.168.0.1
echo "Please unplug and reconnect the Ethernet cable from the Elphel-Camera "
echo ""
echo "After a while the mii-tool command below should show"
echo "TI:ME:00 eth0: negotiated 100baseTx-FD, link ok'"
echo " you can then CTRL+C this script"
sudo mii-tool -w


