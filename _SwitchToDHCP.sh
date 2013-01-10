# Deprecated, use ~/Switch.py instead
# Switching the Network configuration back to DHCP, so we can interweb

echo "Setting Network interface to DHCP (back from 192.168.0.1)"
echo "Please unplug the ELphel camera and plug in the PSI ethernet."
sudo dhclient eth0
echo ""
echo "After a while the mii-tool command below should show something like"
echo "TI:ME:00 eth0: negotiated 100baseTx-FD, link ok'"
echo " you can then CTRL+C this script"
sudo mii-tool -w


