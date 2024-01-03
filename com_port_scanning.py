import serial.tools.list_ports 
import time 
import datetime


class COMPorts:
    def __init__(self, data: list):  
        self.data = data

    @classmethod
    def get_com_ports(cls):  
        data = []
        ports = list(serial.tools.list_ports.comports())  
          

        for port_ in ports:  
            obj = Object(data=dict({"device": port_.device, "serial_number": port_.serial_number,
                                    "description": port_.description.split("(")[0].strip()}))
            data.append(obj)  
        return cls(data=data)  


class Object:  
    def __init__(self, data: dict): 
        self.data = data
        self.device = data.get("device")
        self.description = data.get("description")
        self.serial_number = data.get("serial_number")


class Time:  
    def time_now(self):
        t = time.localtime()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)  

        return current_time


class Time_modifier:

    def __init__(self,h,m,s):  
        self.h = datetime.datetime.now().time().hour  
        self.m = datetime.datetime.now().time().minute  
        self.s = datetime.datetime.now().time().second
        if self.h > h:
            self.h = abs(self.h - h)
            self.m += 60
            if self.m + m >= 2*max(self.m, m):
                self.h = abs(self.h - h)
        else:
            self.h =abs(h - self.h)
        if self.m > m:
            self.s += 60
            if self.s + s >= 2*max(self.s, s):
                self.m = abs(self.m - m)
            else:
                m += 1   # 26 - 13
                self.m = abs(self.m - m)
        else:
            self.m =abs(m - self.m)
        if self.s >= s:
            self.s = abs(self.s - s)
        else:
            self.s =abs(s - self.s)
        self.x = f"{self.h}:{self.m}:{self.s}"

    def get_time(self):
        return self.x


class F_Json_Regulator:
    fList = []

    def __init__(self, data, on, jsn):
        self.data = data
        self.jsn = jsn
        self.on = on
        with open(jsn, 'r+', encoding='utf-8') as f:

            f.seek(0)
            f.write("[\n\n{'")
            if on != 1:
                f.read()
                t = f.tell()
                f.seek(t - 3)
                f.write(',')
                f.write(str(data))
            else:
                f.write(str(data))
            f.write('\n]')
            f.seek(0)


# class F_Json_Regulator:
#
#     def __init__(self, data, on, jsn):
#         self.data = data
#         self.jsn = jsn
#         self.on = on
#         with open(jsn, 'r+', encoding='utf-8') as f:
#
#             f.seek(0)
#             f.write('[\n\n')
#             if on != 0:
#                 f.read()
#                 t = f.tell()
#                 f.seek(t - 3)
#                 f.write(',')
#                 f.write(data)
#             else:
#                 f.write(data)
#             f.write('\n]')
#             f.seek(0)







