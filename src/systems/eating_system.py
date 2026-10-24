import config
import helpers 
class Data_Reader:
    def Read_Keys(self,FILE,string):
        ARRAY=[]
        for key, result in FILE.items():
            set_value=result.get(string,key)
            ARRAY.append(set_value)
        return ARRAY     
        
class Eating_System:
    def __init__(self,commands,general):
        self.commands = commands
        self.general = general
        
    
    def Create_Table_Data(self,FOODS_FILE,SAVE_FILE):
        table_data=[]
        food_keys=[]
        index=0#ister 0 ister 1'den başlasın
        for key,result in FOODS_FILE.items():
            row=[index,result["name"],result["tokluk"],result["enerji"],result["moral"],result["su"],SAVE_FILE["foods"][key]["miktar"],result["buyume_gunu"]]
            food_keys.append(key)
            table_data.append(row)
            index+=1
        return table_data,food_keys
    def Choose_Food(self,minimum,maximum):#tablo gösterme kısmının sonra yaparsın.
        string="Yemek istediğin besinin index numarasını gir:"
        valid_index=self.commands.Choose(minimum,maximum,string)
        
        return valid_index
    
    def Check_Food(self,food_index, food_keys,SAVE_FILE):
        key_choice=food_keys[food_index]
        food_key=SAVE_FILE["foods"][key_choice]
        value=food_key["miktar"]
        if value>=1:#later maybe it can be multi eating
            return key_choice
        else:
            return None
        
        

    def Eat(self,Key,SAVE_FILE,FOODS_FILE):
        if Key is None:
            print("Bu besine sahip olmadığın için yiyemezsin.")
            return False
                
        else:
            #update food
            SAVE_FILE["foods"][Key]["miktar"]-=1      
            #find food values
            satiety=FOODS_FILE[Key]["tokluk"]
            energy=FOODS_FILE[Key]["enerji"]
            moral=FOODS_FILE[Key]["moral"]
            water=FOODS_FILE[Key]["su"]
            #update character values
            #TO DO
            SAVE_FILE["player_condition"]["tokluk"]+=satiety
            SAVE_FILE["player_condition"]["tokluk"]=self.general.Limit_Value(SAVE_FILE["player_condition"]["tokluk"],0,100)
            SAVE_FILE["player_condition"]["enerji"]+=energy
            SAVE_FILE["player_condition"]["enerji"]=self.general.Limit_Value(SAVE_FILE["player_condition"]["enerji"],0,100)
            SAVE_FILE["player_condition"]["moral"]+=moral
            SAVE_FILE["player_condition"]["moral"]=self.general.Limit_Value(SAVE_FILE["player_condition"]["moral"],0,100)
            SAVE_FILE["player_condition"]["su"]+=water    
            SAVE_FILE["player_condition"]["su"]=self.general.Limit_Value(SAVE_FILE["player_condition"]["su"],0,100)
            return True

class EatingController:
    def __init__(self):
        self.save_manager = helpers.SaveManager()
        self.commands = helpers.Commands()
        self.table = helpers.Table()
        self.general = helpers.General()
        self.eating_system = Eating_System(self.commands,self.general)
        
        
    def Run(self):
        #Read File
        FOODS_FILE=self.save_manager.ReadFile(config.FOODS_PATH)
        SAVE_FILE=self.save_manager.ReadFile(config.SAVE_PATH)
        #EatingController LOOP
        while True:
            #Make Table
            Table_Data,food_keys=self.eating_system.Create_Table_Data(FOODS_FILE,SAVE_FILE)
            #Show Table
            title=["Index", "Besin Adı", "Doyurma Etkisi","Enerji Etkisi","Moral Etkisi", "Su Etkisi","Miktar","Büyüme Süresi"]
            self.table.Show_Table(Table_Data,title)
            #Find First and Last index for decision
            last_index = len(food_keys) - 1
            first_index=Table_Data[0][0]
            #Choose the food That you want
            valid_index=self.eating_system.Choose_Food(first_index,last_index)
            #Control the food and take the key of food
            Key=self.eating_system.Check_Food(valid_index,food_keys,SAVE_FILE)
            #Control whether you eat the food
            is_eat=self.eating_system.Eat(Key,SAVE_FILE,FOODS_FILE)
            if is_eat==True:
                    self.save_manager.SaveFile(config.SAVE_PATH,SAVE_FILE)
                    print(FOODS_FILE[Key]["name"]," adlı besin başarıyla yendi")
                    result_command=self.commands.Choose(0,1,"0 - Başka besin Ye\n1 - Ana Menüye Dön\n")
                    if result_command==0:
                        continue
                    else:
                        break
            else:
                returning="0 - Farklı besin ye\n1 - Ana Menüye Dön\n"
                result=self.commands.Choose(0,1,returning)
                if result==0:
                    continue
                else:
                    break    
#Tablo gösterirken sadece Sahip olunanlar gösterilebilir.
game = EatingController()
game.Run()