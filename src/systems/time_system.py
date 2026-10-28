from pathlib import Path
import helpers
import config
systems = Path(__file__).parent
project = systems.parent.parent
save = helpers.read_file(config.SAVE_PATH)


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
day=save["time"]["day"]
hour=save["time"]["hour"]
current_period=save["time"]["period"]
hour=+1
if hour>24:
    hour=1
    day=+1
if  hour<6  or hour==24:
    period="night"
elif hour<12:
    period="morning"
elif hour<18:
    period="noon"
elif hour<24:
    period="evening"

save["player"]["health"]["current"]=-save["player"]["health"]["loss"]
save["player"]["oxygen"]["current"]=-save["player"]["oxygen"]["loss"]
save["player"]["satiety"]["current"]=-save["player"]["satiety"]["loss"]
save["player"]["water"]["current"]=-save["player"]["water"]["loss"]
save["player"]["morale"]["current"]=-save["player"]["morale"]["loss"]
save["player"]["energy"]["current"]=-save["player"]["energy"]["loss"]

#farming update will be added
#oxygen_system()
"""