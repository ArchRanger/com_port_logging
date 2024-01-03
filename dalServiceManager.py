# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 17:55:38 2022

@author: archranger
"""

import datetime
import time
import com_port_scanning 
import json 
import database_cp  
import win32com.client


class DataObj:  
    def __init__(self, data: dict):
        self.data = data
        self.time = data.get("Time")
        self.port = data.get("Port")
        self.name = data.get("Name")
        self.seri_no = data.get("Seri_No")
        self.vid = data.get("Vid")
        self.pid = data.get("Pid")
        self.message = data.get("Message")

    def set_message(self, message):
        self.message = message



class DalJson:
    wmi = win32com.client.GetObject("winmgmts:")  
    h1,m1,s1,h2,m2,s2 = datetime.datetime.now().time().hour,datetime.datetime.now().time().minute,datetime.datetime.now().time().second,datetime.datetime.now().time().hour,datetime.datetime.now().time().minute,datetime.datetime.now().time().second  # uzun uzun saat ayarı düzenlemesi
    counter,mounter = 0,0
    alpha, theta = [],[]
    beta, omega = ["S"],["S"]  
                        

    while True:
        
        print("başladı;")
        for port in com_port_scanning.COMPorts.get_com_ports().data:  
            t = com_port_scanning.Time.time_now(self=0)
            p = port.device
            n = port.description
            sn = "None"
            if port.serial_number is not None:  
                
                sn = port.serial_number
            db = DataObj({
                        "Time": str(t),
                        "Port": str(p),
                        "Name": str(n),
                        "Seri_No": str(sn),
                        "Message": "mesaj yok."
            })
            print("port deneme: "+p)  # sadece deneme
            if not p == "COM5" and not p =="COM6":  
                
                alpha.append(db.data)  
                x = db.data            
                for a in alpha:
                    s = str(a.get("Seri_No"))
                    s= "12345678910"
                    if len(s) >=1:
                        print("none değil")  
                        a["Message"] = "Bu cihaz giris yapti."

                        if counter == 0: 
                            counter += 1  
                        if counter == 2:  
                            counter -= 1 
                        for b in beta:
                            if b != s:  
                                beta[0] = s  
                                h1=datetime.datetime.now().time().hour
                                m1=datetime.datetime.now().time().minute
                                s1=datetime.datetime.now().time().second 
                                with open('data.json',
                                          'a',encoding="utf-8") as json_dosya:  
                                    json.dump(a, json_dosya)
                                    json_dosya.write(',\n')
                                    # json_dosya.write('"Bu cihaz giris yapti.",\n') # bu satırı görmeyin,
                                database_cp.MySQL_processor_Port(a["Time"], a["Port"], a["Name"], a["Seri_No"], a["Message"]) 
                                com_port_scanning.time.sleep(3)  
            elif len(com_port_scanning.COMPorts.get_com_ports().data) == 2:  
                print("none ")  
                if len(alpha) >= 1:  
                    alpha.pop()  
                
                beta[0] = "S"  
                if counter == 1:  
                    y = com_port_scanning.Time_modifier(h1, m1, s1)
                    y = y.get_time()
                    x["Message"] = f"USB cihazi cikarildi. Takili durdugu sure: {y} "  
                    database_cp.MySQL_processor_Port(x["Time"], x["Port"], x["Name"], x["Seri_No"], x["Message"])
                    with open('data.json', 'a',encoding="utf-8") as json_dosya:  
                        json_dosya.write("\n")  
                        
                        json.dump(x, json_dosya)
                        json_dosya.write(",\n")

                        json_dosya.write("\n")
                    counter += 1
            else:
                time.sleep(0)

        for usb in wmi.InstancesOf("Win32_USBHub"): 
            tn, vid, pid, srn, nm = str(com_port_scanning.Time.time_now(self=0)), str(usb.DeviceID[8:12]), \
                                    str(usb.DeviceID[17:21]), str(usb.DeviceID[22:]), str(usb.Name)
            datb = DataObj({
                "Time": tn,
                "Name": nm.replace("ı", "i").replace("İ", "I").replace("ğ","g").replace("ü","u").replace("ç","c").replace("ö","o").replace("ş","s"),
                "Seri_No": srn,
                "Vid": vid,
                "Pid": pid,
                "Message": "mesaj yok"
            })
            if not str(usb.Name) == "USB Bileşik Aygıt" and not str(usb.Name) == "USB Kök Hub (USB 3.0)":
                theta.append(datb.data)
                _x = datb.data
                for t in theta:
                    _s = str(t.get("Seri_No"))
                    _s = "12345678910"
                    if len(_s) >= 1:
                        print("none değil")
                        t["Message"] = "Bu cihaz giris yapti."

                        if mounter == 0:
                            mounter += 1
                        if mounter == 2:
                            mounter -= 1
                        for o in omega:
                            if o != _s:
                                omega[0] = _s
                                h2 = datetime.datetime.now().time().hour
                                m2 = datetime.datetime.now().time().minute
                                s2 = datetime.datetime.now().time().second
                                with open('data.json',
                                          'a',encoding="utf-8") as json_dosya:  
                                    json.dump(t, json_dosya)
                                    json_dosya.write(',\n')
                                    # json_dosya.write('"Bu cihaz giris yapti.",\n')
                                database_cp.MySQL_processor_USB(t["Time"], t["Name"], t["Seri_No"], t["Vid"], t["Pid"], t["Message"])
                                com_port_scanning.time.sleep(3)
            elif len(wmi.InstancesOf("Win32_USBHub")) == 4:
                print("none2 ")
                if len(theta) >= 1:
                    theta.pop()
                # for i in range(counter):
                omega[0] = "S"
                if mounter == 1:
                    _y = com_port_scanning.Time_modifier(h2, m2, s2)
                    _y = _y.get_time()
                    _x["Message"] = f"USB cihazi cikarildi. Takili durdugu sure: {_y} "
                    database_cp.MySQL_processor_USB(_x["Time"], _x["Name"], _x["Seri_No"], _x["Vid"], _x["Pid"], _x["Message"])
                    with open('data.json', 'a', encoding="utf-8") as json_dosya:
                        json_dosya.write("\n")
                        # json_dosya.write(f"{_x}")
                        json.dump(_x, json_dosya)
                        json_dosya.write(",\n")

                        json_dosya.write("\n")
                    mounter += 1
                else:
                    time.sleep(0)





