class TimeManager:
    def __init__(self):
        pass

    
    def time_loop(self,save_file):
        time=save_file["time_system"]["time"]
        if time%24<6:
            save_file["time_system"]["day_loop"]="Night"
        elif time%24<12:
            save_file["time_system"]["day_loop"]="Morning"
        elif time%24<18:
            save_file["time_system"]["day_loop"]="Afternoon"
        else:
            save_file["time_system"]["day_loop"]="Evening"
            
            
        
    def pass_hour(self,save_file):
        save_file["time_system"]["time"]+=1
        self.time_loop(save_file)