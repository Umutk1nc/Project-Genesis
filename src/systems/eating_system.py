import os
import json
from pathlib import Path
from tabulate import tabulate

systems = Path(__file__).parent
project = systems.parent.parent
DATA_DIR = project / "data" / "processed"
Foods = DATA_DIR / "besinler.json"
foods_have=DATA_DIR / "foods_save.json"

your_foods_array=[]
toklukArray=[]
foodsNameArray=[]
tablo_verisi = []
foodsEnergyArray=[]
foodsMoralArray=[]

with open(Foods, "r", encoding="utf-8") as file:
    foods_all = json.load(file)
    
with open(foods_have, "r", encoding="utf-8") as file:
    your_foods_have = json.load(file)

for key3, result3 in foods_all.items():
    givenEnergy=result3.get("enerji",key3)
    foodsEnergyArray.append(givenEnergy)
    
    
for key4, result4 in foods_all.items():
    foodsMoral=result4.get("moral",key4)
    foodsMoralArray.append(foodsMoral)

    
for key2, result2 in your_foods_have.items():
    sahip_olunan=result2.get("miktar",key2)
    your_foods_array.append(sahip_olunan)
    
    
    
for key, result in foods_all.items():
    # Eğer 'name' anahtarı yoksa (ispanak gibi), anahtarın kendi adını baş harfi büyük yapıp yazdır
    name = result.get("name", key.capitalize())
    foodsNameArray.append(name)

for value, tokluk in foods_all.items():
    tokluk_deger = tokluk.get("tokluk", value.capitalize())
    toklukArray.append(tokluk_deger)


        
for index in range(1,len(foodsNameArray)+1):
    satir = [index, foodsNameArray[index-1], toklukArray[index-1],foodsEnergyArray[index-1],foodsMoralArray[index-1],  your_foods_array[index-1]]
    tablo_verisi.append(satir)

def eating_command():
    while True:
        without_eat_condition=input("1 - Tekrar Dene\n2 - Vazgeç\nKomutun:")
        if without_eat_condition=="1":
            return eating_choose()
        
        elif without_eat_condition=="2":
            return None
        
        else:
            print("Geçerli komut girmelisin")
            continue


def eating_choose():
    basliklar = ["Index", "Besin Adı", "Doyurma Etkisi","Enerji Etkisi","Moral Etkisi", "Sahip Olduğun"]
    print(tabulate(tablo_verisi, headers=basliklar, tablefmt="grid"))
    while True:
        eat=input("\n\n\n\nYemek İstediğin Besini Seç:")
        
        if eat.isdigit():        # Sayı mı?
            eat = int(eat)
            if eat<=len(foodsNameArray) and eat>=1:
                break
            else:
                print(f"Lütfen 1 -",len(foodsNameArray),"aralığında sayı gir! ❌")                          
        else:
            print("Lütfen sayı gir! ❌")

    
    
    for index in range(1,len(foodsNameArray)+1):
        if eat==index:
            if your_foods_array[index-1]>0:
                
                
                with open(foods_have, "r", encoding="utf-8") as file:
                    oyuncu_envanteri = json.load(file)
                
                
                secilen_besin=your_foods_array[index-1]   
                Key_list=list(oyuncu_envanteri.keys())
                Key=Key_list[eat-1]
                oyuncu_envanteri[Key]["miktar"] -= 1
                
                keyName=foodsNameArray[eat-1]
                print("1",keyName,"yedin.")


                with open(foods_have, "w", encoding="utf-8") as file:
                    json.dump(oyuncu_envanteri, file, indent=4, ensure_ascii=False)
                pass
            else:
                print("Bu Besine Sahip Olmadığın İçin Yiyemezsin❌")
                eating_com=eating_command()
                if eating_com is None:
                    return None
                    
                    
                  
    return eat