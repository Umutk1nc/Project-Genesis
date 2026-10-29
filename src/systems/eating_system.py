import config
import helpers 
        
class EatingSystem:
    def __init__(self,commands,general):
        self.commands = commands
        self.general = general
        
    
    def create_table_data(self,foods_file,save_file):
        table_data=[]
        food_keys=[]
        index=0#start from 0 or 1
        for key,result in foods_file.items():
            row=[index,result["name"],result["satiety"],result["energy"],result["morale"],result["water"],save_file["foods"][key]["amount"],result["growth_day"]]
            food_keys.append(key)
            table_data.append(row)
            index+=1
        return table_data,food_keys
    def choose_food(self,minimum,maximum):#you will do the table display part later.
        string="Enter the index number of the food you want to eat:"
        valid_index=self.commands.choose(minimum,maximum,string)
        
        return valid_index
    
    def check_food(self,food_index, food_keys,save_file):
        key_choice=food_keys[food_index]
        food_key=save_file["foods"][key_choice]
        value=food_key["amount"]
        if value>=1:#later maybe it can be multi eating
            return key_choice
        else:
            return None
        
        

    def eat(self,key,save_file,foods_file):
        if key is None:
            print("You cannot eat this food because you do not have it.")
            return False
                
        else:
            #update food
            save_file["foods"][key]["amount"]-=1      
            #find food values
            satiety=foods_file[key]["satiety"]
            energy=foods_file[key]["energy"]
            morale=foods_file[key]["morale"]
            water=foods_file[key]["water"]
            #update character values
            #TO DO
            save_file["player_condition"]["satiety"]+=satiety
            save_file["player_condition"]["satiety"]=self.general.limit_value(save_file["player_condition"]["satiety"],0,100)
            save_file["player_condition"]["energy"]+=energy
            save_file["player_condition"]["energy"]=self.general.limit_value(save_file["player_condition"]["energy"],0,100)
            save_file["player_condition"]["morale"]+=morale
            save_file["player_condition"]["morale"]=self.general.limit_value(save_file["player_condition"]["morale"],0,100)
            save_file["player_condition"]["water"]+=water    
            save_file["player_condition"]["water"]=self.general.limit_value(save_file["player_condition"]["water"],0,100)
            return True

class EatingController:
    def __init__(self):
        self.save_manager = helpers.SaveManager()
        self.commands = helpers.Commands()
        self.table = helpers.Table()
        self.general = helpers.General()
        self.eating_system = EatingSystem(self.commands,self.general)
        
        
    def run(self):
        #Read File
        foods_file=self.save_manager.read_file(config.FOODS_PATH)
        save_file=self.save_manager.read_file(config.SAVE_PATH)
        #EatingController LOOP
        while True:
            #Make Table
            table_data,food_keys=self.eating_system.create_table_data(foods_file,save_file)
            #Show Table
            title=["Index", "Food Name", "Satiety Effect","Energy Effect","Morale Effect", "Water Effect","Amount","Growth Time"]
            self.table.show_table(table_data,title)
            #Find First and Last index for decision
            last_index = len(food_keys) - 1
            first_index=table_data[0][0]
            #Choose the food That you want
            valid_index=self.eating_system.choose_food(first_index,last_index)
            #Control the food and take the key of food
            key=self.eating_system.check_food(valid_index,food_keys,save_file)
            #Control whether you eat the food
            is_eat=self.eating_system.eat(key,save_file,foods_file)
            if is_eat==True:
                    self.save_manager.save_file(config.SAVE_PATH,save_file)
                    print(foods_file[key]["name"]," was eaten successfully")
                    result_command=self.commands.choose(0,1,"0 - Eat Another Food\n1 - Main Menu\n")
                    if result_command==0:
                        continue
                    else:
                        break
            else:
                returning="0 - Eat Another Food\n1 - Main Menu\n"
                result=self.commands.choose(0,1,returning)
                if result==0:
                    continue
                else:
                    break    
#When showing the table, only owned items can be displayed.
if __name__=="__main__":
    game = EatingController()
    game.run()