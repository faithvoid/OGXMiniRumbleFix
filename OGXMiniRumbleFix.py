import usb.core, usb.util, time, sys, os, webbrowser

VID = 0x045E # Microsoft VID, may require changing for third-party controllers.
PID_WIRED = 0x028E # Genuine wired Xbox 360 controller PID
PID_WIRELESS = 0x0719 # Genuine Xbox 360 wireless adapter PID
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
    '\033]8;;https://github.com/faithvoid/OGXMiniRumbleFix\033\\OGX-Mini Rumble Fix v1.01\033]8;;\033\\' +
''']

by [''' + 
    '\033]8;;https://github.com/faithvoid\033\\faithvoid\033]8;;\033\\'
''']

''')

    devices = list(usb.core.find(find_all=True, idVendor=VID))
    
    if not devices:
        print("No Xbox 360 / XInput controllers found!\n")
        sys.exit(1)

    supported_pids = [PID, PID_GENERIC, PID_GENERIC_TWO, PID_WIRELESS, PID_WIRED]
    dev = None
    for pid in supported_pids:
        for d in devices:
            if d.idProduct == pid:
                dev = d
                print(f"Supported controller found! [{d.idVendor:04X}:{d.idProduct:04X}]")
                break
        if dev:
            break

    if dev is None and devices:
        print("Unsupported controller(s) found with Microsoft(-style) VID:")
        for i, d in enumerate(devices):
            print(f"{i+1}: {d.idVendor:04X}:{d.idProduct:04X}")

        choice = input("\nWould you like to try sending a 'Rumble Enable' packet?\n\n- Only do this if you're sure this is an Xbox 360(-style) controller! -\n\n(Y/N): ").strip().upper()
        if choice == "Y":
            while True:
                selection = input(f"Enter the number of the device (1-{len(devices)}): ").strip()
                if selection.isdigit() and 1 <= int(selection) <= len(devices):
                    dev = devices[int(selection)-1]
                    break
                else:
                    print("Invalid selection, try again.")
        else:
            print("No device selected! Exiting...")
            sys.exit(1)

    if dev is None:
        print("No supported controller found!")
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
        print("No OUT endpoint found!")
        sys.exit(2)

    usb.util.claim_interface(dev, intf_num)
    print(f"Sending 'Rumble Enable' packet to {dev.idVendor:04X}:{dev.idProduct:04X}...\n")
    dev.write(ep.bEndpointAddress, RUMBLE_ENABLE)
    time.sleep(0.05)

    usb.util.release_interface(dev, intf_num)
    usb.util.dispose_resources(dev)

    if os.geteuid() == 0:
        print("Xbox 360 controller rumble should be fixed! Unplug + Replug the controller and visit the URL below to test vibration:\n")
        print(GAMEPAD_URL + "\n")
    else:
        print("Xbox 360 controller rumble should be fixed! Unplug + Replug the controller and check your vibration in the browser window!\n")
        webbrowser.open(GAMEPAD_URL)

if __name__ == "__main__":
    main()
