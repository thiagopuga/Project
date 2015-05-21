# Project

Setting a static IP address (Raspbian):
sudo ifconfig eth0 169.254.0.2

To check the new IP:
hostname -I

The new IP address will be lost when we reboot, so we need to ensure it is set every time we boot (or at least every time we want it to be when we boot).

Make a copy of the file, with the following command:
sudo cp /boot/cmdline.txt /boot/cmdline.normal
