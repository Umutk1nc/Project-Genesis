import os
import json
from pathlib import Path

systems = Path(__file__).parent
project = systems.parent.parent
DATA_DIR = project / "data" / "processed"
EVENT_PATH = DATA_DIR / "events.json"
saves=project/"saves"
SAVE_PATH = saves / "Auto_save.json"



with open(EVENT_PATH, "r", encoding="utf-8") as file:
    events = json.load(file)
with open(SAVE_PATH, "r", encoding="utf-8") as file:
    SAVES = json.load(file)


#1. Anlık Event
event_is_continue=False
if event_is_continue==False:
    pass





#2. Süreli Event (ÇOK ÖNEMLİ)
acikma_durumu=events["aclik"]["aclik_etkisi"]
su_kaybi=events["susuzluk"]["susuzluk_etkisi"]
enerji_kaybi=events["enerji"]["enerji_etkisi"]


zaman_degisimi=SAVES["zaman"]["anlik"]
su=SAVES["susuzluk"]["kalan"]
aclik=SAVES["aclik"]["kalan"]
enerji=SAVES["enerji"]["kalan"]




while zaman_degisimi!=0:
    su=su-su_kaybi
    aclik=aclik-acikma_durumu
    enerji=enerji-enerji_kaybi
    zaman_degisimi=zaman_degisimi-1
    print(f"\t",zaman_degisimi,"\t",aclik,"\t",su,"\t",enerji)
    continue
        
        
        
        
        

#3. Kritik Event