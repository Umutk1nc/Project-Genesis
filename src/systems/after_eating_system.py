import json
import eating_system
from eating_system import*


eat=eating_choose()

#Herhangi bir şey yenilmediğinde None döndü.
#Aksi takdirde yediğimiz besinin numarası döndürülüyor
if eat is None:
    pass
else:
    food_name=foodsNameArray[eat-1]
    foods_by_name = {i["name"]: i for i in foods_all.values()}
    energy=foods_by_name[food_name]["enerji"]
    tokluk=foods_by_name[food_name]["tokluk"]
    moral=foods_by_name[food_name]["moral"]
    su=foods_by_name[food_name]["su"]
    print(eat)#Kontrol Amaçlı
    print(tokluk)#Kontrol Amaçlı
    print(energy)#Kontrol Amaçlı
    print(moral)#Kontrol Amaçlı
    print(su)#Kontrol Amaçlı
    
life_path=DATA_DIR / "life.json"
with open(life_path, "r",encoding="utf-8") as file:
    life=json.load(file)

print("------------")
# Bu kısımda yenilen besinin değerleri ile güncellemeoldu.
# Ayrıca sınır değer 100 korundu. 
def updating_essentials():
    mevcut_tokluk=life["tokluk"]["mevcut"]
    mevcut_su=life["su"]["mevcut"]
    mevcut_enerji=life["enerji"]["mevcut"]
    mevcut_moral=life["moral"]["mevcut"]
    array=[mevcut_tokluk,tokluk,mevcut_su,su,mevcut_enerji,energy,mevcut_moral,moral]
    updating_essentials_array=[]
    for i in range(1,len(array),2):
        updating_essentials_array.append(array[i]+array[i-1])
 
        
    for i in range(0,len(updating_essentials_array)): 
        if updating_essentials_array[i]>100:
            updating_essentials_array[i]=100
    return updating_essentials_array


def data_recording(updating_array):
    #Yediğimiz besinlerle güncellenen verileri jsona ekleyeceğiz.
    
    with open(life_path, "r",encoding="utf-8") as file:
        life=json.load(file)
    life["tokluk"]["mevcut"]=updating_array[0]#tokluk
    life["su"]["mevcut"]=updating_array[1]#su
    life["enerji"]["mevcut"]=updating_array[2]#enerji
    life["moral"]["mevcut"]=updating_array[3]#moral


    with open(life_path, "w", encoding="utf-8") as file:
        json.dump(life, file, indent=4, ensure_ascii=False)
updating_array=updating_essentials()
data_recording(updating_array)