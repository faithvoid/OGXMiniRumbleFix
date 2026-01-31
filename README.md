# OGX-Mini Xbox 360 Controller Rumble Fix
OGX-Mini Xbox 360 Controller rumble fix Python script for Linux (may work under other operating systems, but is unsupported). Requires pyusb (python-pyusb) as a dependency.

## How to use:
- Plug in your Xbox 360 controller or receiver. If using a wireless controller, make sure to pair your controller to the receiver (if experiencing issues on Linux, try installing xpad and rebooting)
- Open your terminal in the folder OGXMiniRumbleFix.py is saved in.
- Run "sudo python3 OGXMiniRumbleFix.py" (this requires root permissions to access USB devices!)
- Unplug + replug your Xbox 360 controller / wireless adapter and follow the link in the terminal to test the vibration, it should now be restored!
- Please note that, as of right now, reconnecting your controller to an OGX-Mini WILL kill the vibration again. Just run this script again if that happens and it'll be restored!
