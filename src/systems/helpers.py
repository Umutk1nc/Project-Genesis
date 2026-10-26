import os
import json
import random
import math
import config
from tabulate import tabulate
class Screen:
    def clear(self):
        os.system('cls' if os.name=="nt" else 'clear')

class General:
    def limit_value(self,value,minimum,maximum):
        if value>maximum:
            value=maximum
        if value<minimum:
            value=minimum
        return value 
    def food_finder(self,key,searching,foods_file):
        return foods_file[key][searching]
    
    
    def growth_curve(self,progress):
        return 1 / (1 + math.exp(-config.CURVE_CONSTANT * (progress - 0.5)))
        
    
    def chance(self,probability):
        return random.random()<probability
    
    def calculate_amount(self,amount, probability):
        ready=0
        for i in range(amount):
            if self.chance(probability):
                ready +=1
        return ready
    
    

class SaveManager:
    def read_file(self,path):
        with open(path,"r",encoding="utf-8") as file:
            return json.load(file)

#While you are saving a file you can do:
#Read DATA=ReadFile(self,PATH)  
#Change DATA[]...[domates]=5
#Save SaveFile (self,PATH,DATA)

    def save_file (self,path,data):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data,file,indent=4, ensure_ascii=False)

class Table:
    def show_table(self,row,column):
        print(tabulate(row, headers=column, tablefmt="fancy_grid"))

class Commands:
    def choose(self,minimum,maximum,message):
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
    def choice(self):
        choice=self.choose(1,2,"1 - Tekrar Dene\n2 - Vazgeç\nKomutun:")            
        if choice == 1:
            return 1

        elif choice == 2:
            return 2 

class MenuManager:
    def __init__(self):
        self.commands=Commands()
                
    def show_menu(self,title,options):
        print(f"=================={title} Menüsü=================\n")
        for index,option in enumerate(options):
            print(f"{index} - {option}\n")
        string="Komut Seç:"
        return self.commands.choose(0,index,string)
    

object=Screen()
object.clear()