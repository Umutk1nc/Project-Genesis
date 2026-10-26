from pathlib import Path
import json
systems = Path(__file__).parent
project = systems.parent.parent
SAVE_PATH = project / "saves" / "save_system.json"


class TimeManager:
    def time_loop(self,save_file):
        time=save_file["time_system"]["time"]
        if time%24<6:
            save_file["time_system"]["day_loop"]="Night"
        elif time%24<12:
            save_file["time_system"]["day_loop"]="Morning"
        elif time%24<18:
            save_file["time_system"]["day_loop"]="Noon"
        elif time%24<24:
            save_file["time_system"]["day_loop"]="Tonight"
            
            
        
    def pass_hour(self,save_file):
        save_file["time_system"]["time"]+=1
        self.time_loop(save_file)
    
        


"""
with open(SAVE_PATH, "r", encoding="utf-8") as file:
    save = json.load(file)

#with open(SAVE_PATH, "w", encoding="utf-8") as file:
#    json.dump(time_save,file, indent=4, ensure_ascii=False)
gun=save["zaman"]["gun"]
saat=save["zaman"]["saat"]
mevcut_periyot=save["zaman"]["periyot"]
saat=+1
if saat>24:
    saat=1
    gun=+1
if  saat<6  or saat==24:
    periyot="gece"
elif saat<12:
    periyot="sabah"
elif saat<18:
    periyot="ögle"
elif saat<24:
    periyot="aksam"

save["oyuncu"]["saglik"]["mevcut"]=-save["oyuncu"]["saglik"]["kayip"]
save["oyuncu"]["oksijen"]["mevcut"]=-save["oyuncu"]["oksijen"]["kayip"]
save["oyuncu"]["tokluk"]["mevcut"]=-save["oyuncu"]["tokluk"]["kayip"]
save["oyuncu"]["su"]["mevcut"]=-save["oyuncu"]["su"]["kayip"]
save["oyuncu"]["moral"]["mevcut"]=-save["oyuncu"]["moral"]["kayip"]
save["oyuncu"]["enerji"]["mevcut"]=-save["oyuncu"]["enerji"]["kayip"]

#tarim güncellemesi olacak
#oksijen_sistemi()
"""