import pyudev

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')

for device in iter(monitor.poll, None):
    if device.action == 'add':
        print('{} connected'.format(device))





# import pyudev
# context = pyudev.Context()
# monitor = pyudev.Monitor.from_netlink()
# # For USB devices
# monitor.filter_by(susbsytem='usb')
# # OR specifically for most USB serial devices
# monitor.filter_by(susbystem='tty')
# for action, device in monitor:
#     vendor_id = device.get('ID_VENDOR_ID')
#     # I know the devices I am looking for have a vendor ID of '22fa'
#     if vendor_id in ['22fa']:
#         print('Detected {} for device with vendor ID {}'.format(action, vendor_id))


# import usb.core
# dev = usb.core.Configuration(device= 781 ,configuration=0) 

# VID=0x0781
# PID=0x5595 
# # dev = usb.core.find(idvendor = VID, idProduct = PID)
# dev = usb.core.find(idvendor = 0x0781, idProduct = 0x5595)
# print(dev)

# # ep = dev[0].interfaces()[0].endpoints()[0]

# # i=dev[0].interface()[0].binterfaceNumber
# # dev.reset()

# # if(dev.is_kernal_driver_active()):
# #     print("usb is connected")
# if not dev:
#     print("coudnot find the pendrive")
# else:
#     print("found the pendrive")
# exit(0)

# VID=0x0781
# PID=0x5595 
# for dev in usb.core.find(idvendor = 0x0781, idProduct = 0x5595):
#     print(dev)

#!/usr/bin/python
# import sys
# import usb.core
# # find USB devices
# dev = usb.core.find(find_all=True)
# print(dev)
# # loop through devices, printing vendor and product ids in decimal and hex
# for cfg in dev:
# #   sys.stdout.write('Decimal VendorID=' + str(cfg.idVendor) + ' & ProductID=' + str(cfg.idProduct) + ' & manifacturername=' + str(cfg.iManufacturer) +'\n')
#   sys.stdout.write('Hexadecimal VendorID=' + hex(cfg.idVendor) + ' & ProductID=' + hex(cfg.idProduct) + '& manifacturername=' + str(cfg.iManufacturer) +'\n\n')