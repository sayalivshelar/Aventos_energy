#####################################################################################################################
# importing the packages required
#####################################################################################################################
import software_ini as sw_ini_present
import os
import sys
import datetime
import shutil
from shutil import copytree, ignore_patterns
import subprocess
import json
import pyudev
context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')

flag=False
while 1:
    while flag==False:
        partitionsFile = open("/proc/partitions")
        # print(partitionsFile)
        lines = partitionsFile.readlines()[2:]#Skips the header lines
        # print(lines)
        for line in lines:
            words = [x.strip() for x in line.split()]
            minorNumber = int(words[1])
            deviceName = words[3]
            if minorNumber % 16 == 0:
                path = "/sys/class/block/" + deviceName
                if os.path.islink(path):
                    var_1=os.path.realpath(path).find("/usb")
                    if var_1 > 0:
                        print ("/dev/%s" % deviceName)
                        flag=True
    # for device in iter(monitor.poll, None):
    #     if device.action == 'add':
    #         print('{} connected'.format(device))
        # Path of the file from where you  want to copy
        source_directory='/media/pi/PENDRIVE/FIRMWARE_UPDATE/'
        files = os.listdir(source_directory)
        importing_file_flag= False

        # destination path to copy the files  
        destination = '/home/pi/Desktop/LATEST_FIRMWARE_UPDATE/back_%s'%datetime.datetime.now()
        source_directory='/media/pi/PENDRIVE/FIRMWARE_UPDATE/'
        try :
            for f in files:
                file_2=os.listdir(source_directory+f)
                for f1 in file_2:
                    if(f1 == 'software_ini.py'):
                        print("file found")
                        importing_file_flag=True
                
        except Exception as e:
            print(e)
        if importing_file_flag == True:
            import imp
            MODULE_PATH = source_directory+f+'/software_ini.py'
            MODULE_NAME = 'software_ini'
            sw_ini_update = imp.load_source(MODULE_NAME, MODULE_PATH)

            ##########################################################################################################
            # checking the Firmware version 
            ##########################################################################################################
            # check present Firmware version and upgrad Firmware version 
            #  == - no update to the server
            #  >  - update the version 
            #  <  - downgrade the version 
            ##########################################################################################################
            if sw_ini_present.Version['Present_version'] == sw_ini_update.Version['Upgrade_Version']:
                print("same firmware version number")
                # print("Present version number = "+ str(sw_ini_present.Version['Upgrade_Version']) +" update version number = "+ str(sw_ini_update.Version['Upgrade_Version']) )
                print("-----")

            elif sw_ini_present.Version['Present_version'] < sw_ini_update.Version['Upgrade_Version']:
                print("Upgrade firmware Version number")
                # uncomment below commented lines
                # try :
                #     for f in files:
                #         #create the files 
                #         source = '/media/pi/PENDRIVE/FIRMWARE_UPDATE/%s' % f
                #         copytree(source, destination, ignore=ignore_patterns('.pyc', 'tmp'))    
                # except Exception as e:
                #     print(e)
                # print("Present version number = "+ str(sw_ini_present.Version['Present_version']) +" update version number = "+ str(sw_ini_update.Version['Upgrade_Version']))
                # print("-----")
                sw_ini_present.Version['Present_version'] = sw_ini_update.Version['Upgrade_Version'] 
                #open the file and update the version numbers 
                # Dir_path =  os.path.abspath(os.path.dirname(sys.argv[0]))
                # subprocess.call(["ls"])
                # with open(Dir_path+'/software_ini.py','r') as file:
                #         JSON_Data_string=file.read()
                #         JSON_Data=json.loads(JSON_Data_string)
                #         file.close()
                # print(JSON_Data)

            elif sw_ini_present.Version['Present_version'] > sw_ini_update.Version['Upgrade_Version']:
                print("Downgrade firmware Version number")
                print("Present version number = "+ str(sw_ini_present.Version['Present_version']) +" update version number = "+ str(sw_ini_update.Version['Upgrade_Version']))
                print("-----")
                sw_ini_present.Version['Present_version'] = sw_ini_update.Version['Upgrade_Version']
            
            
            ##########################################################################################################
            # checking the docker version 
            ##########################################################################################################
            
            if sw_ini_present.docker['Present_version'] == sw_ini_update.docker['Upgrade_Version']:
                print('Docker Version is same')
            elif sw_ini_present.docker['Present_version'] < sw_ini_update.docker['Upgrade_Version']:    
                print('Upgrade present Docker version')
            elif sw_ini_present.docker['Present_version'] > sw_ini_update.docker['Upgrade_Version']:
                print('downgrade present Docker version')






                
