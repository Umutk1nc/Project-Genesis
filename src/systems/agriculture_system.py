import math
import config
import helpers
import time_system

class MenuData:
    def __init__(self):
        
        self.field_menu_title="Tarla"
        self.field_menu_chooses=["Ekim","Hasat","Sulama","Gübreleme","Başka Tarla Seç","Ana Menü"]
   
        

class FieldManager:
    def __init__(self):
        self.table=helpers.Table()
        self.general=helpers.General()        
        
    def View_Fields(self,SAVE_FILE):
        fields=SAVE_FILE["fields"]
        title=["Index", "Miktar","Hazır","Su","Verim", "Sıcaklık"]
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
            print(f"\n===================== Tarla {field_index} =====================")
            self.table.Show_Table(table_data,title)      
    
    def GetField(self,SAVE_FILE,field_index):
        return SAVE_FILE["fields"][field_index]   
    
    def GetTotal(self,crops):
        return sum(crop["amount"] for crop in crops)
                            
    def Show_Field(self,field,index,FOODS_FILE):
        crops=field["crops"]
        field_data=[]
        total_amount=self.GetTotal(crops)
        total_ready = sum(crop["ready"] for crop in crops)
        print(f"\n=============== Tarla {index} ===============")
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
            name=self.general.Food_Finder(food_key,"name",FOODS_FILE)
            amount=crop["amount"]
            elapsed_days=crop["elapsed_days"]
            plant_time=crop["plant_time"]
            ready=crop["ready"]
            hp=crop["hp"]
            field_data.append([name,amount,f"{elapsed_days}/{plant_time}",ready,hp])
        title=["Bitki","Miktar","Büyüme","Hazır","HP"]
        self.table.Show_Table(field_data,title)
            
    #def Show_Field_Crops(self,)    

    
    
class PlantManager:
    def __init__(self,field_manager):
        self.table=helpers.Table()
        self.general=helpers.General()
        self.save_manager=helpers.SaveManager()
        self.commands=helpers.Commands()
        self.field_manager=field_manager
    
    def ShowCrops(self,save_file,foods_file):
        table_data=[]
        food_keys=[]
        index=0  
        foods=save_file["foods"]
        for food_key in foods:
            amount=foods[food_key]["miktar"]
            if amount>0: 
                name=self.general.Food_Finder(food_key,"name",foods_file)
                food_keys.append(food_key)
                table_data.append([index,name,amount])
                index+=1
        #Su ışık ihtiyacı olma süresi
        #burada detaylı göster menüsü olsun böyle olursa eating systemdeki detaylı gösterilen bitki tablosu gelsin
        title=["Index","Bitki","Miktar"]  
        self.table.Show_Table(table_data,title)
        return food_keys
    
    def FindEmptyArea(self,field,save_field):
        capacity=save_field["fields"][field]["capacity"]
        crops=save_field["fields"][field]["crops"]
        total_amount=self.field_manager.GetTotal(crops)
        return capacity-total_amount        
    
    def GetEmptyCapacity(self,selected_plant,total_area,save_file):
        if save_file["foods"][selected_plant]["miktar"]<total_area:
            return save_file["foods"][selected_plant]["miktar"]
        else:
            return total_area
    
    def PlantCrop(self,amount,field_index,plant_key,save_file,foods_file):
        save_file["foods"][plant_key]["miktar"]-=amount
        crops=save_file["fields"][field_index]["crops"]
        growth_time=foods_file[plant_key]["buyume_gunu"]
        new_crop = {
        "food": plant_key,
        "amount": amount,
        "plant_time": growth_time,
        "elapsed_days": 0,
        "ready":0,
        "hp": 100}
        crops.append(new_crop)
        self.save_manager.SaveFile(config.SAVE_PATH,save_file)
    
    def PlantController(self,current_field_index,save_file,foods_file):
        food_keys=self.ShowCrops(save_file,foods_file)
        total_area=self.FindEmptyArea(current_field_index,save_file)
        if total_area==0:
            print("Maximum ekim kapasitesine ulaşıldı.\n")
            choose=self.commands.Choose(0,2,"0 - Başka Tarlada Ekim Yap\n1 - Başka İşlem Yap\n2 - Ana Menü\nKomut:")
            if choose==0:
                return "another_field"
            elif choose==1:
                return "field_menu"
            else:
                return "main_menu"
        else:
            print(f"Ekilebilir Alan:{total_area}\n")
            selected_plant_index=self.commands.Choose(0,len(food_keys)-1,"Ekilecek Bitkiyi Seç:")
            selected_plant=food_keys[selected_plant_index]
            max_plant=self.GetEmptyCapacity(selected_plant,total_area,save_file)
            
            print(f"Maksimum {max_plant} miktarda ekebilirsin")
            
            amount=self.commands.Choose(1,max_plant,"Ekilecek Bitki Miktarını Yaz:")
            selected_plant_name=self.general.Food_Finder(selected_plant,"name",foods_file)
            print(f"{amount} tane {selected_plant_name} ekeceksin\n")
            if self.commands.Choose(0,1,"0 - Devam et\n1 - Vazgeç\nKomut:")==0:
                self.PlantCrop(amount,current_field_index,selected_plant,save_file,foods_file)
                print("Bitki Başarıyla Ekildi.")       
                command_choose=self.commands.Choose(0,2,"0 - Başka Tarlada Devam et\n1 - Başka İşlem Yap\n2 - Ana Menü\nKomut:")
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
    
    def CalculatePossibility(self,probability,amount):
        counter=0
        for i in range(amount):
            ...
        
    def CalculateGrowthAmount(self,elapsed_days,plant_time,deviation,amount):
        MAX_GROWTH_DAY=plant_time+deviation
        MIN_GROWTH_DAY=plant_time-deviation
        if elapsed_days<MIN_GROWTH_DAY:
            return 0
        elif elapsed_days>=MAX_GROWTH_DAY:
            return amount
        else:
            progress = (elapsed_days - MIN_GROWTH_DAY) / (MAX_GROWTH_DAY - MIN_GROWTH_DAY)
            #bell curve probability
            progress=self.general.Limit_Value(progress,0,1)
            probability=self.general.GrowthCurve()(progress)
            return self.general.CalculateAmount(amount,probability)
        
    def CalculateGrownPlant(self,foods_file,save_file):
        fields=save_file["fields"]
        for field in fields:
            crops=field["crops"]
            for crop in crops:
                deviation=foods_file[crop["food"]]["sapma"]
                MAX_GROWTH_DAY=crop["plant_time"]+deviation
                MIN_GROWTH_DAY=crop["plant_time"]-deviation
                
                if crop["elapsed_days"]<MIN_GROWTH_DAY:
                    continue
                elif crop["elapsed_days"]<MAX_GROWTH_DAY:
                    crop["elapsed_days"]+1-MIN_GROWTH_DAY
                else:#çürüme
                    ...
    
    def GrownFieldTable(self,foods_file,save_file,field_index):
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
            deviation=foods_file[key]["sapma"]
            ready=crop["ready"]
            
            #Show new system and write to json new variables
            #I IGNORE THIS BECAUSE THE CALCULATE MUST BE IN TIME SYSTEM
            #self.CalculateGrowthAmount(self,elapsed_days,plant_time,deviation,amount)
            if ready>0:
                grown_amount_data.append([counter,name,ready,amount])
                counter+=1
                index_list.append(index)
        return grown_amount_data,index_list            
    
    def Show_Grown_Plants(self,grown_amount_data):
        title=["Crop Index","Bitki","Hazır","Miktar"]
        self.table.Show_Table(grown_amount_data,title)
            
    def Select_Harvest(self,field_index,save_file):
        crops=save_file["fields"][field_index]["crops"]
        number_of_values=0
        for crop in crops:
            if crop["ready"]>0:
                number_of_values+=1
        crop_choose=self.commands.Choose(0,number_of_values,f"Bitkileri Hasat Et\nBir Bitki İçin - [0,{number_of_values-1}]\nTüm Hepsi İçin - {number_of_values}\n>>")
        return crop_choose,number_of_values
    
    #HARVEST FROM THE BEGİNİNG
    def GetReadyAmount(self,crop):
        #return save_file["fields"][field_index]["crops"][crop_index]["ready"]
        return crop["ready"]
    
    def ResetHarvestSpeed(self,remaining_speed):
        if remaining_speed==0:
            return config.HARVEST_SPEED
        return remaining_speed
    
    def CalculateHarvest(self,ready,remaining_speed):
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
    
    def UpdateHarvest(self,crop,ready,harvested_amount,save_file):
        key=crop["food"]
        crop["ready"]=ready
        crop["amount"]-=harvested_amount
        save_file["foods"][key]["miktar"]+=harvested_amount
            
    def IsHourFinished(self,remaining_speed):
        return remaining_speed == 0
    
    def PassHarvestHour(self,save_file):
        #SPECIAL FOR HARVEST SYSTEM
        
        #ALL GENERAL THINGS
        self.time_manager.PassHour(save_file)
        
    def IsCropFinished(self,crop):
        return self.GetReadyAmount(crop) == 0
    
    def HarvestCrop(self,crop,remaining_speed,save_file):
        ready=self.GetReadyAmount(crop)
        while ready>0:   
            remaining_speed = self.ResetHarvestSpeed(remaining_speed)
            harvested_amount, remaining_speed, ready=self.CalculateHarvest(ready,remaining_speed)
            self.UpdateHarvest(crop,ready,harvested_amount,save_file)
            
            if self.IsHourFinished(remaining_speed):
                self.PassHarvestHour(save_file)
        return remaining_speed                    
                         
    def HarvestField(self,field,save_file):
        remaining_speed = config.HARVEST_SPEED
        crops=field["crops"]
        for crop in crops:
            if self.IsCropFinished(crop):
                continue
            remaining_speed=self.HarvestCrop(crop,remaining_speed,save_file)
        
        if remaining_speed<config.HARVEST_SPEED and remaining_speed!=0:
            self.PassHarvestHour(save_file)        
      
    def HarvestOneCrop(self,crop,save_file):
        #choose How much
        remaining_speed=self.HarvestCrop(crop,config.HARVEST_SPEED,save_file)
        if remaining_speed<config.HARVEST_SPEED:
            self.PassHarvestHour(save_file)  
    
    def CompareTheChoose(self,number_of_values,crop_choose):
         return crop_choose==number_of_values
             
    def GetField(self,field_index,save_file):
        return save_file["fields"][field_index]         
    
    def FindToDeleteCrop(self,crops):
        delete_list=[]
        for crop in crops:
            if crop["amount"]==0:
                delete_list.append(True)
            else:
                delete_list.append(False)
        return delete_list
    
    def CropDelete(self,crops,delete_list):
        for index in range(len(crops) - 1, -1, -1):
            if delete_list[index]:
                del crops[index]
                

                
        
        
    def StartHarvest(self,field_index,save_file,foods_file):
        while True:
            start_time = save_file["time_system"]["time"]
            field=self.GetField(field_index,save_file)
            grown_amount_data,index_list=self.GrownFieldTable(foods_file,save_file,field_index)
            
            if not grown_amount_data:
                print(f"Tarla {field_index} İçin Hasat Edilecek Hiç Bitki Yok.")
                choose=self.commands.Choose(0,1,"0 - Başka Tarla Seç\n1 - Başka İşlem Yap\nKomut Seç:")
                if choose==0:
                    return "another_field"
                else:
                    return "field_menu"         
            else:
                print(f"\n=================== Tarla {field_index} ===================")
            
            self.Show_Grown_Plants(grown_amount_data)
            crop_choose,number_of_values=self.Select_Harvest(field_index,save_file)
            
            if self.commands.Choose(0,1,"0 - Devam et\n1 - Vazgeç\n")==1:
                return "field_menu"
                
            if self.CompareTheChoose(number_of_values,crop_choose):
                print(f"Hasat Edilen Miktar:{sum(crop['ready'] for crop in field['crops'])}")
                self.HarvestField(field,save_file)
                message="Tarla Hasadı Bitti.\n0 - Tarla Seç\n1 - Başka İşlem Yap\n2 - Ana Menü\nKomut:"
                condition="another_field"
                
            else:
                crop_index=index_list[crop_choose]
                print(f"Hasat Edilen Miktar:{field['crops'][crop_index]['ready']}")
                self.HarvestOneCrop(field["crops"][crop_index],save_file)
                message="Bitki Hasadı Bitti.\n0 - Başka Hasat Yap\n1 - Başka İşlem Yap\n2 - Ana Menü\nKomut:"
                condition="another_crop"
            print("Tarla Hasat Ediliyor...")
                
            end_time = save_file["time_system"]["time"]
            print(f"Geçen Zaman:{end_time-start_time}")
            #Hasat edilen miktar göster
            #Hasat ediln Bitkileri Envantere Ekle
            #Tarlada hiç hazır bitki yok uyarısı
            delete_list=self.FindToDeleteCrop(field["crops"])
            self.CropDelete(field["crops"],delete_list)
            self.save_manager.SaveFile(config.SAVE_PATH,save_file)
            choice=self.commands.Choose(0,2,message)
            if choice==0:
                if condition=="another_field":
                    return "another_field"
            elif choice==1:
                return "field_menu"
            else: 
                return "main_menu"  

    
class WaterManager:
    def __init__(self):
        self.general=helpers.General()
        self.table=helpers.Table()
        self.commands=helpers.Commands()
        self.time_manager=time_system.TimeManager()
        self.save_manager=helpers.SaveManager()
    #GET AND CALCULATE
    
    def GetCleanWater(self,save_file):
        return save_file["us_durumu"]["temiz_su"]["mevcut"]
    
   
   
    def CalculateHourlyWaterNeed(self,amount,water_need_coefficient):
       return water_need_coefficient*amount/config.IRRIGATION_CONSTANT
   
    
       
    def CalculateCropsWaterNeed(self,crops,foods_file):
        hourly_water_need_array=[]
        for crop in crops:
            key=crop["food"]
            amount=crop["amount"]
            water_need_coefficient=foods_file[key]["su_ihtiyaci"]                  
            hourly_water_need=self.CalculateHourlyWaterNeed(amount,water_need_coefficient)
            hourly_water_need_array.append(hourly_water_need)
        return hourly_water_need_array
   
   
            
    def CalculateFieldWaterNeed(self,field,foods_file):
        crops=field["crops"]
        hourly_water_need_array=self.CalculateCropsWaterNeed(crops,foods_file)
        return sum(hourly_water_need_array)
    
    def CalculateAllFieldsWaterNeed(self,save_file, foods_file):
        fields=save_file["fields"]
        return sum(self.CalculateFieldWaterNeed(field,foods_file) for field in fields)
    
    
    def CalculateIrrigationSpeed(self,energy):
        other_speed_factors=1
        return energy*config.IRRIGATION_SPEED_CONSTANT*other_speed_factors/100
        
    
    def CalculateIrrigationTime(self,save_file,current_water_need):
        energy=save_file["player_condition"]["enerji"]
        current_speed=self.CalculateIrrigationSpeed(energy)
        return math.ceil(current_water_need/current_speed)
    
    def CalculateCurrentWaterNeed(self,field,foods_file):
        hourly_need=self.CalculateFieldWaterNeed(field,foods_file)
        return (100-field["water"])*hourly_need*config.IRRIGATION_CONSTANT/100
    
            
    #CREATE AND SHOW
    def CreateFieldWaterTable(self,field, foods_file,save_file):
        crops=field["crops"]
        table_data=[]
        amount=sum(crop["amount"] for crop in crops)
        capacity=field["capacity"]
        fertility=field["fertility"]
        water=field["water"]
        current_water_need=self.CalculateCurrentWaterNeed(field,foods_file)
        time_need=self.CalculateIrrigationTime(save_file,current_water_need)
        title=["Nem","Su İhtiyacı","Sulama Süresi","Verim","Doluluk"]
        table_data.append([f"%{water}",current_water_need,time_need,fertility,f"{amount}/{capacity}"])
        return table_data,title
    
    def CreateCropsWaterTable(self,field,foods_file):
        crops=field["crops"]
        table_data=[]
        title=["Bitki","Miktar","Su İhtiyacı","Durum"]
        total_water_need_array=self.CalculateCropsWaterNeed(crops,foods_file)
        
        for index,crop in enumerate(crops):
            amount=crop["amount"]
            key=crop["food"]
            name=self.general.Food_Finder(key,"name",foods_file)
            water_need=self.general.Food_Finder(key,"su_ihtiyaci",foods_file)
            if water_need<2:
                result="🟢 Az Su İster"
            elif water_need==2:
                result="🟡 Normal"
            else:
                result="🔴 Çok Su İster"
            table_data.append([name,amount,total_water_need_array[index],result])
        self.table.Show_Table(table_data,title)
        return table_data,title
    
    def IsFieldFullyWatered(self,field):
        return field["water"]==100
        
        
    
    def ShowIrrigationInfo(self,field,save_file,foods_file):
        clean_water=save_file["us_durumu"]["temiz_su"]["mevcut"]
        current_water_need=self.CalculateCurrentWaterNeed(field,foods_file)
        water_time=self.CalculateIrrigationTime(save_file,current_water_need)
        
        print("================ Sulama Özeti  ================")
        print(f"Temiz Su Deposu      : {clean_water} L")
        print(f"Gerekli Su           : {current_water_need} L")
        print(f"Nem                  : %{field["water"]}")
        
        if self.IsFieldFullyWatered(field):
            result="💧 Sulamaya Gerek Yok"
        elif clean_water<current_water_need:
            print(f"Eksik Su           : {current_water_need-clean_water} L")
            print(f"Sulama Süresi        : {water_time} saat")
            result="❌ Yetersiz Su Miktarı"
        else:
            print(f"Sulama Süresi        : {water_time} saat")
            result="✅ Sulanabilir"

        print(f"Durum                : {result}     ")
        print("===============================================")
        
        return result
    
    def ShowFieldWaterCost(self,field,foods_file):
        return self.CalculateFieldWaterNeed(field,foods_file)*config.IRRIGATION_CONSTANT
    
    def ShowAllFieldsWaterCost(self,save_file,foods_file):
        return self.CalculateAllFieldsWaterNeed(save_file,foods_file)*config.IRRIGATION_CONSTANT
    
    def CreateCosts(self,save_file,foods_file):
        table_data=[]
        fields=field=save_file["fields"]
        
        title=["Tarla","Nem","Sulama Maliyeti","Tahmini Süre","Durum"]
        for index,field in enumerate(fields):
            real_water_need=self.CalculateCurrentWaterNeed(field,foods_file)
            field_time_need=self.CalculateIrrigationTime(save_file,real_water_need)
            humidity=field["water"]
            real_water_need=self.CalculateCurrentWaterNeed(field,foods_file)
            if humidity==100:
                condition="❌ Sulanamaz"
            else:
                condition="💧 Sulanabilir"
            table_data.append([f"Tarla {index}",humidity,real_water_need,field_time_need,condition])
        
        total_water_need=sum(self.CalculateCurrentWaterNeed(field,foods_file) for field in fields)
        total_time_need=self.CalculateIrrigationTime(save_file,total_water_need)
        
        table_data.append(["Tüm Tarlalar","-",total_water_need,total_time_need,"-"])
        return table_data,title
    
    
    def ShowCosts(self,save_file,foods_file):
        table_data,title=self.CreateCosts(save_file,foods_file)
        self.table.Show_Table(table_data,title)
    #OPTIONS
    
    def SelectWaterMode(self,field_index):
        choose=self.commands.Choose(0,2,f"0 - Tarla {field_index}'den devam et\n1 - Tarla Değiştir\nKomut:")
        return choose
    
    
    def ConfirmWatering(self):
        choose=self.commands.Choose(0,1,"0 - Sulamaya Başla\n1 - Vazgeç\nKomut:") 
        if choose==1:
            return "field_menu"
        
        
    def AfterWaterMenu(self):
        choose=self.commands.Choose(0,1,"0 - Başka Sulama Yap\n1 - Tarla Menüsüne Dön\n2 - Ana Menü\nKomut:") 
        if choose==1:
            return "field_menu"
        elif choose==2:
            return "main_menu"
    
    #IRRIGRATION 
    def WaterField(self,field,foods_file,save_file):
        water_cost=self.CalculateFieldWaterNeed(field,foods_file)*config.IRRIGATION_CONSTANT
        energy=save_file["player_condition"]["enerji"]
        current_speed=self.CalculateIrrigationSpeed(energy)
        
    
    #CONTROLLER   
    def WaterController(self,save_file,foods_file,field_index):
        field=save_file["fields"][field_index]
        #print(f"\n=============== Tarla {field_index} ===============")
        clean_water=self.GetCleanWater(save_file)
        self.ShowCosts(save_file,foods_file)
        choose=self.SelectWaterMode(field_index)
        
        if choose==1:
            field_choose=self.commands.Choose(0,len(save_file["fields"]),f"Tarla Seç\nBir Tarla İçin -> [0,{len(save_file["fields"])-1}]\nTüm Tarlalar İçin -> {len(save_file["fields"])}\nKomut:")
            if field_choose==len(save_file["fields"]):
                ...
            else:
                field=save_file["fields"][field_choose]
                
                
        table_data,title=self.CreateFieldWaterTable(field,foods_file,save_file)
        self.table.Show_Table(table_data,title)          
        self.CreateCropsWaterTable(field,foods_file)
        irrigation_result=self.ShowIrrigationInfo(field,save_file,foods_file)
        if irrigation_result=="✅ Sulanabilir":
            result=self.ConfirmWatering()
        else:
            command=self.commands.Choose(0,1,"0 - Başka Tarla Sula\1 - Tarla Menüsüne Dön\nKomut:")
            if command==0:
                ...
                #continue
            else:
                return "field_menu"
        
        if result=="field_menu":
            return "field_menu"
        self.WaterField(field,foods_file,save_file) 
            
            
        
        
        
    
class AgricultureController:
    def __init__(self):
        self.save_manager = helpers.SaveManager()
        self.field_manager = FieldManager()
        self.commands=helpers.Commands()
        self.menu_manager=helpers.MenuMananger()
        self.menu_data=MenuData()
        self.plant_manager = PlantManager(self.field_manager)
        self.harvest_manager=HarvestManager()
        self.water_manager=WaterManager()
        self.save_file = None
        self.foods_file = None
        self.current_field = None
        self.current_field_index = None
    
    
    def FieldMenu(self):
        while True:
            field_menu_choose=self.menu_manager.ShowMenu(self.menu_data.field_menu_title,self.menu_data.field_menu_chooses)
            
            if field_menu_choose==0:
                result=self.plant_manager.PlantController(self.current_field_index,self.save_file,self.foods_file)
                if result=="another_field":
                    #another field
                    break
                elif result=="field_menu":
                    #same field and menu screen
                    continue
                else:
                    #Main Menu
                    return "main_menu"
                    
                
            elif field_menu_choose==1:
                result=self.harvest_manager.StartHarvest(self.current_field_index,self.save_file,self.foods_file)
                if result =="another_field":
                    break
                elif result=="field_menu":
                    continue
                else:
                    return result       
            elif field_menu_choose==2:
                self.water_manager.WaterController(self.save_file,self.foods_file,self.current_field_index)
            elif field_menu_choose==3:
                #Gübrele
                ...
            elif field_menu_choose==4:
                return "another_field"        
            else:
                return "main_menu"
    
    def Run(self):
        self.foods_file=self.save_manager.ReadFile(config.FOODS_PATH)
        self.save_file=self.save_manager.ReadFile(config.SAVE_PATH)
        #LOOP START
        while True:
            self.field_manager.View_Fields(self.save_file)
            #Index kısmı değişsin mi?
            self.current_field_index=self.commands.Choose(0,len(self.save_file["fields"])-1,"Bir Tarla Seç:")
            self.current_field=self.field_manager.GetField(self.save_file,self.current_field_index)
            #self.field_manager.MakeFieldTable(self.current_field,self.foods_file)
            self.field_manager.Show_Field(self.current_field,self.current_field_index,self.foods_file)
            #may write "you are doing for Field {self.current_field}"
            
            
            #THE TRUE START
            
            if self.FieldMenu()=="main_menu":
                return
                
        
        
        
game=AgricultureController()
game.Run()

