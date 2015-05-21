# Project

Setting a static IP address (Raspbian):
sudo ifconfig eth0 169.254.0.2

To check the new IP:
hostname -I

The new IP address will be lost when we reboot, so we need to ensure it is set every time we boot (or at least every time we want it to be when we boot).

Make a copy of the file, with the following command:
sudo cp /boot/cmdline.txt /boot/cmdline.normal

Next edit the original file using nano:
sudo nano /boot/cmdline.txt

At the end of the long line, add the following (you will need to add a space between the last item and “ip”:
ip=169.254.0.2

Ctrl+x and y to save and exit

Make a copy of this file too:
sudo cp /boot/cmdline.txt /boot/cmdline.direct

You can now reboot the Raspberry Pi (sudo reboot), and next time the IP address will be automatically set.

To change between configurations, simply use the following commands (just remember to edit  /boot/cmdline.direct if you need to change the IP address in future).

sudo cp /boot/cmdline.normal /boot/cmdline.txt
sudo cp /boot/cmdline.direct /boot/cmdline.txt
