import random
from eylem_sistemi import *
hour=1
day=24*hour
week=day*7
month=day*30


# Çekilecek Veriler
mevcut_tarih=26
sure=random.randint(1,1000)#gecici olarak sure bu şekilde sonrasında diğer eventlere göre veri gelecek sureye.


def gecen_sure_mesaji(sure):
    month_condition,month_remain=divmod(sure,month)
    week_condition,week_remain=divmod(month_remain,week)
    day_condition,hour_remain=divmod(week_remain,day)
    print(f"",sure,"\n")
    print("-----Geçen Zaman-----\n")
    print("Geçen Ay:",month_condition,"\nGeçen Hafta:",week_condition,
        "\nGeçen Gün:",day_condition,"\nGeçen Saat:",hour_remain)
gecen_sure_mesaji(sure)


#Eylem Durumu Core Tick
while True:
    if event_is_continue==True:
        mevcut_tarih=mevcut_tarih+1
        continue
    else:
        break
if (mevcut_tarih%24)<6 or (mevcut_tarih%24)>=18:
    day_condition="Gece"
else:
    day_condition="Gündüz" 

print(day_condition)
print(su)