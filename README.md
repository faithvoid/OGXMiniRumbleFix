# OGX-Mini Xbox 360 Controller Rumble Fix
OGX-Mini Xbox 360 Controller rumble fix Python script for Linux (may work under other operating systems, but is unsupported). Requires pyusb (python-pyusb) as a dependency.
```
⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣶⣶⣶⣶⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡀⠀⠈⠉⠛⠿⣿⣿⣿⣿⠿⠛⠉⠁⠀⢀⠀⠀⠀⠀⠀
⠀⠀⠀⣴⣿⣿⣿⣶⣄⡀⠀⠈⠙⠋⠁⠀⢀⣠⣶⣿⣿⣿⣦⠀⠀⠀
⠀⢀⣾⣿⣿⣿⣿⣿⣿⡿⠂⠀⠀⠀⠀⠐⢿⣿⣿⣿⣿⣿⣿⣷⡀⠀
⠀⣾⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⢀⡀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣷⠀
⢠⣿⣿⣿⣿⣿⡟⠁⠀⠀⢀⣴⣿⣿⣦⡀⠀⠀⠈⢻⣿⣿⣿⣿⣿⡄
⢸⣿⣿⣿⣿⠏⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠹⣿⣿⣿⣿⡇
⠘⣿⣿⣿⠏⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠹⣿⣿⣿⠃
⠀⢿⣿⡟⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⢻⣿⡿⠀
⠀⠈⢿⡇⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⢸⡿⠁⠀
⠀⠀⠀⠃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠘⠀⠀⠀
⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠿⠿⠿⠿⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀
```
## How to use (root, easy):
- Download the latest "OGXMiniRumbleFix.py" from the repository (there won't be a real "Release" since this is just a stopgap fix)
- Plug in your Xbox 360 controller or receiver. If using a wireless controller, make sure to pair your controller to the receiver (if experiencing issues on Linux, try installing xpad and rebooting)
- Open your terminal in the folder OGXMiniRumbleFix.py is saved in.
- Run "sudo python3 OGXMiniRumbleFix.py" (this requires root permissions to access USB devices!)
- Unplug + replug your Xbox 360 controller / wireless adapter and follow the link in the terminal to test the vibration, it should now be restored!
- Please note that, as of right now, reconnecting your controller to an OGX-Mini WILL kill the vibration again. Just run this script again if that happens and it'll be restored!

## How to use (non-root, medium difficulty):
- Download the latest "OGXMiniRumbleFix.py" from the repository (there won't be a real "Release" since this is just a stopgap fix)
- Plug in your Xbox 360 controller or receiver. If using a wireless controller, make sure to pair your controller to the receiver (if experiencing issues on Linux, try installing xpad and rebooting)
- Open your terminal in the folder OGXMiniRumbleFix.py is saved in.
- Make a new file on your system called "/etc/udev/rules.d/99-xbox.rules" (ie; ``` sudo nano /etc/udev/rules.d/99-xbox.rules ``` ) and enter the following into it: ``` SUBSYSTEM=="usb", ATTR{idVendor}=="045e", MODE="0666" ``` 
- Run ``` sudo udevadm control --reload-rules ``` & ``` sudo udevadm trigger ``` (this may log you out)
- Run "python3 OGXMiniRumbleFix.py"
- Unplug + replug your Xbox 360 controller / wireless adapter and check the link that opens up in your browser to test the vibration, it should now be restored!
- Please note that, as of right now, reconnecting your controller to an OGX-Mini WILL kill the vibration again. Just run this script again if that happens and it'll be restored!
