import configparser
from distutils.command.config import config
import os
import datetime
from shutil import copytree, ignore_patterns
import sys

destination = '/home/pi/Desktop/SEM_code/Sem_Source_code_v4.002/Bootloader_files/back_%s'%datetime.datetime.now()
source_directory='/media/pi/PENDRIVE/FIRMWARE_UPDATE/SEM_code'
files = os.listdir(source_directory)
try :
    for f in files:
        #create the files 
        source = '/media/pi/PENDRIVE/FIRMWARE_UPDATE/SEM_code/%s' % f
        copytree(source, destination, ignore=ignore_patterns('.pyc', 'tmp'))    
except Exception as e:
    print(e)


