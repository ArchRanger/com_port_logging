import usb

from usb.core import NoBackendError,USBError

byte_char_mapper = [
    ["","","","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9","","","",""," "],[],["","","","","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","","","","","","","","","","","","",""]
                   ]
def byte_char_map(x,y):
    try:
        return byte_char_mapper[x][y]
    except IndexError:
        return ""
    except:
        return ""

def read_scan(queue, vid, pid):
    # Cihaz bağlantı kontrol döngüsü
    while True:
        try:
            # Scannera girenlere karşılık cihaz yöneticisinden cihaza ait VID ve PID alma kısmı
            # vid örneği: 2046
            # pid örneği: 21C1
            dev = usb.core.find(idVendor=int("0x" + vid, 16),
                                idProduct=int("0x" + pid, 16))
            # Cihazı varsayılan konfigürasyona buradan alıyoruz
            dev.set_configuration()
            # Konfigürasyonu objeden alma kodu
            conf = dev.get_active_configuration()
            # Konfigürasyonun detaylarını değişken olarak ayırma kodu
            cfg = conf[0, 0]
            ep = cfg[0]
            r = []

            # Barkodu okuma döngüsü
            while True:
                # Çıktıyı tutacak değişken
                code = ""
                try:
                    # Scannerı okuyup byte'ları array olarak tutma kodu
                    data = dev.read(ep.bEndpointAddress,ep.wMaxPacketSize)
                    # Verileri listeye ekliyoruz
                    r.append([data[0], data[2]])
                    # Eğer byte array'i byte yayınından TAB'i kabul ederse
                    if data[2] == 43:
                        # Karakter ayrıştırmasını başlatır;
                        for x in r:
                            code += str(byte_char_map(x[0], x[1]))
                            # Karakteri sürecin sırasına alır,
                            queue.put(code)
                            r = []
                # Tarama yapılmadığında verilen hata kodu
                except USBError as e:
                    val = str(e).split("[")[2].split("]")[0]
                    if val in ["claim_interface", "submit_async"]:
                        break
                    else:
                        queue.put("")
        # Scannera bir cihaz bağlı olmadığı, veya tespit edilemediği durumdaki hata kodu,
        except NoBackendError:
            # Backend yoksa
            queue.put(None)
        except AttributeError:
            # Scanner yoksa
            queue.put(None)

# Bu fonksiyon lag olmadığında herhangi arızalı bir durumda çalışacak
def get_scan(queue):
    # Süreçteki sırada bulunan değeri alır
    while True:
        data = queue.get()
        if data != "":
            # Sadece data değeri bulabilirse yazdıracak
            print(data)
        else:
            print("Scanner not connected.")



while True:
    read_scan()







