import datetime
import time
import com_port_scanning  # ilgili class import edildi
import json  # JSON kütüphanesi eklendi
import database_cp  # Database işlemleri sayfası
import win32com.client  # usb taramada gerekli modül


class DataObj:  # portlar için daha detaylı bir obje
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


# Database işlemleri için veriler JSON dosyasına çevriliyor.
# (Çalıştırılacak olan ve oluşturulan her modül dahil varlıkları kullanan ana sınıf.)
class DalJson:
    wmi = win32com.client.GetObject("winmgmts:")  # usb'yi obje şeklinde çekecek method
    h1,m1,s1,h2,m2,s2 = datetime.datetime.now().time().hour,datetime.datetime.now().time().minute,datetime.datetime.now().time().second,datetime.datetime.now().time().hour,datetime.datetime.now().time().minute,datetime.datetime.now().time().second  # uzun uzun saat ayarı düzenlemesi
    counter,mounter = 0,0
    alpha, theta = [],[]
    beta, omega = ["S"],["S"]  # bunların her birisi hem usb hem port taraması
                        # için oluşturulan "ikişer adet ayrı" değişkenler (alpha-port theta-usb, h1-port h2-usb).

    while True:
        # while döngüsü ile portlar 2 saniyelik delay ile kayt işlemi yapılmaktadır. (çok daha farklı bir hal aldı.)
        print("başladı;")
        for port in com_port_scanning.COMPorts.get_com_ports().data:  # ilk sayfadaki port objesinin datası alınıyor
            t = com_port_scanning.Time.time_now(self=0)
            p = port.device
            n = port.description
            sn = "None"
            if port.serial_number is not None:  # portta seri numarası var ise yukarıdaki
                                                # obje içerisine değişkenler tanınıyor
                sn = port.serial_number
            db = DataObj({
                        "Time": str(t),
                        "Port": str(p),
                        "Name": str(n),
                        "Seri_No": str(sn),
                        "Message": "mesaj yok."
            })
            print("port deneme: "+p)  # sadece deneme
            if not p == "COM5" and not p =="COM6":  # otomatik olarak içerideki algılanan
                                                    # 5 ve 6. portları görmezden gelmesi için
                alpha.append(db.data)  # yukarıdaki alpha listesine şu oluşturulan objenin "data"sını ekledik
                x = db.data            # datayı aynı zamanda x ismini verdiğimiz bir değişkene de atadık
                for a in alpha:
                    s = str(a.get("Seri_No"))
                    s= "12345678910"
                    if len(s) >=1:
                        print("none değil")  # burası dahil şu 4 satır biraz gereksiz gibi, çok takılmamak lazım
                        a["Message"] = "Bu cihaz giris yapti."

                        if counter == 0:  # burası biraz karışık, sayaç 0'sa (hiç girmemişse bir cihaz) 1 artırsın
                            counter += 1  # ve bir daha giriş olmuşsa, 2 olmuşsa 1 eksilsin. Dolayısıyla sayaç
                        if counter == 2:  # 0 iken (cihaz çıkmış mesajı vermesin) ancak cihaz var iken çıkarılma
                            counter -= 1  # yapıldığında sayaç eksilip altlardaki kodlarda onun mesajı yazdırılıyor
                        for b in beta:
                            if b != s:  # beta listesindeki her bir b eğer s'ye eşit değilse eşitliyor, sonra tekrar
                                beta[0] = s  # değiştiriliyor, sebebi her farklı cihaz girişinde kontrol mekanizması.
                                h1=datetime.datetime.now().time().hour
                                m1=datetime.datetime.now().time().minute
                                s1=datetime.datetime.now().time().second  # cihaz giriş yaptığında süreyi almak
                                com_port_scanning.F_Json_Regulator(a,counter-1,"data.json")
                                database_cp.MySQL_processor_Port(a["Time"], a["Port"], a["Name"], a["Seri_No"], a["Message"])  # json'a atmayla birlikte database'e de gönderme yapılıyor
                                com_port_scanning.time.sleep(3)  # (diğer modül içerisine gönderilerek)
            elif len(com_port_scanning.COMPorts.get_com_ports().data) == 2:  # sadece 2 veri,
                print("none ")  # (com5 ve 6) var demektir ve boş saymasını istiyoruz bu durumda, ve listeden eksiltme
                if len(alpha) >= 1:  # yapıyoruz yukarılarda bahsedildiği gibi.
                    alpha.pop()  # alpha'da varsa obje (sadece 5 ve 6 kaldığı için) var olan bu obje çıkarılıyor
                # for i in range(counter): # (burayı da görmeyin)
                beta[0] = "S"  # beta tekrar eski haline dönüştürüldü, tekrar yeni cihaz alacak hale getirildi
                if counter == 1:  # bu haldeyken sayaç 1 ise daha önceki alınan süre ile geçen zamanı buluyor
                    y = com_port_scanning.Time_modifier(h1, m1, s1)
                    y = y.get_time()
                    x["Message"] = f"USB cihazi cikarildi. Takili durdugu sure: {y} "  # bunları falan yazıyor
                    database_cp.MySQL_processor_Port(x["Time"], x["Port"], x["Name"], x["Seri_No"], x["Message"])
                    with open('data.json', 'a',encoding="utf-8") as json_dosya:  # hem database'e hem de json
                        json_dosya.write("\n")  # dosyasına çıkış yapıldığı ve süre bilgileri yazılıyor.
                        # json_dosya.write(f"{x}") # (burayı da görmeyin)
                        json.dump(x, json_dosya)
                        json_dosya.write(",\n")

                        json_dosya.write("\n")
                    counter += 1
            else:
                time.sleep(0)

        for usb in wmi.InstancesOf("Win32_USBHub"):  # buradan sonrası da yukarının aynısının "usb" için olan hali.
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
            if not str(usb.Name) ==  "USB Kök Hub (USB 3.0)":
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
                                com_port_scanning.F_Json_Regulator(t,mounter-1,"data.json")
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





