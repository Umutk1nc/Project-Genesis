import os
import json
import random
import math
import config
from tabulate import tabulate
class Screen:
    def Clear(self):
        os.system('cls' if os.name=="nt" else 'clear')

class General:
    def Limit_Value(self,value,minimum,maximum):
        if value>maximum:
            value=maximum
        if value<minimum:
            value=minimum
        return value 
    def Food_Finder(self,key,searching,FOODS_FILE):
        return FOODS_FILE[key][searching]
    
    
    def GrowthCurve(self,progress):
        return 1 / (1 + math.exp(-config.CURVE_CONSTANT * (progress - 0.5)))
        
    
    def Chance(self,probability):
        return random.random()<probability
    
    def CalculateAmount(self,amount, probability):
        ready=0
        for i in range(amount):
            if self.Chance(probability):
                ready +=1
        return ready
    
    

class SaveManager:
    def ReadFile(self,PATH):
        with open(PATH,"r",encoding="utf-8") as file:
            return json.load(file)

#While you are saving a file you can do:
#Read DATA=ReadFile(self,PATH)  
#Change DATA[]...[domates]=5
#Save SaveFile (self,PATH,DATA)

    def SaveFile (self,PATH,DATA):
        with open(PATH, "w", encoding="utf-8") as file:
            json.dump(DATA,file,indent=4, ensure_ascii=False)

class Table:
    def Show_Table(self,row,column):
        print(tabulate(row, headers=column, tablefmt="fancy_grid"))

class Commands:
    def Choose(self,minimum,maximum,message):
        while True:
            choice_value=input(message)
            if choice_value.isdigit():
                choice_value = int(choice_value)
                if choice_value<=maximum and choice_value>=minimum:
                    return choice_value
                else:#again and again message may write
                    print(f"Lütfen " ,minimum, "-",maximum,"aralığında sayı gir! ")
            else:
                print("Lütfen geçerli bir komut gir! ")
    def Choice(self):
        choice=self.Choose(1,2,"1 - Tekrar Dene\n2 - Vazgeç\nKomutun:")            
        if choice == 1:
            return 1

        elif choice == 2:
            return 2 

class MenuMananger:
    def __init__(self):
        self.commands=Commands()
                
    def ShowMenu(self,title,options):
        print(f"=================={title} Menüsü=================\n")
        for index,option in enumerate(options):
            print(f"{index} - {option}\n")
        string="Komut Seç:"
        return self.commands.Choose(0,index,string)
    

object=Screen()
object.Clear()