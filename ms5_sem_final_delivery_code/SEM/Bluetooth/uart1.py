import socket   
from ast import Str
import os
import requests
import json
from inspect import Parameter
from multiprocessing.dummy import Value
import numbers
from threading import Thread
from optparse import Values
from pkgutil import get_data
import sys
from threading import local
from tkinter import N
from tokenize import Number
from turtle import fd
from unicodedata import name
import dbus, dbus.mainloop.glib
from gi.repository import GLib
from example_advertisement import Advertisement
from example_advertisement import register_ad_cb, register_ad_error_cb
from example_gatt_server import Service, Characteristic
from example_gatt_server import register_app_cb, register_app_error_cb
#import header1
import time
import init
from Hotspot import hotspot_ethernet



BLUEZ_SERVICE_NAME =           'org.bluez'
DBUS_OM_IFACE =                'org.freedesktop.DBus.ObjectManager'
LE_ADVERTISING_MANAGER_IFACE = 'org.bluez.LEAdvertisingManager1'
GATT_MANAGER_IFACE =           'org.bluez.GattManager1'
GATT_CHRC_IFACE =              'org.bluez.GattCharacteristic1'
UART_SERVICE_UUID =            '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
UART_RX_CHARACTERISTIC_UUID =  '6e400002-b5a3-f393-e0a9-e50e24dcca9e'
UART_TX_CHARACTERISTIC_UUID =  '6e400003-b5a3-f393-e0a9-e50e24dcca9e'
LOCAL_NAME =                   'SEM_HUSSMANN_BLE'
mainloop = None
macro='''
start_of-frame=0
client_side=2
server_side=3
read=r
write=w
'''
#from python.enum import Parameter_name
#import json 

DATAthread=None

class TxCharacteristic(Characteristic):
    def __init__(self, bus, index, service):
        Characteristic.__init__(self, bus, index, UART_TX_CHARACTERISTIC_UUID,
                                ['notify'],service)
        self.notifying = False
        #GLib.io_add_watch(sys.stdin, GLib.IO_IN,self.on_console_input)
        init.DATAthread=Thread(target=self.TXthread)
            
    # def on_console_input(self, fd):
    #     s = fd.readline()
    #     if s.isspace():
    #         pass
    #     else:
    #         self.send_tx(s)
    #     return True

    def TXthread(self):
        time.sleep(1)
        while(1):
            if(init.Tx_Flag == True):
                init.Tx_Flag = False
                # str="hello"
                # time.sleep(1)
                self.send_tx(init.Tx_buff)
            time.sleep(0.1)
            
            # return True

    def send_tx(self,s):
        if not self.notifying:
            return
        value = []
        for c in s:
            value.append(dbus.Byte(c.encode()))
        self.PropertiesChanged(GATT_CHRC_IFACE, {'Value': value}, [])
        
        


    def StartNotify(self):
        if self.notifying:
            return
        
        print("it is connected")
        self.notifying = True
        init.Connection_Flag = True

    def StopNotify(self):
        if not self.notifying:
            return
        print("disconnected")
        self.notifying = False
        init.Connection_Flag = False
    


def RXthread():
    time.sleep(1)
    
    while(1):
        if(init.Rx_Flag == True):
            init.Rx_Flag = False

            # init.Tx_Flag = True
            data=init.Rx_buff 
            daya_check(data)
            print(data)

        time.sleep(1)

def daya_check(data):
    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname)     
    
    if data == '1':
        print("Read_db1")
        try:
            response = requests.get("http://localhost:8000/api/xr75/sec/")
            dict_count = response.json()
            total_pram = (len(dict_count[0].keys()) - 3)
            row_count = (len([e for e in dict_count if isinstance(e, dict)]))
            print("Total Number of Prameters in 10-Seconds Data Table:",total_pram)
            print("Total Number of Rows(Entires) in Seconds Data Table:",row_count)
            data_to_send="Total Number of Prameters in 10-Seconds Data Table:"+total_pram +"Total Number of Rows(Entires) in Seconds Data Table:"+row_count
            init.Tx_buff=data_to_send
            init.Tx_Flag = True
        except:
            print("server down")
            init.Tx_buff="server down"
            init.Tx_Flag = True
            

    elif data == '2':
        print("Read_db2")
        try:
            response = requests.get("http://localhost:8000/api/xr75/min/")
            dict_count = response.json()
            total_pram = (len(dict_count[0].keys()) - 3)
            row_count = (len([e for e in dict_count if isinstance(e, dict)]))
            print("Total Number of Prameters in 5-Minutes Data Table:",total_pram)
            print("Total Number of Rows(Entires) in Minutes Data Table:",row_count)
            data_to_send="Total Number of Prameters in 5-Minutes Data Table:"+total_pram +"Total Number of Rows(Entires) in Minutes Data Table:"+row_count
            init.Tx_buff=data_to_send
            init.Tx_Flag = True
        except:
            print("server down")
            init.Tx_buff="server down"
            init.Tx_Flag = True
    elif data == '3':
        print("Read_db3")
        try:
            response = requests.get("http://localhost:8000/api/xr75/hour/")
            dict_count = response.json()
            total_pram = (len(dict_count[0].keys()) - 3)
            row_count = (len([e for e in dict_count if isinstance(e, dict)]))
            print("Total Number of Prameters in 4-Hours Data Table:",total_pram)
            print("Total Number of Rows(Entires) in Hours Data Table:",row_count)
            data_to_send="Total Number of Prameters in 4-Hours Data Table:"+total_pram +"Total Number of Rows(Entires) in Hours Data Table:"+row_count
            init.Tx_buff=data_to_send
            init.Tx_Flag = True
        except:
            print("server down")
            init.Tx_buff="server down"
            init.Tx_Flag = True
    elif data == '4':
        print("Read_ip_address",IPAddr)
        data_to_send="Read_ip_address = "+IPAddr
        init.Tx_buff=data_to_send
        init.Tx_Flag = True
    elif data == '5':
        # print(os.popen('sudo iwgetid -r').read())
        print("Read_WiFi acess point ssid name:",os.popen('sudo iwgetid -r').read())
    elif data == '6':
        print("Read_WiFi acess point password")
    elif data == '7':
        config_api='http://'+IPAddr+':8000/api/xr75/config/'
        sec_api='http://'+IPAddr+':8000/api/xr75/sec/'
        min_api='http://'+IPAddr+':8000/api/xr75/min/'
        hour_api='http://'+IPAddr+':8000/api/xr75/hour/'
        print(config_api,sec_api,min_api,hour_api)
        print("Read_SuportedREST api's")
        min_api='http://'+IPAddr+':8000/api/xr75/min/'
        data_to_send="1)"+config_api+" 2)"+sec_api+" 3)"+min_api+" 4)"+hour_api
        init.Tx_buff=data_to_send
        init.Tx_Flag = True
    elif data == '8':
        user_name="Reas SEM Module user name = "+os.getlogin()
        print(user_name)
        data_to_send=user_name
        init.Tx_buff=data_to_send
        init.Tx_Flag = True

def Tx_handle():
    time.sleep(1)
    while(1):

        if(init.Connection_Flag == True):
            with open("Read_Configuration.json") as f:
                data=json.load(f)
                length=len(data[0])
                init.Tx_buff = ""

                # for key,value in list(data[0].items()):
                #     if((key=="created_on") or (key=="modified_on")):
                #         init.Tx_buff += str(key) + ":-" + str(value) + "\n"
                #     # init.Tx_buff+=length
                # print((init.Tx_buff))

                # if(init.Connection_Flag == True):
                #     if(init.Tx_Flag == False):
                #         init.Tx_Flag = True
                #     else:
                #         pass
                # else:
                #     break
                time.sleep(10)
        time.sleep(1)
                
                # if data[0]:
                #     for i in range(0,3):
                #         if data[i]:
                #             for j in data[i]:
                #                 init.Tx_buff=j
                #                 init.Tx_Flag = True
                #                 c+=1
                # else:
                #     break
                        

         

            # if(init.Tx_Flag == False):
            #     # init.Tx_buff = "Sandeep"
            #     init.Tx_Flag = True
            # else:
            #     pass
            # data=init.Rx_buff 
            # print(data)
            
       

class RxCharacteristic(Characteristic):
    def __init__(self, bus, index, service):
        Characteristic.__init__(self, bus, index, UART_RX_CHARACTERISTIC_UUID,
                                ['write'], service)
        

    def WriteValue(self, value, options):
        print(value)
        print(value[0])
        if(value[0]== 1):
            print()
        print(type(value[0]))
        global Rx_Flag
        value=format(bytearray(value).decode())
        init.Rx_buff = value
        init.Rx_Flag = True
        
       
        # print("\n")
        # c=bytes(value)
        # print(c)
        # d=c.decode("\""+'utf-8'+"\"")
        # e=int(d)
        # print(d)
        # print(type(d))
        # e=((str(d)))
        # print(type(e))
        # print(e)
        # print(e[0])
        # print(type(e[0]))

        # # n=(e[0])
        # # print(n)
        # if(e[0]==str(0)):
        #     print("##")
        #     if(e[1]>=str(1)and e[1]<=str(2)):
        #         print("###")
        #         if((e[2]>=str(1)) and e[2]<=str(8)):
        #             c=(e[2])
        #             print(c)
        #             print("###")
        #             d=int(str(c))
        #             print(type(d))
        #             n=hex(int(d))
        #             print(n)
        #             if(e[3]==str(0)) :
        #                 print("#")
        #                 # print(e[3])
        #                 # m=(int(e[3]))
        #                 # p=m
        #                 # print(p)
        #                 # print(type(m))
        #                 if(e[3]==str(0)):
        #                     m=int(e[4])
        #                     print(m)
        #                     print(type(m))
        #                     parameter=Parameter_name(m).name
        #                     print(parameter)
        #                     print("####")
        #                     f=open('data.json')
        #                     data=json.load(f)
        #                     print(data)
        #                     j=0
        #                     print("#")
        #                     key=data.keys()
        #                     value=data.values()
        #                     key1=list(key)
        #                     value1=list(value)
        #                     print(key1)
        #                     print(value1)
        #                     print("#1")
        #                     for i in key1:
        #                         print(key1)
        #                         print("#####")
        #                         if(key1[j]==parameter):
        #                             print("########")
        #                             key_name=key1[j]
        #                             value_1=value1[j]
        #                             s=({key_name:value_1})
        #                             send_data=TxCharacteristic.send_tx(self, value_1)
        #                             print(send_data)
                                 
            

        
                  
                

                # if((d[2]==str(3))and d[2]==str(4)):
                #     print("hi")
            
   
                    
                   
        


        # a=(d>>3)
        # print(a)
        # if(((d>>3)and 1)==0):
            # print("hi")


        # print(type(e))
        #c.hex()
        #print(c.hex())
        #print(binascii.hexlify(c))
        # print(type(c))
        # d=c.decode("utf-8")
        # print(d)

        # a=('remote: {}'.format(bytearray(value).decode()))
        # print(type(a))
        # #print(str(a))
        # #print(hex(a))
        # print(a[8])
        # if(a[8]==str(0)):
        #     if(a[9]):
        #         print("hi")
            


        # if a in range(0,5):
        #     b=int(a)
        #     print(type(b))
        #     print(b)


        #print(a)
        #b=(type(a))
        #print(b)
            #if(b=='int'):
        # c=self.get_data(a)
        # print(c)

    
    # def get_data(self, bus, n):
    #     global number
    #     number=n
    #     object1=header1.uuid_of_parameter()
    #     print(object1)
    #     return object1

        

class UartService(Service):
    def __init__(self, bus, index):
        Service.__init__(self, bus, index, UART_SERVICE_UUID, True)
        self.add_characteristic(TxCharacteristic(bus, 0, self))
        self.add_characteristic(RxCharacteristic(bus, 1, self))

class Application(dbus.service.Object):
    def __init__(self, bus):
        self.path = '/'
        self.services = []
        dbus.service.Object.__init__(self, bus, self.path)

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_service(self, service):
        self.services.append(service)

    @dbus.service.method(DBUS_OM_IFACE, out_signature='a{oa{sa{sv}}}')
    def GetManagedObjects(self):
        response = {}
        for service in self.services:
            response[service.get_path()] = service.get_properties()
            chrcs = service.get_characteristics()
            for chrc in chrcs:
                response[chrc.get_path()] = chrc.get_properties()
        return response

class UartApplication(Application):
    def __init__(self, bus):
        Application.__init__(self, bus)
        self.add_service(UartService(bus, 0))

class UartAdvertisement(Advertisement):
    def __init__(self, bus, index):
        Advertisement.__init__(self, bus, index, 'peripheral')
        self.add_service_uuid(UART_SERVICE_UUID)
        self.add_local_name(LOCAL_NAME)
        self.include_tx_power = True

def find_adapter(bus):
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),
                               DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()
    for o, props in objects.items():
        if LE_ADVERTISING_MANAGER_IFACE in props and GATT_MANAGER_IFACE in props:
            return o
        print('Skip adapter:', o)
    return None

def Mainthread():
    time.sleep(2)
    mainloop.run()

def main():
    global mainloop
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    adapter = find_adapter(bus)
    if not adapter:
        print('BLE adapter not found')
        return

    service_manager = dbus.Interface(
                                bus.get_object(BLUEZ_SERVICE_NAME, adapter),
                                GATT_MANAGER_IFACE)
    ad_manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter),
                                LE_ADVERTISING_MANAGER_IFACE)

    app = UartApplication(bus)
    adv = UartAdvertisement(bus, 0)

    mainloop = GLib.MainLoop()

    service_manager.RegisterApplication(app.get_path(), {},
                                        reply_handler=register_app_cb,
                                        error_handler=register_app_error_cb)
    ad_manager.RegisterAdvertisement(adv.get_path(), {},
                                     reply_handler=register_ad_cb,
                                     error_handler=register_ad_error_cb)


    init.initialization()  

    try:
        
        DATAthread1=Thread(target=RXthread)
        mainthread=Thread(target=Mainthread)
        Txthread=Thread(target=Tx_handle)
        init.DATAthread.start()
        DATAthread1.start()
        mainthread.start()
        Txthread.start()
        init.DATAthread.join()
        # DATAthread1.join()
        # mainthread.join()
        #mainloop.run()
    except Exception as e:
        print(e)
        adv.Release()

if __name__ == '__main__':
    main()