import usb.core
import usb.util
import time
import sys

VID = 0x045E
PID = 0x0291 
PIDALT = 0x0289

RUMBLE_ENABLE = bytes([0x00, 0x00, 0x08, 0x01])

def main():
    dev = usb.core.find(idVendor=VID, idProduct=PID) or usb.core.find(idVendor=VID, idProduct=PIDALT)
    if dev is None:
        print("Xbox 360 controller / wireless receiver not found!")
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

    dev.write(ep.bEndpointAddress, RUMBLE_ENABLE)
    time.sleep(0.05)

    usb.util.release_interface(dev, intf_num)
    usb.util.dispose_resources(dev)

    print("Xbox 360 controller rumble should be fixed! Unplug + Replug the controller and visit the URL below to test vibration:")
    print("https://hardwaretester.com/gamepad")

if __name__ == "__main__":
    main()
