import os
import json
from pathlib import Path
from tabulate import tabulate
import math
import numpy as np
#import time_system
systems = Path(__file__).parent
project = systems.parent.parent
Game=project.parent
SRC=Game/"src"
SAVE_DIR=project/"saves"
DATA_DIR = project/ "data" / "processed"
foods = DATA_DIR / "besinler.json"
save=SAVE_DIR/"save_system_ex.json"

with open(foods, "r", encoding="utf-8") as file:
    foods_file = json.load(file)
with open(save, "r", encoding="utf-8") as file:
    save_file = json.load(file)
    
alan_sayisi=save_file["tarim"]["alan_sayisi"]

def alan_olustur():
    pass

def tarla_goruntule():   
    for i in range(alan_sayisi):
        print(f"---------------------------------ALAN ID:",i,"---------------------------------")
        print("-----------------------------------------------------------------------------")
        ekilen_bitkiler=save_file["tarim"]["alanlar"][i]["ekilen_bitkiler"]
        ekilme_sayisi=save_file["tarim"]["alanlar"][i]["ekilme_sayisi"]
        ekilme_saati=save_file["tarim"]["alanlar"][i]["ekilme_saati"]
        bitki_durumu=save_file["tarim"]["alanlar"][i]["bitki_durumu"]
        tarla_sicaklik=save_file["tarim"]["alanlar"][i]["tarla_sicaklik"]
        su_seviyesi=save_file["tarim"]["alanlar"][i]["su_seviyesi"]
        tarla_verimi=save_file["tarim"]["alanlar"][i]["tarla_verimi"]
        bos_alan=save_file["tarim"]["alanlar"][i]["bos_alan"]
        
        bitki_sayisi=len(ekilen_bitkiler)
        
        for i in range(bitki_sayisi):
            print("Ad:",ekilen_bitkiler[i],"\tSayı:",ekilme_sayisi[i],"\tSaat:",ekilme_saati[i],"\tYüzde:",bitki_durumu[i])
            if i==bitki_sayisi-1:
                print("*****************************************************************************")
                print("--------------------------------TARLA DURUMU--------------------------------")
                print("*****************************************************************************")
                print("Sıcaklık:",tarla_sicaklik,"\tSu Seviyesi:",su_seviyesi,"\tVerim:",tarla_verimi,"\tBoş Alan:",bos_alan)
                print("=============================================================================\n")

def tarla_ek_secimi():
    print("--------------------------Alanlar--------------------------")
    print("-----------------------------------------------------------")
    array=[]
    for i in range(alan_sayisi):
        bos_alan=save_file["tarim"]["alanlar"][i]["bos_alan"]
        su_seviyesi=save_file["tarim"]["alanlar"][i]["su_seviyesi"]
        tarla_verimi=save_file["tarim"]["alanlar"][i]["tarla_verimi"]
        if bos_alan>0:
            array.append(i)
            print("ALAN ID:",i,"\tSu Seviyesi",su_seviyesi,"\tVerim:",tarla_verimi,"\tBoşluk",bos_alan)  
             
    if not array:
        alan_olustur_secenek=input("Hiç boş alan bulunmuyor.\n1 - Yeni alan oluştur\n2 Çık")
        if alan_olustur_secenek=="1":
            alan_olustur()
        else: 
            pass
    
    
    def alan_kontrol():
            ekilecek_alan_secimi=input("\nHangi Alana Ekmek İstiyorsun:")
            ekilecek_alan_secimi=digit_validation(ekilecek_alan_secimi)
            if ekilecek_alan_secimi in array:
                return ekilecek_alan_secimi
            else:
                print("Geçersiz Komut") 
                return None
    
    while(True):
        ekilecek_alan_secimi=alan_kontrol()
        if ekilecek_alan_secimi is None:
            continue
        else:
            break
    return ekilecek_alan_secimi

def ekilme_islemi(ekilecek_alan_secimi):
    #sahip olunan besinleri ve gereken özellikler itablo biçiminde ekrana getir ve buradan sahip olduğumuz boş alan kadar ekmeye devam et
    counter=0
    raw_data=[]
    for besin, ozellikler in foods_file.items():
        buyume_gunu=ozellikler["buyume_gunu"]
        su_ihtiyaci=ozellikler["su_ihtiyaci"]
        isik_ihtiyaci=ozellikler["isik_ihtiyaci"]
        isim=ozellikler["name"]
        miktar=save_file["foods"][besin]["miktar"]
        counter=counter+1
        raw_data.append([counter,isim,buyume_gunu,su_ihtiyaci,isik_ihtiyaci,miktar])

    sutun_isimleri = ["ID", "Bitki Adı", "Büyüme Süresi","Su İhtiyacı","Işık İhtiyacı" ,"Sahip Olunan"]
                
    new_counter=0
    zero_counter=0
    raw_data=[]
    gecici_array=[]
    condition="1"
    for besin, ozellikler in foods_file.items():
        buyume_gunu=ozellikler["buyume_gunu"]
        su_ihtiyaci=ozellikler["su_ihtiyaci"]
        isik_ihtiyaci=ozellikler["isik_ihtiyaci"]
        isim=ozellikler["name"]
        miktar=save_file["foods"][besin]["miktar"]      
        if miktar==0:
            zero_counter=zero_counter+1
            if zero_counter==counter and new_counter==0:
                print("Ekebileceğin hiçbir bitkiye sahip değilsin.\n")
                break 
            continue   
        else:
            condition="0"
            new_counter=new_counter+1
            gecici_array.append(besin)
        raw_data.append([new_counter,isim,buyume_gunu,su_ihtiyaci,isik_ihtiyaci,miktar])
        
    if condition=="0":
        sutun_isimleri = ["Index", "Bitki Adı", "Büyüme Süresi","Su İhtiyacı","Işık İhtiyacı" ,"Sahip Olunan"]  
        print(tabulate(raw_data, headers=sutun_isimleri, tablefmt="fancy_grid"))
    
    def control_large(besin_secim_parametre):
        while True:
            if besin_secim_parametre>new_counter or besin_secim_parametre<0:
                besin_secim_parametre=input("Ekeceğin besinin numarasını yaz:")
                besin_secim_parametre=digit_validation(besin_secim_parametre)
            else:
                return besin_secim_parametre
    
    ekilecek_besin_secimi=input("Ekeceğin besinin numarasını yaz:")
    ekilecek_besin_secimi=digit_validation(ekilecek_besin_secimi)
    ekilecek_besin_secimi=control_large(ekilecek_besin_secimi)
    
    
    ekilecek_besin=gecici_array[ekilecek_besin_secimi-1]
    
            
        
    print("Ekme işlemi başlatılıyor...")
    
    ekilen_besin_ismi=foods_file[ekilecek_besin]["name"]
    ekilen_besin_sahip_olunan=save_file["foods"][ekilecek_besin]["miktar"]
    bos_alan_durumu=save_file["tarim"]["alanlar"][ekilecek_alan_secimi]["bos_alan"]
    
    
    data=[[ekilen_besin_ismi,ekilen_besin_sahip_olunan,bos_alan_durumu,ekilecek_alan_secimi]]
    sutun=["İsim","Sahip olduğun","Boş Alan","Alan ID"]
    print(tabulate(data, headers=sutun, tablefmt="fancy_grid"))
    ekme_islem_sureci(data)
            
def ekme_islem_sureci(data):
    if data[0][1]<data[0][2]:
        print(f"En fazla {data[0][1]} adet ekebilirsin.")
        max_ekilen=data[0][1]
    else:
        print(f"En fazla {data[0][2]} adet ekebilirsin.")
        max_ekilen=data[0][2]
    miktar=input(f"Ne kadar ekmek istersin:\nVazgeç - 0=>\nHepsini Ek - {max_ekilen}<=")

    miktar=digit_validation(miktar)          
    if miktar<=0:
        tarla_ek_secimi()
    elif miktar>0 and miktar<max_ekilen:
        ekilecek_miktar=miktar
    else:
        ekilecek_miktar=max_ekilen
    print()          
    print (f"{ekilecek_miktar} adet {data[0][0]} ekiliyor")    
    #time_system()
       

def digit_validation(variable):
    while True:
        if str(variable).isdigit():
            return int(variable)   
        else:
            variable=input("Geçersiz Giriş, Tekrar Dene:")      
            
               
def valid_integer_validation(variable,array_ID):
    variable=digit_validation(variable)
    while True:
        if variable in array_ID:
            return variable
        else:
            variable=input("Geçersiz Giriş, Tekrar Dene:") 
            variable=digit_validation(variable)
            

    


def tarla_sula():
    alan_ID=[]
    su_seviyesi=[]
    su_ihtiyaci=[]
    su_satir=[]
    urun_sayisi=[]
         
    for i in range(save_file["tarim"]["alan_sayisi"]):
        ekilen_bitki_array=save_file["tarim"]["alanlar"][i]["ekilen_bitkiler"]
        ekilen_bitki_array_uzunluk=len(ekilen_bitki_array)
        total_su=0

        
        for j in range (ekilen_bitki_array_uzunluk):
            identication_besin=ekilen_bitki_array[j] 
            
            if foods_file[identication_besin]["su_ihtiyaci"]=="cok_yuksek":
               susuzluk_katsayisi=5 
                
            elif foods_file[identication_besin]["su_ihtiyaci"]=="yuksek":
                susuzluk_katsayisi=4
                
            elif foods_file[identication_besin]["su_ihtiyaci"]=="orta":
                susuzluk_katsayisi=3
            elif foods_file[identication_besin]["su_ihtiyaci"]=="dusuk":
                susuzluk_katsayisi=2
            elif foods_file[identication_besin]["su_ihtiyaci"]=="cok_dusuk":
                susuzluk_katsayisi=1
            
    
            total_su+=save_file["tarim"]["alanlar"][i]["ekilme_sayisi"][j]*susuzluk_katsayisi
            
            
        alan_ID.append(i)    
        su_ihtiyaci.append(total_su)
        su_seviyesi.append(save_file["tarim"]["alanlar"][i]["su_seviyesi"])
        urun_sayisi.append(sum(save_file["tarim"]["alanlar"][i]["ekilme_sayisi"]))
        su_satir.append([alan_ID[i],su_seviyesi[i],su_ihtiyaci[i]/10,urun_sayisi[i]])
        
        
        
      
    su_sutun=["Alan ID","Nem","Saatlik Su İhtiyacı","Ürün Sayısı"]
    print(tabulate(su_satir, headers=su_sutun, tablefmt="fancy_grid"))
    
    while True:
        sulama_alani=input("Sulamak istediğin alanın ID'sini gir:")
        sulama_alani=digit_validation(sulama_alani)
        condition=0    
        for i in range(0,len(alan_ID)):
            if sulama_alani==alan_ID[i]:
                condition=1
                break
        if condition==1:
            break
    
    
    
    #burada bir tablo ver sulamanın azalttığı su miktarı ve neme etkisi 
    save_file["tarim"]["alanlar"][alan_ID[sulama_alani]]["su_seviyesi"]
    
    sulama_satir=[[alan_ID[sulama_alani],su_seviyesi[sulama_alani],su_ihtiyaci[sulama_alani],urun_sayisi[sulama_alani]]]
    sulama_sutun=["Sulanan Alan","Nem","Sulama Maliyeti","Ürün Sayısı"]
    print(tabulate(sulama_satir, headers=sulama_sutun, tablefmt="fancy_grid"))
    
    sulanan_tarla_guncelle(sulama_alani,su_seviyesi,su_ihtiyaci,urun_sayisi)
    #tarla_boyut*su_katsayısı_ortalaması/10
    #katsayı_toplamı/tarla_boyut
    #bitki_sagligi-2*susuzluk_katsayisi*saat
         

def sulanan_tarla_guncelle(sulama_alani,su_seviyesi,su_ihtiyaci,urun_sayisi):
    pass


def hasat_edilecek_goruntule():
    sutun=["Alan ID","Bitki Adı","Hasat Edilebilen Bitki Sayısı"]
    satir=[]
    hasat_edilecek_array=[]
    for alan_index in range(alan_sayisi):
        bitki_durumu=save_file["tarim"]["alanlar"][alan_index]["bitki_durumu"]
        for j in range(len(bitki_durumu)):
            if bitki_durumu[j]==100:
                bitki_ID=save_file["tarim"]["alanlar"][alan_index]["ekilen_bitkiler"][j]
                bitki_ismi=foods_file[bitki_ID]["name"]
                ekili_urun=save_file["tarim"]["alanlar"][alan_index]["ekilme_sayisi"][j]
                satir.append([alan_index,bitki_ismi,ekili_urun])
                hasat_edilecek_array.append(alan_index)
    if not satir:
        print("Hasat edilebilecek hiçbir ürün yoktur.")
        print("Çıkış Yapılıyor...")
        #time.sleep(2)
        return commands()
    else:
        table(satir,sutun)
    hasat_et(hasat_edilecek_array,satir,sutun)     
     
def hasat_et(hasat_edilecek_array,satir,sutun):
    hasat_edilecek_ID=input("Hasat etmek istediğin alanın ID'sini yaz:")
    valid_ID=valid_integer_validation(hasat_edilecek_ID,hasat_edilecek_array)    
    alandaki_yetisen_bitki_cesidi=hasat_edilecek_array.count(valid_ID)
    new_satir=[]
    counter=0
    energy_constant=10 
    sutun[0]="Grup ID"
    for i in range(len(satir)):
            if satir[i][0]==valid_ID:
                satir[i][0]=counter
                counter+=1
                new_satir.append(satir[i])
    table(new_satir,sutun)
    hasat_secim=input(f"[0 , {counter-1}] - Belirli bir grubu hasat et.\nTüm tarlayı hasat etmek için aralık dışı sayı gir.\nSeçim:")        
    hasat_secim=digit_validation(hasat_secim)
    
    
    #If all fields in the not range and all fields,if not in the range the number of the field until contain value
    if hasat_secim in new_satir [0]:
        #A value
        print(new_satir[hasat_secim][2])
        sum_of_harvest=new_satir[hasat_secim][2]
        harvest_name=new_satir[hasat_secim][1]
        print("Harvest name",harvest_name)
          
    else:
        harvest_array=[]
        #All value
        sum_of_harvest=0
        len_list=len(new_satir[0])
        for t in range(len_list-1):
           sum_of_harvest+=new_satir[t][2]
           harvest_array.append(new_satir[t][1])
        print("Harvest name array",harvest_array)
        print(sum_of_harvest)  
    #just hand after that thiss must be another equipments
    #time will pass until complete the harvest
    power_of_hand=1
    constant_harvest=20   
    available_energy=save_file["player_condition"]["enerji"]
    harvest=0

    with open(save, "r", encoding="utf-8") as file:
        save_harvest = json.load(file)
    available_energy=save_file["player_condition"]["enerji"]
    while sum_of_harvest>0 and available_energy>=energy_constant:
        capacity_of_harvest=np.fix((available_energy*power_of_hand*constant_harvest)/100)
        #time_system()
        #time_system give condition if condition true ask continue or stop
        #condition is false continue until the field completed to harves
        condition_event=False
        if condition_event==True:
            continue_or_quit=input("1 - Devam Et\n2 - Çık")
            #after this fix a litle system
            if continue_or_quit=="1":
                
                continue
            else:
                pass
        else:
            if sum_of_harvest>=capacity_of_harvest:   
                sum_of_harvest-=capacity_of_harvest
                available_energy-=energy_constant#may  change
                harvest=capacity_of_harvest
                 #update files
                save_file["tarim"]["alanlar"][valid_ID]["ekilen_bitkiler"]
                
                with open(save, "w", encoding="utf-8") as file:
                    json.dump(save_file, file, indent=4, ensure_ascii=False)
                
                
 
            
            else:
                available_energy-=np.ceil((sum_of_harvest/capacity_of_harvest)*energy_constant)#you may make fix 
                harvest=sum_of_harvest
                sum_of_harvest=0
            print("total:",harvest)
            print("energy:",available_energy)
        """with open(save, "w", encoding="utf-8") as file:
         #Hafızadaki veriyi JSON formatına çevirip dosyaya basıyoruz
            json.dump(save_harvest, file, indent=4, ensure_ascii=False)"""            
                
    

                
            #update energy, field, foods

            
                  
        
    
    
    
    
    
            
    #Hasat edilirken sayısına göre o kadar süre geçecek
    #Hasat edilince envantere eklenecek
    #Tarla yok olmayacak verimi hasat edildikten sonra sabit kalacak




   
def table(satir,sutun):
    print(tabulate(satir, headers=sutun, tablefmt="fancy_grid"))

def commands():
    tarla_command=input("1 - Tarla Görüntüle\n2 - Çıkış Yap\n")
    if tarla_command=="1":
        tarla_goruntule()
        tarla_islem_secenek=input("1 - Tarla Ek\n2 - Tarla Sula\n3 - Hasat Et\n4 - Çık\n")
    
        if tarla_islem_secenek=="1":
            ekilecek_alan_secimi=tarla_ek_secimi()    
            ekilme_islemi(ekilecek_alan_secimi) 
        elif tarla_islem_secenek=="2":
            tarla_sula()
        elif tarla_islem_secenek=="3":
            hasat_edilecek_goruntule()
    else:
        pass



commands()