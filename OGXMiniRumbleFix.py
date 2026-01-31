import usb.core
import usb.util
import time
import sys

VID = 0x045E
PID = 0x0291 or 0x0289

RUMBLE_ENABLE = bytes([0x00, 0x00, 0x08, 0x01])
RUMBLE_ON     = bytes([0x00, 0x01, 0x0F, 0xC0])
RUMBLE_OFF    = bytes([0x00, 0x01, 0x00, 0x00])

def main():
    dev = usb.core.find(idVendor=VID, idProduct=PID)
    if dev is None:
        print("Receiver / Controller not found!")
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

    dev.write(ep.bEndpointAddress, RUMBLE_ON)
    time.sleep(0.25)
    dev.write(ep.bEndpointAddress, RUMBLE_OFF)

    usb.util.release_interface(dev, intf_num)
    usb.util.dispose_resources(dev)

    print("Rumble should be fixed! Unplug + Replug the controller and visit the URL below to test vibration:")
    print("https://hardwaretester.com/gamepad")

if __name__ == "__main__":
    main()
