import math

from attrs import field
import config
import helpers
import time_system

class MenuData:
    def __init__(self):
        
        self.field_menu_title="Field"
        self.field_menu_chooses=["Plant","Harvest","Irrigate","Fertilize","Select Another Field","Main Menu"]
   
        

class FieldManager:
    def __init__(self):
        self.table=helpers.Table()
        self.general=helpers.General()        
        
    def view_fields(self,save_file):
        fields=save_file["fields"]
        title=["Index", "Amount","Ready","Water","Fertility", "Temperature"]
        for field_index,field in enumerate(fields):
            crops=field["crops"]
            table_data=[]
            total_ready = sum(crop["ready"] for crop in crops)
            capacity=field["capacity"]
            water=field["water"]
            fertility=field["fertility"]
            temperature=field["temperature"]
            
            #to find total amount
            total_amount = sum(crop["amount"] for crop in crops)
            
            table_data.append([field_index,f"{total_amount}/{capacity}",total_ready,water,fertility,temperature])
            print(f"\n===================== Field {field_index} =====================")
            self.table.show_table(table_data,title)      
    
    def get_field(self,save_file,field_index):
        return save_file["fields"][field_index]   
    
    def get_total(self,crops):
        return sum(crop["amount"] for crop in crops)
                            
    def show_field(self,field,index,foods_file):
        crops=field["crops"]
        field_data=[]
        total_amount=self.get_total(crops)
        total_ready = sum(crop["ready"] for crop in crops)
        print(f"\n=============== Field {index} ===============")
        print(f"Capacity:{total_amount}/{field["capacity"]}")
        print(f"Water:{field["water"]}")
        print(f"Fertility:{field["fertility"]}")
        print(f"Temperature:{field["temperature"]}")
        print(f"Ready:{total_ready}")
        print("───────────────────────────────────────")
        print("                  Crops                  ")
        print("───────────────────────────────────────")
        
        for crop in crops:
            food_key=crop["food"]
            name=self.general.food_finder(food_key,"name",foods_file)
            amount=crop["amount"]
            elapsed_days=crop["elapsed_days"]
            plant_time=crop["plant_time"]
            ready=crop["ready"]
            hp=crop["hp"]
            field_data.append([name,amount,f"{elapsed_days}/{plant_time}",ready,hp])
        title=["Plant","Amount","Growth","Ready","HP"]
        self.table.show_table(field_data,title)

    
    
class PlantManager:
    def __init__(self,field_manager):
        self.table=helpers.Table()
        self.general=helpers.General()
        self.save_manager=helpers.SaveManager()
        self.commands=helpers.Commands()
        self.field_manager=field_manager
    
    def show_crops(self,save_file,foods_file):
        table_data=[]
        food_keys=[]
        index=0  
        foods=save_file["foods"]
        for food_key in foods:
            amount=foods[food_key]["amount"]
            if amount>0: 
                name=self.general.food_finder(food_key,"name",foods_file)
                food_keys.append(food_key)
                table_data.append([index,name,amount])
                index+=1
        #Water and light requirement duration
        #there should be a detailed display menu here; if so, use the detailed plant table from the eating system
        title=["Index","Plant","Amount"]  
        self.table.show_table(table_data,title)
        return food_keys
    
    def find_empty_area(self,field,save_field):
        capacity=save_field["fields"][field]["capacity"]
        crops=save_field["fields"][field]["crops"]
        total_amount=self.field_manager.get_total(crops)
        return capacity-total_amount        
    
    def get_empty_capacity(self,selected_plant,total_area,save_file):
        if save_file["foods"][selected_plant]["amount"]<total_area:
            return save_file["foods"][selected_plant]["amount"]
        else:
            return total_area
    
    def plant_crop(self,amount,field_index,plant_key,save_file,foods_file):
        save_file["foods"][plant_key]["amount"]-=amount
        crops=save_file["fields"][field_index]["crops"]
        growth_time=foods_file[plant_key]["growth_day"]
        new_crop = {
        "food": plant_key,
        "amount": amount,
        "plant_time": growth_time,
        "elapsed_days": 0,
        "ready":0,
        "hp": 100}
        crops.append(new_crop)
        self.save_manager.save_file(config.SAVE_PATH,save_file)

    def has_plant_in_stock(self,save_file):
        return any(food["amount"] > 0 for food in save_file["foods"].values())

    def plant_controller(self,current_field_index,save_file,foods_file):
        if not self.has_plant_in_stock(save_file):
            print("No Seeds Available to Plant.\n")
            return "field_menu"
        
        total_area=self.find_empty_area(current_field_index,save_file)
        if total_area==0:
            print("Maximum planting capacity reached.\n")
            choose=self.commands.choose(0,2,"0 - Plant in Another Field\n1 - Do Another Action\n2 - Main Menu\nCommand:")
            if choose==0:
                return "another_field"
            elif choose==1:
                return "field_menu"
            else:
                return "main_menu"
        else:
            food_keys=self.show_crops(save_file,foods_file)
            print(f"Plantable Area:{total_area}\n")
            selected_plant_index=self.commands.choose(0,len(food_keys)-1,"Select the Plant to Sow:")
            selected_plant=food_keys[selected_plant_index]
            max_plant=self.get_empty_capacity(selected_plant,total_area,save_file)
            
            print(f"You can plant a maximum of {max_plant}")
            
            amount=self.commands.choose(1,max_plant,"Enter the Amount of Plants to Sow:")
            selected_plant_name=self.general.food_finder(selected_plant,"name",foods_file)
            print(f"You will plant {amount} {selected_plant_name}\n")
            if self.commands.choose(0,1,"0 - Continue\n1 - Cancel\nCommand:")==0:
                self.plant_crop(amount,current_field_index,selected_plant,save_file,foods_file)
                print("Plant Successfully Sown.")       
                command_choose=self.commands.choose(0,2,"0 - Continue in Another Field\n1 - Do Another Action\n2 - Main Menu\nCommand:")
                if command_choose==0:
                    return "another_field"
                elif command_choose==1:
                    return "field_menu"
                else:
                    return "main_menu"
                    
                #Continue to plant or exit
            else:
                return "field_menu"
            


class HarvestManager:
    def __init__(self):
        self.general=helpers.General()
        self.table=helpers.Table()
        self.commands=helpers.Commands()
        self.time_manager=time_system.TimeManager()
        self.save_manager=helpers.SaveManager()
    
    def calculate_possibility(self,probability,amount):
        counter=0
        for i in range(amount):
            ...
        
    def calculate_growth_amount(self,elapsed_days,plant_time,deviation,amount):
        max_growth_day=plant_time+deviation
        min_growth_day=plant_time-deviation
        if elapsed_days<min_growth_day:
            return 0
        elif elapsed_days>=max_growth_day:
            return amount
        else:
            progress = (elapsed_days - min_growth_day) / (max_growth_day - min_growth_day)
            #bell curve probability
            progress=self.general.limit_value(progress,0,1)
            probability=self.general.growth_curve()(progress)
            return self.general.calculate_amount(amount,probability)
        
    def calculate_grown_plant(self,foods_file,save_file):
        fields=save_file["fields"]
        for field in fields:
            crops=field["crops"]
            for crop in crops:
                deviation=foods_file[crop["food"]]["deviation"]
                max_growth_day=crop["plant_time"]+deviation
                min_growth_day=crop["plant_time"]-deviation
                
                if crop["elapsed_days"]<min_growth_day:
                    continue
                elif crop["elapsed_days"]<max_growth_day:
                    crop["elapsed_days"]+1-min_growth_day
                else:#rot
                    ...
    
    def grown_field_table(self,foods_file,save_file,field_index):
        field=save_file["fields"][field_index]
        grown_amount_data=[]
        crops=field["crops"]
        index_list=[]
        counter=0
        for index,crop in enumerate (crops):
            key=crop["food"]
            name=foods_file[key]["name"]
            amount=crop["amount"]
            elapsed_days=crop["elapsed_days"]
            plant_time=crop["plant_time"]
            deviation=foods_file[key]["deviation"]
            ready=crop["ready"]
            
            #Show new system and write to json new variables
            #I IGNORE THIS BECAUSE THE CALCULATE MUST BE IN TIME SYSTEM
            #self.CalculateGrowthAmount(self,elapsed_days,plant_time,deviation,amount)
            if ready>0:
                grown_amount_data.append([counter,name,ready,amount])
                counter+=1
                index_list.append(index)
        return grown_amount_data,index_list            
    
    def show_grown_plants(self,grown_amount_data):
        title=["Crop Index","Plant","Ready","Amount"]
        self.table.show_table(grown_amount_data,title)
            
    def select_harvest(self,field_index,save_file):
        crops=save_file["fields"][field_index]["crops"]
        number_of_values=0
        for crop in crops:
            if crop["ready"]>0:
                number_of_values+=1
        crop_choose=self.commands.choose(0,number_of_values,f"Harvest Plants\nFor One Plant - [0,{number_of_values-1}]\nFor All - {number_of_values}\n>>")
        return crop_choose,number_of_values
    
    #HARVEST FROM THE BEGINNING
    def get_ready_amount(self,crop):
        #return save_file["fields"][field_index]["crops"][crop_index]["ready"]
        return crop["ready"]
    
    def reset_harvest_speed(self,remaining_speed):
        if remaining_speed==0:
            return config.HARVEST_SPEED
        return remaining_speed
    
    def calculate_harvest(self,ready,remaining_speed):
        harvested_amount=0
        if ready>=remaining_speed:
            ready-=remaining_speed
            harvested_amount+=remaining_speed
            remaining_speed=0
        else:
            remaining_speed-=ready
            harvested_amount+=ready
            ready=0
        return harvested_amount, remaining_speed, ready
    
    def update_harvest(self,crop,ready,harvested_amount,save_file):
        key=crop["food"]
        crop["ready"]=ready
        crop["amount"]-=harvested_amount
        save_file["foods"][key]["amount"]+=harvested_amount
            
    def is_hour_finished(self,remaining_speed):
        return remaining_speed == 0
    
    def pass_harvest_hour(self,save_file):
        #SPECIAL FOR HARVEST SYSTEM
        
        #ALL GENERAL THINGS
        self.time_manager.pass_hour(save_file)
        
    def is_crop_finished(self,crop):
        return self.get_ready_amount(crop) == 0
    
    def harvest_crop(self,crop,remaining_speed,save_file):
        ready=self.get_ready_amount(crop)
        while ready>0:   
            remaining_speed = self.reset_harvest_speed(remaining_speed)
            harvested_amount, remaining_speed, ready=self.calculate_harvest(ready,remaining_speed)
            self.update_harvest(crop,ready,harvested_amount,save_file)
            
            if self.is_hour_finished(remaining_speed):
                self.pass_harvest_hour(save_file)
        return remaining_speed                    
                         
    def harvest_field(self,field,save_file):
        remaining_speed = config.HARVEST_SPEED
        crops=field["crops"]
        for crop in crops:
            if self.is_crop_finished(crop):
                continue
            remaining_speed=self.harvest_crop(crop,remaining_speed,save_file)
        
        if remaining_speed<config.HARVEST_SPEED and remaining_speed!=0:
            self.pass_harvest_hour(save_file)        
      
    def harvest_one_crop(self,crop,save_file):
        #choose How much
        remaining_speed=self.harvest_crop(crop,config.HARVEST_SPEED,save_file)
        if remaining_speed<config.HARVEST_SPEED:
            self.pass_harvest_hour(save_file)  
    
    def compare_the_choose(self,number_of_values,crop_choose):
         return crop_choose==number_of_values
             
    def get_field(self,field_index,save_file):
        return save_file["fields"][field_index]         
    
    def find_to_delete_crop(self,crops):
        delete_list=[]
        for crop in crops:
            if crop["amount"]==0:
                delete_list.append(True)
            else:
                delete_list.append(False)
        return delete_list
    
    def crop_delete(self,crops,delete_list):
        for index in range(len(crops) - 1, -1, -1):
            if delete_list[index]:
                del crops[index]
                

                
        
        
    def start_harvest(self,field_index,save_file,foods_file):
        while True:
            start_time = save_file["time_system"]["time"]
            field=self.get_field(field_index,save_file)
            grown_amount_data,index_list=self.grown_field_table(foods_file,save_file,field_index)
            
            if not grown_amount_data:
                print(f"There Are No Plants to Harvest for Field {field_index}.")
                choose=self.commands.choose(0,1,"0 - Select Another Field\n1 - Do Another Action\nSelect Command:")
                if choose==0:
                    return "another_field"
                else:
                    return "field_menu"         
            else:
                print(f"\n=================== Field {field_index} ===================")
            
            self.show_grown_plants(grown_amount_data)
            crop_choose,number_of_values=self.select_harvest(field_index,save_file)
            
            if self.commands.choose(0,1,"0 - Continue\n1 - Cancel\n")==1:
                return "field_menu"
                
            if self.compare_the_choose(number_of_values,crop_choose):
                print(f"Harvested Amount:{sum(crop['ready'] for crop in field['crops'])}")
                self.harvest_field(field,save_file)
                message="Field Harvest Complete.\n0 - Select Field\n1 - Do Another Action\n2 - Main Menu\nCommand:"
                condition="another_field"
                
            else:
                crop_index=index_list[crop_choose]
                print(f"Harvested Amount:{field['crops'][crop_index]['ready']}")
                self.harvest_one_crop(field["crops"][crop_index],save_file)
                message="Plant Harvest Complete.\n0 - Harvest Again\n1 - Do Another Action\n2 - Main Menu\nCommand:"
                condition="another_crop"
            print("Field Being Harvested...")
                
            end_time = save_file["time_system"]["time"]
            print(f"Elapsed Time:{end_time-start_time}")
            #Show harvested amount
            #Add harvested plants to inventory
            #Warning if there are no ready plants in the field
            delete_list=self.find_to_delete_crop(field["crops"])
            self.crop_delete(field["crops"],delete_list)
            self.save_manager.save_file(config.SAVE_PATH,save_file)
            choice=self.commands.choose(0,2,message)
            if choice==0:
                if condition=="another_field":
                    return "another_field"
            elif choice==1:
                return "field_menu"
            else: 
                return "main_menu"  

class IrrigationManager:
    def __init__(self):
        self.general=helpers.General()
        self.table=helpers.Table()
        self.commands=helpers.Commands()
        self.time_manager=time_system.TimeManager()
        self.save_manager=helpers.SaveManager()

    def get_total_water_need(self,field, foods_file):
        total_water_need=0
        crops=field["crops"]
        for crop in crops:
            key=crop["food"]
            amount=crop["amount"]
            water_need_coefficient=foods_file[key]["water_need"]
            total_water_need+=water_need_coefficient*amount
        return total_water_need

    def required_water_for_field(self,field, foods_file):
        total_water_need=self.get_total_water_need(field, foods_file)
        return (100-field["water"])*total_water_need/100

    def get_irrigation_speed(self,energy):
        return (energy/100) * config.IRRIGATION_SPEED_CONSTANT

    def get_irrigation_time(self,required_water, speed):
        return math.ceil(required_water / speed)


    

    #Show

    def show_all_fields_overview(self,save_file, foods_file):
        fields=save_file["fields"]
        table_data=[]
        title=["Field","Moisture","Irrigation Cost","Estimated Time","Status"]
        for index,field in enumerate(fields):
            required_water=self.required_water_for_field(field, foods_file)
            energy=save_file["player_condition"]["energy"]
            irrigation_speed=self.get_irrigation_speed(energy)
            irrigation_time=self.get_irrigation_time(required_water, irrigation_speed)
            moisture=field["water"]
            if moisture==100:
                status="❌ Cannot Irrigate"
            else:
                status="💧 Irrigable"
            table_data.append([f"Field {index}",moisture,required_water,irrigation_time,status])
        total_required_water=sum(self.required_water_for_field(field, foods_file) for field in fields)
        total_irrigation_time=self.get_irrigation_time(total_required_water, speed=self.get_irrigation_speed(save_file["player_condition"]["energy"]))
        table_data.append(["All Fields","-",total_required_water,total_irrigation_time,"-"])
        return table_data,title

    def show_field_irrigation_info(self,field, save_file, foods_file,is_all_fields):
        energy = save_file["player_condition"]["energy"]
        speed = self.get_irrigation_speed(energy)
        clean_water = save_file["base_status"]["clean_water"]["current"]
        if is_all_fields:
            irrigable_fields = [field for field in save_file["fields"] if field["water"] < 100]
            required_water=sum(self.required_water_for_field(field, foods_file) for field in irrigable_fields)
            irrigation_time = self.get_irrigation_time(required_water, speed)
            print("================ Irrigation Summary  ================")
            print(f"Clean Water Tank     : {clean_water} L")
            print(f"Total Required Water : {required_water} L")
            is_fully_watered = len(irrigable_fields) == 0
            return self.calculate_irrigation_feasibility(is_fully_watered, required_water, clean_water, irrigation_time)
        else:
            required_water = self.required_water_for_field(field, foods_file)
            irrigation_time = self.get_irrigation_time(required_water, speed)
            print("================ Irrigation Summary  ================")
            print(f"Clean Water Tank     : {clean_water} L")
            print(f"Required Water       : {required_water} L")
            print(f"Moisture             : %{field['water']}")
            is_fully_watered = field["water"] == 100
            return self.calculate_irrigation_feasibility(is_fully_watered, required_water, clean_water, irrigation_time)

    def calculate_irrigation_feasibility(self, is_fully_watered, required_water, clean_water, irrigation_time):
        if is_fully_watered:
            result="💧 No Irrigation Needed"
        elif clean_water<required_water:
            print(f"Water Shortage     : {required_water-clean_water} L")
            print(f"Irrigation Time      : {irrigation_time} hours")
            result="❌ Insufficient Water Amount"
        else:
            print(f"Irrigation Time      : {irrigation_time} hours")
            result="✅ Irrigable"

        print(f"Status               : {result}     ")
        print("===============================================")
        return result

    def show_crops_water_info(self,field,foods_file):
        crops=field["crops"]
        table_data=[]
        title=["Plant","Amount","Water Need","Status"]
        for crop in crops:
            key=crop["food"]
            amount=crop["amount"]
            name=self.general.food_finder(key,"name",foods_file)
            water_need=self.general.food_finder(key,"water_need",foods_file)
            total_water_need = water_need * amount * (100 - field["water"]) / 100
            if water_need<2:
                result="🟢 Needs Little Water"
            elif water_need==2:
                result="🟡 Normal"
            else:
                result="🔴 Needs A Lot of Water"
            table_data.append([name,amount,total_water_need,result])
        self.table.show_table(table_data,title)


    def irigate_field(self,field,save_file,foods_file):
        required_water = self.required_water_for_field(field, foods_file)
        total_water_need = self.get_total_water_need(field, foods_file)
        is_done=True
        while required_water > 0:
            current_energy = save_file["player_condition"]["energy"]
            if save_file["player_condition"]["energy"]<config.IRRIGATION_ENERGY_THRESHOLD:#Energy Check whether the player has enough energy to irrigate
                print("Player is too exhausted to irrigate!")
                #Ask where to go
                is_done=False
                break
            elif save_file["base_status"]["clean_water"]["current"]<=0:#Water Check whether the player has enough water to irrigate
                print("Not enough clean water to irrigate!")
                #Ask where to go
                is_done=False
                break
            else:#Irrigation Process
                irrigation_speed = self.get_irrigation_speed(current_energy)
                available_water = save_file["base_status"]["clean_water"]["current"]
                applied_water = min(irrigation_speed, required_water, available_water)


                print(f"Irrigating Field {save_file['fields'].index(field)}...")
                save_file["player_condition"]["energy"]-=config.IRRIGATION_ENERGY_COST
                field["water"]+=(applied_water/total_water_need)*100
                if field["water"]>=100:
                    field["water"]=100
                    #Unused energy should be returned to the player
                    save_file["player_condition"]["energy"]+=math.floor((1 - (applied_water / irrigation_speed)) * config.IRRIGATION_ENERGY_COST)

                
                save_file["base_status"]["clean_water"]["current"]-=applied_water
                required_water-=applied_water
                self.time_manager.pass_hour(save_file)
        self.save_manager.save_file(config.SAVE_PATH,save_file)
        is_done = (field["water"] >= 100)
        return is_done



                
    def after_irrigation_menu(self,save_file,foods_file,is_done,field,is_all_fields):
        print("================ Irrigation Summary  ================")
        if is_all_fields:
            if is_done:
                print("All Fields Irrigated Successfully.")
            else:
                print("Irrigation Stopped Due to Insufficient Resources.")
            for index, field in enumerate(save_file["fields"]):
                print(f"Field {index} Moisture: {field['water']}%")
        else:
            if is_done:
                print(f"Field {save_file['fields'].index(field)} Irrigated Successfully.")
            else:
                print("Irrigation Stopped Due to Insufficient Resources.")
            print(f"Field {save_file['fields'].index(field)} Moisture: {field['water']}%")
        if is_all_fields:    
            choose=self.commands.choose(0,1,"0 - Select Another Field\n1 - Main Menu\nCommand:")
            return "another_field" if choose == 0 else "main_menu"
        else:
            choose=self.commands.choose(0,2,"0 - Select Another Field\n1 - Field Menu\n2 - Main Menu\nCommand:")
            if choose==0:
                return "another_field"
            elif choose==1:
                return "field_menu"
            else:
                return "main_menu"

    def water_controller(self,save_file, foods_file, field_index):
        self.show_field_irrigation_info(save_file["fields"][field_index], save_file, foods_file,False)
        select=self.commands.choose(0,1,f"0 - Continue from Field {field_index}\n1 - Change Field\nCommand:")
        if select==0:#Same Field
            self.show_crops_water_info(save_file["fields"][field_index], foods_file)
            field=save_file["fields"][field_index]
            status=self.show_field_irrigation_info(field, save_file, foods_file,False)
            if status=="❌ Insufficient Water Amount" or status=="💧 No Irrigation Needed":
                return self.after_irrigation_menu(save_file,foods_file,False,field,False)
            is_done=self.irigate_field(field,save_file,foods_file)
            return self.after_irrigation_menu(save_file,foods_file,is_done,field,False)
        else:#Change Field
            show_all_fields, title=self.show_all_fields_overview(save_file, foods_file)
            self.table.show_table(show_all_fields,title)
            choose=self.commands.choose(0,len(save_file["fields"]),f"Select a Field to Irrigate:\nTo Irrigate All Fields, Select {len(save_file['fields'])}\nCommand:")
            if choose == len(save_file['fields']):#Irrigate All Fields
                self.show_field_irrigation_info(save_file["fields"][field_index], save_file, foods_file,True)
                for field in save_file["fields"]:
                    if field["water"]<100:
                        is_done=self.irigate_field(field,save_file,foods_file)
                return self.after_irrigation_menu(save_file,foods_file,is_done,field,True)
            else:#Irrigate Selected Field
                field=save_file["fields"][choose]
                self.show_crops_water_info(save_file["fields"][field_index], foods_file)
                status=self.show_field_irrigation_info(field, save_file, foods_file,False)
                if status=="❌ Insufficient Water Amount" or status=="💧 No Irrigation Needed":
                    return self.after_irrigation_menu(save_file,foods_file,False,field,False)
                is_done=self.irigate_field(field,save_file,foods_file)
                return self.after_irrigation_menu(save_file,foods_file,is_done,field,False)

        
        
        
    
class AgricultureController:
    def __init__(self):
        self.save_manager = helpers.SaveManager()
        self.field_manager = FieldManager()
        self.commands=helpers.Commands()
        self.menu_manager=helpers.MenuManager()
        self.menu_data=MenuData()
        self.plant_manager = PlantManager(self.field_manager)
        self.harvest_manager=HarvestManager()
        self.irrigation_manager=IrrigationManager()
        self.save_file = None
        self.foods_file = None
        self.current_field = None
        self.current_field_index = None
    
    
    def field_menu(self):
        while True:
            field_menu_choose=self.menu_manager.show_menu(self.menu_data.field_menu_title,self.menu_data.field_menu_chooses)
            
            if field_menu_choose==0:
                result=self.plant_manager.plant_controller(self.current_field_index,self.save_file,self.foods_file)
                if result=="another_field":
                    #another field
                    return "another_field"
                
                elif result=="field_menu":
                    #same field and menu screen
                    continue
                else:
                    #Main Menu
                    return "main_menu"
                    
                
            elif field_menu_choose==1:
                result=self.harvest_manager.start_harvest(self.current_field_index,self.save_file,self.foods_file)
                if result =="another_field":
                    break
                elif result=="field_menu":
                    continue
                else:
                    return result       
            elif field_menu_choose==2:
                result=self.irrigation_manager.water_controller(self.save_file,self.foods_file,self.current_field_index)
                if result=="another_field":
                    break
                elif result=="main_menu":
                    return "main_menu"
                
            elif field_menu_choose==3:
                #Fertilize
                ...
            elif field_menu_choose==4:
                return "another_field"        
            else:
                return "main_menu"
    
    def run(self):
        self.foods_file=self.save_manager.read_file(config.FOODS_PATH)
        self.save_file=self.save_manager.read_file(config.SAVE_PATH)
        #LOOP START
        while True:
            self.field_manager.view_fields(self.save_file)
            #Should the index part change?
            self.current_field_index=self.commands.choose(0,len(self.save_file["fields"])-1,"Select a Field:")
            self.current_field=self.field_manager.get_field(self.save_file,self.current_field_index)
            #self.field_manager.MakeFieldTable(self.current_field,self.foods_file)
            self.field_manager.show_field(self.current_field,self.current_field_index,self.foods_file)
            #may write "you are doing for Field {self.current_field}"
            
            
            #THE TRUE START
            
            if self.field_menu()=="main_menu":
                return
                
        
        
if __name__ == "__main__":
    game = AgricultureController()
    game.run()        