# Project

Install Raspbian (monitor, keyboard, mouse)
•	Username: pi (default)
•	Password: raspberry (default)

Setup a static IP address (https://pihw.wordpress.com/guides/direct-network-connection/)
•	sudo ifconfig eth0 169.254.0.2
•	hostname -I (check if it worked)
•	Saving the new configuration
o	sudo cp /boot/cmdline.txt /boot/cmdline.normal (copy of the original file)
o	sudo nano /boot/cmdline.txt (edit the original file)
o	Add at the end of the long line ip=169.254.0.2 (add a space between the last item and “ip=169.254.0.2”)
o	Crt+x and y (to save and exit)
o	sudo cp /boot/cmdline.txt /boot/cmdline.direct (copy of the new file)
o	sudo reboot (next time the IP address will be automatically set)

TCP vs UDP (http://pymotw.com/2/socket/udp.html)
•	TCP (ensuring that all of the data is transmitted in the right order)
•	UDP (delivery is not guaranteed, faster than TCP, single packet = only hold 65,507 bytes)

GitHub (https://github.com/thiagopuga/Project.git)

Reading analog-to-digital (http://raspberry.io/projects/view/reading-from-a-mcp3002-analog-to-digital-converter/)
•	Use a analog-to-digital converter (ADC)

Setup a remote desktop for Raspberry Pi (http://www.raspians.com/knowledgebase/?knowledgebase=setting-up-a-remote-desktop-view-the-pi-on-your-windows-pc/)
•	Install Xming on Windows (http://sourceforge.net/projects/xming/)
•	"C:\Program Files (x86)\Xming\Xming.exe" :0 -clipboard -rootless -screen 0 800x600+100+100@1 (set window size on the shortcut, +100+100 is the window`s position on the screen)
•	Install PuTTY on Windows (http://www.putty.org/)
o	Run PuTTY.
o	Select SSH as the connection type.
o	Enter in your Pi’s IP address as the Host Name
o	The port should be 22 unless you know better
o	In PuTTY`s option tree, select Connection/SSH/X11
o	Check the box labelled Enable X11 forwarding
o	Go back to Session options (in the option tree)
o	If you would like to save these settings, type a name in the Saved Sessions box and click Save
o	Click Open
o	Once you have logged into the Pi type startlxde and you will see the desktop of your Raspberry in the Xming window (the Xming must be running on Windows)

Time synchronization via GPS
