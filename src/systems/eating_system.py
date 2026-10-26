import config
import helpers 
class DataReader:
    def read_keys(self,file,string):
        array=[]
        for key, result in file.items():
            set_value=result.get(string,key)
            array.append(set_value)
        return array     
        
class EatingSystem:
    def __init__(self,commands,general):
        self.commands = commands
        self.general = general
        
    
    def create_table_data(self,foods_file,save_file):
        table_data=[]
        food_keys=[]
        index=0#ister 0 ister 1'den başlasın
        for key,result in foods_file.items():
            row=[index,result["name"],result["tokluk"],result["enerji"],result["moral"],result["su"],save_file["foods"][key]["miktar"],result["buyume_gunu"]]
            food_keys.append(key)
            table_data.append(row)
            index+=1
        return table_data,food_keys
    def choose_food(self,minimum,maximum):#tablo gösterme kısmının sonra yaparsın.
        string="Yemek istediğin besinin index numarasını gir:"
        valid_index=self.commands.choose(minimum,maximum,string)
        
        return valid_index
    
    def check_food(self,food_index, food_keys,save_file):
        key_choice=food_keys[food_index]
        food_key=save_file["foods"][key_choice]
        value=food_key["miktar"]
        if value>=1:#later maybe it can be multi eating
            return key_choice
        else:
            return None
        
        

    def eat(self,key,save_file,foods_file):
        if key is None:
            print("Bu besine sahip olmadığın için yiyemezsin.")
            return False
                
        else:
            #update food
            save_file["foods"][key]["miktar"]-=1      
            #find food values
            satiety=foods_file[key]["tokluk"]
            energy=foods_file[key]["enerji"]
            moral=foods_file[key]["moral"]
            water=foods_file[key]["su"]
            #update character values
            #TO DO
            save_file["player_condition"]["tokluk"]+=satiety
            save_file["player_condition"]["tokluk"]=self.general.limit_value(save_file["player_condition"]["tokluk"],0,100)
            save_file["player_condition"]["enerji"]+=energy
            save_file["player_condition"]["enerji"]=self.general.limit_value(save_file["player_condition"]["enerji"],0,100)
            save_file["player_condition"]["moral"]+=moral
            save_file["player_condition"]["moral"]=self.general.limit_value(save_file["player_condition"]["moral"],0,100)
            save_file["player_condition"]["su"]+=water    
            save_file["player_condition"]["su"]=self.general.limit_value(save_file["player_condition"]["su"],0,100)
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
            title=["Index", "Besin Adı", "Doyurma Etkisi","Enerji Etkisi","Moral Etkisi", "Su Etkisi","Miktar","Büyüme Süresi"]
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
                    print(foods_file[key]["name"]," adlı besin başarıyla yendi")
                    result_command=self.commands.choose(0,1,"0 - Başka besin Ye\n1 - Ana Menüye Dön\n")
                    if result_command==0:
                        continue
                    else:
                        break
            else:
                returning="0 - Farklı besin ye\n1 - Ana Menüye Dön\n"
                result=self.commands.choose(0,1,returning)
                if result==0:
                    continue
                else:
                    break    
#Tablo gösterirken sadece Sahip olunanlar gösterilebilir.
game = EatingController()
game.run()