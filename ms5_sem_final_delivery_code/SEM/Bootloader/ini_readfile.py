#import configuration
import configparser
from distutils.command.config import config

#mporting required modules to read raspberry pi username
import pwd

#import shutil 
from shutil import copytree, ignore_patterns
import shutil

# import everything from tkinter module
from tkinter import *

# import messagebox from tkinter module
import tkinter.messagebox

# create a tkinter root window
# global root
# root = tkinter.Tk()

# import system  
import sys
import os
import subprocess

# import cron tab 
from crontab import CronTab

# import threading 
from threading import Thread
import time

# import gpio packages
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time modul

# reading the raspberrypi username
global Raspberry_pi_username
Raspberry_pi_username=pwd.getpwuid(os.getuid())[0]

# defalut "Restart_led" pin and "switch" pin
Restart_led=37
switch=12
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Restart_led, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(switch, GPIO.IN)
GPIO.output(Restart_led,GPIO.HIGH)
same_version_flag=False
# dir_path =  os.path.abspath((os.curdir))
# print(dir_path)
dir_path =  os.path.abspath(os.path.dirname(sys.argv[0]))
dir_path = dir_path.replace("/Bootloader",'')
os.chdir(dir_path)

# # root window title and dimension
# root.title("When you press a button the message will pop up")
# root.geometry('500x300')

# Create a messagebox showinfo
def onClick_restart():
	tkinter.messagebox.showinfo("Welcome to GFG.", "restart")
	subprocess.call(["sudo","reboot"])

def onClick_cancel():
	tkinter.messagebox.showinfo("Welcome to GFG.", "cancel")

def main_run():

	while 1:
		# root.mainloop()
		GPIO.output(Restart_led, GPIO.HIGH)
		time.sleep(0.2)
		GPIO.output(Restart_led, GPIO.LOW)
		time.sleep(0.2)
		# print('Switch status = ', GPIO.input(switch))
		if( GPIO.input(switch) == True):
			print("reboot the raspberry pi ")
			GPIO.cleanup()
			subprocess.call(['sudo','reboot'])
            
# #to check wether the bootloades is working or not 
# button_restart = Button(root, text="restart", command=onClick_restart, height=5, width=10)
# button_cancel= Button(root, text="cancel", command=onClick_cancel, height=5, width=10)
# button_restart.pack(side='bottom')
# button_cancel.pack(side='bottom')
# non_blobking_thread = Thread(target=main_run)
# non_blobking_thread.start()
# root.mainloop()
def main():
    pendrive_exist=False

    while 1:
        time.sleep(2)
        pendrive_inserted=False 
        pendrive_status_flag_2=False 

        update_version_flag=False
        flag=False
        # partitionsFile = open("/proc/partitions")
        # print(partitionsFile)
        # lines = partitionsFile.readlines()[2:]#Skips the header lines
        # print(lines)
        # for line in lines:
        #     words = [x.strip() for x in line.split()]
        #     minorNumber = int(words[1])
        #     deviceName = words[3]
        #     if minorNumber % 16 == 0:
        #         path = "/sys/class/block/" + deviceName
        #         if os.path.islink(path):
        #             var_1=os.path.realpath(path).find("/usb")
        #             # pendrive_status_flag_1=False 
        #             # pendrive_status_flag_2=False 
        #             if var_1 > 0:
        # while 1:
        try:
            present_dir = os.getcwd()
            if((os.path.exists("/media/"+Raspberry_pi_username+"/PENDRIVE")) and (pendrive_exist==False)):
                pendrive_exist=True
                if(os.path.exists("/media/"+Raspberry_pi_username+"/PENDRIVE/FIRMWARE_UPDATE/DataBase_back_up") ):
                    # present_dir = os.getcwd()
                    os.chdir("/media/"+Raspberry_pi_username+"/PENDRIVE/FIRMWARE_UPDATE/DataBase_back_up")
                    subprocess.call(['chmod','+x',present_dir+'/Bootloader'+'/db_bup.sh'])
                    subprocess.call(['sh', present_dir+'/Bootloader'+'/db_bup.sh' ])
                    os.chdir(present_dir)
                else:
                    print("")
              
                GPIO.output(Restart_led,GPIO.HIGH)
                pendrive_inserted = True
                # present directory 
                Dir_path =  os.path.abspath(os.path.dirname(sys.argv[0]))
                # print(Dir_path)
                time.sleep(5)
                #file locations
                path=Dir_path+'/source_back_up/MainCode/'

                Config_present = configparser.ConfigParser()
                Config_present.read(dir_path+"/Bootloader/Bootloader_conf.ini")
                if((os.path.exists("/media/"+Raspberry_pi_username+"/PENDRIVE/FIRMWARE_UPDATE/Bootloader_conf.ini") ) and (os.path.exists("/media/"+Raspberry_pi_username+"/PENDRIVE/FIRMWARE_UPDATE/MainCode"))):
                    Config_update = configparser.ConfigParser()
                    Config_update.read("/media/"+Raspberry_pi_username+"/PENDRIVE/FIRMWARE_UPDATE/Bootloader_conf.ini")

                    update_version = float(Config_update.get('CODE', 'Version'))
                    # print("update_version",update_version)
                    flag=False
                    present_version = float(Config_present.get('CODE', 'Version'))
                    pendrive_status_flag_2=True 
                    if (present_version == update_version):
                        if(same_version_flag==False):
                            print('present_version=',present_version, 'update_version=',update_version )
                            print("no need to copy the code ")
                            same_version_flag=True
                        # new_destination=path
                        # try:
                        #     shutil.rmtree(new_destination)  # empty the directory
                        # except Exception as e:
                        #     print('New File created') 
                    if (((present_version < update_version) or ( present_version > update_version ) ) and (update_version_flag==False)):
                        update_version_flag=True
                        same_version_flag=True
                        print('present_version=',present_version, 'update_version=',update_version )
                        print("copy the code")
                        source_directory='/media/'+Raspberry_pi_username+'/PENDRIVE/FIRMWARE_UPDATE/'
                        files = os.listdir(source_directory)
                        # new_version='version_%s'%datetime.datetime.now()
                        new_version='Version_4.001'
                        new_destination=path+new_version
                        # new_destination='/home/pi/Desktop/SEM/MainCode/source_back_up/MainCode'+new_version
                        try:
                            shutil.rmtree(new_destination)  # empty the directory
                        except Exception as e:
                            print('New File created')    
                        try :
                            for f in files:
                                #create the files
                                if f == 'MainCode':
                                    source = '/media/'+Raspberry_pi_username+'/PENDRIVE/FIRMWARE_UPDATE/MainCode'
                                    copytree(source, new_destination , ignore=ignore_patterns('.pyc', 'tmp'))  
                                    flag = True
                        except Exception as e:
                            print(e)
                    Config_present = configparser.ConfigParser()
                    Config_present.read(dir_path+"/Bootloader/Bootloader_conf.ini")
                    Config_present['CODE']['version'] = str(update_version)
                    with open(dir_path+"/Bootloader/Bootloader_conf.ini",'w') as config_file:
                        Config_present.write(config_file)
                        config_file.close()
                else:
                    if(os.path.exists("/media/"+Raspberry_pi_username+"/PENDRIVE/FIRMWARE_UPDATE/Controller_Select/Controller_Select.ini")):
                        # os.chdir("/media/"+Raspberry_pi_username+"/PENDRIVE/FIRMWARE_UPDATE/Controller_Select")
                        Controller_Varient_read_in_p = configparser.ConfigParser()
                        Controller_Varient_read_in_p.read("/media/"+Raspberry_pi_username+"/PENDRIVE/FIRMWARE_UPDATE/Controller_Select/Controller_Select.ini")
                        Controller_varient_in_P = str(Controller_Varient_read_in_p.get('CONTROLLER', 'varient'))
                        Controller_Varient_read_in_sem = configparser.ConfigParser()
                        Controller_Varient_read_in_sem.read(dir_path+"/MainCode/Present_version/Controller_select.ini")
                        Controller_varient_in_sem = str(Controller_Varient_read_in_sem.get('CONTROLLER', 'varient'))
                        if(Controller_varient_in_P != Controller_varient_in_sem):
                            Controller_Varient_read_in_sem['CONTROLLER']['varient'] = str(Controller_varient_in_P)
                            with open(dir_path+"/MainCode/Present_version/Controller_select.ini",'w') as config_file:
                                Controller_Varient_read_in_sem.write(config_file)
                                config_file.close()
                            # subprocess.call(['sudo reboot'])
                    else:
                        print("")
                if flag == True :
                    # try:
                    #     # subprocess.call(['cd ..'])
                    #     # os.chdir("..")
                    #     # os.chdir("..")
                    #     # subprocess.call(['ls'])
                    #     # Dir_path_1 =  os.path.abspath(os.path.dirname(sys.argv[0]))
                    #     # print(Dir_path_1)
                    #     # os.chdir(Dir_path+"/sem_django")
                    #     shutil.rmtree('/home/pi/Desktop/SEM/MainCode/Previous_version_1')  # empty the directory
                    # except Exception as e:
                    #     print(e) 
                    # source =dir_path+"/Bootloader/source_back_up/MainCode/Version_4.001"
                    source =dir_path+"/Bootloader/source_back_up/MainCode/Latest_backup"
                    destination =dir_path+"/MainCode/Present_new_code"
                    files = os.listdir(source)
                    try :
                        for f in files:
                            copytree(source, destination , ignore=ignore_patterns('.pyc','tmp'))  
                            flag = True
                    except Exception as e:
                        print("")

                    # DIR_Change = 
                    # os.chdir(dir_path+"/MainCode")
                    cron = CronTab(user=Raspberry_pi_username)
                    print("befor")
                    for item in cron:
                        print(item)
                    cron.remove_all(comment='SEM_ON_Reboot')
                    cron.write()
                    os.rename(dir_path+"/MainCode/Previous_version",dir_path+"/MainCode/Previous_version_1")
                    os.rename(dir_path+"/MainCode/Present_version",dir_path+"/MainCode/Previous_version")
                    os.rename(dir_path+"/MainCode/Present_new_code",dir_path+"/MainCode/Present_version")
                    shutil.rmtree(dir_path+"/MainCode/Previous_version_1")  # empty the directory
                    # shutil.rmtree('/home/pi/Desktop/SEM/MainCode/Present_new_code')  # empty the directory

                    cron = CronTab(user=Raspberry_pi_username)

                    job = cron.new(command='python ' + dir_path+"/MainCode/Present_version" + '/main.py', comment='SEM_ON_Reboot')
                    job.every_reboot() 
                    print("after")

                    for item in cron:
                        print(item)
                    cron.write()
                    # button_restart = Button(root, text="Restart", command=onClick_restart, height=5, width=10)
                    # button_cancel= Button(root, text="cancel", command=onClick_cancel, height=5, width=10)
                    # button_restart.pack(side='bottom')
                    # button_cancel.pack(side='bottom')
                    #GPIO Switch 
                    non_blobking_thread = Thread(target=main_run)
                    non_blobking_thread.start()
                    #pop up will display, click restart to reboot 
                    # root.mainloop()
                

            elif(os.path.exists("/media/"+Raspberry_pi_username+"/PENDRIVE") == False):
                pendrive_exist=False

        except Exception as e:
            print(e)
        if(pendrive_inserted == False):
            same_version_flag=False    
        # print("Please insert the pendrive")
                # pendrive_status_flag_1=True   

        # if ((pendrive_status_flag_1 == True) and (pendrive_status_flag_2 == True)):
        #     print("Please insert the pendrive")


if __name__ == "__main__":
    
    # ###################################
    # import RPi.GPIO as GPIO 
    # from time import sleep
    # while 1:
    #     GPIO.setwarnings(False) # Ignore warning for now
    #     GPIO.setmode(GPIO.BOARD)
    #     Pin_num=38
    #     GPIO.setup(Pin_num, GPIO.OUT, initial=GPIO.LOW)
    #     while 1:   
    #         GPIO.output(Pin_num,GPIO.HIGH) 
    #         sleep(1)
    #         GPIO.output(Pin_num,GPIO.LOW) 
    #         sleep(1)
    # ###################################
    main()


































































































# if present_version > update_version :
#     print('present_version=',present_version, 'update_version=',update_version )
#     print("downgrade the code ")
#     source_directory='/media/pi/PENDRIVE/FIRMWARE_UPDATE/'
#     files = os.listdir(source_directory)
#     # new_version='version_%s'%datetime.datetime.now()
#     new_version='Version_4.001'
#     new_destination=Dir_path+'/source_back_up/MainCode/'+new_version
#     try:
#         shutil.rmtree(new_destination)
#     except Exception as e:
#         print("New File created") 
#     # for f in os.listdir(Dir_path+'/source_back_up'):
#     #     os.remove(os.path.join(dir, f))
#     try :
#         for f in files:
#             #create the files
#             if f == 'MainCode':
#                 source = '/media/pi/PENDRIVE/FIRMWARE_UPDATE'
#                 copytree(source, new_destination, ignore=ignore_patterns('.pyc', 'tmp'))    
#     except Exception as e:
#         print(e)




# previous_version = float(Config_present.get('CODE', 'Version'))
# if previous_version == 4.002:
#     print("same version ",previous_version)
# if previous_version < 4.002:
#     # print("downgrade ",previous_version)
#     if Config_present.get('CODE', 'Change') == "downgrade" :

#         Dir_path =  os.path.abspath(os.path.dirname(sys.argv[0]))
#         print(Dir_path)
#         source_directory='/media/pi/PENDRIVE/FIRMWARE_UPDATE/'
#         files = os.listdir(source_directory)
#         importing_file_flag= False

#         # destination path to copy the files  
#         destination = '/home/pi/Desktop/SEM/Bootloader/back_%s'%datetime.datetime.now()
#         source_directory='/media/pi/PENDRIVE/FIRMWARE_UPDATE/'
#         try :
#             for f in files:
#                 file_2=os.listdir(source_directory+f)
#                 for f1 in file_2:
#                     if(f1 == 'software_ini.py'):
#                         print("file found")
#                         importing_file_flag=True
                
#         except Exception as e:
#             print(e)



#         try :
#             for f in files:
#                 #create the files 
#                 source = '/media/pi/PENDRIVE/FIRMWARE_UPDATE/%s' % f
#                 copytree(source, destination, ignore=ignore_patterns('.pyc', 'tmp'))    
#         except Exception as e:
#             print(e)



#         print("DOWN_GRADING")
# if previous_version > 4.002:
#     # print("upgrade version ",previous_version)
#     if Config_present.get('CODE', 'Change') == "upgrade" :

#         Dir_path =  os.path.abspath(os.path.dirname(sys.argv[0]))
#         print(Dir_path)
#         source_directory='/media/pi/PENDRIVE/FIRMWARE_UPDATE/'
#         files = os.listdir(source_directory)
#         importing_file_flag= False

#         # destination path to copy the files  
#         destination = '/home/pi/Desktop/SEM/Bootloader/back_%s'%datetime.datetime.now()
#         source_directory='/media/pi/PENDRIVE/FIRMWARE_UPDATE/'
#         try :
#             for f in files:
#                 file_2=os.listdir(source_directory+f)
#                 for f1 in file_2:
#                     if f1 == 'SEM':
#                         for f2 in f1:
#                             if f2 == 'Bootloader':
#                                 for f3 in f2:
#                                     if(f3 == 'software_ini.py'):
#                                         print("file found")
#                                         importing_file_flag=True
#         except Exception as e:
#             print(e)



#         try :
#             for f in files:
#                 #create the files 
#                 source = '/media/pi/PENDRIVE/FIRMWARE_UPDATE/%s' % f
#                 copytree(source, destination, ignore=ignore_patterns('.pyc', 'tmp'))    
#         except Exception as e:
#             print(e)
    
# print(Config.get('CODE', 'Change'))

