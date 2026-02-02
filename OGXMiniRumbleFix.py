import usb.core, usb.util, time, sys, os, webbrowser

VID = 0x045E # Microsoft VID, may require changing for third-party controllers.
PID_WIRED = 0x028E # Genuine wired Xbox 360 controller PID
PID_W = 0x0719 # Genuine Xbox 360 wireless adapter PID
PID_GENERIC = 0x0291 # Third-party wireless adapter PID
PID_GENERIC_TWO = 0x02AA # Additional third-party wireless adapter PID
PID = 0x0289 # Third-party(?) Xbox 360 controller PID
GAMEPAD_URL = "https://hardwaretester.com/gamepad"

RUMBLE_ENABLE = bytes([0x00, 0x00, 0x08, 0x01])

def main():

    print('''
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

[''' + 
    '\033]8;;https://github.com/faithvoid/OGXMiniRumbleFix\033\\OGX-Mini Rumble Fix v1.0\033]8;;\033\\' +
''']

by [''' + 
    '\033]8;;https://github.com/faithvoid\033\\faithvoid\033]8;;\033\\'
''']

''')

    dev = usb.core.find(idVendor=VID, idProduct=PID) or usb.core.find(idVendor=VID, idProduct=PID_GENERIC) or usb.core.find(idVendor=VID, idProduct=PID_GENERIC_TWO) or usb.core.find(idVendor=VID, idProduct=PID_W) or usb.core.find(idVendor=VID, idProduct=PID_WIRED)
    if dev is None:
        print("Xbox 360 controller / wireless receiver not found! Please reconnect your controller and try again.")
        print("If that doesn't work, find the VID and PID of your controller and replace PID and VID values in the script and retry!\n")
        sys.exit(1)

    cfg = dev.get_active_configuration()

    ep = None
    intf_num = None

    for intf in cfg:
        if dev.is_kernel_driver_active(intf.bInterfaceNumber):
            dev.detach_kernel_driver(intf.bInterfaceNumber)

        for e in intf:
            if usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT:
                ep = e
                intf_num = intf.bInterfaceNumber
                break
        if ep:
            break

    if ep is None:
        print("No OUT endpoint found")
        sys.exit(2)

    usb.util.claim_interface(dev, intf_num)
    print('Initializing...\n')
    dev.write(ep.bEndpointAddress, RUMBLE_ENABLE)
    time.sleep(0.05)

    usb.util.release_interface(dev, intf_num)
    usb.util.dispose_resources(dev)

    time.sleep(1)

    if os.geteuid() == 0:
        print("Xbox 360 controller rumble should be fixed! Unplug + Replug the controller and visit the URL below to test vibration:\n")
        print("https://hardwaretester.com/gamepad" + "\n")

    else:
        print("Xbox 360 controller rumble should be fixed! Unplug + Replug the controller check your vibration in the browser window!")
        webbrowser.open(GAMEPAD_URL)

if __name__ == "__main__":
    main()
