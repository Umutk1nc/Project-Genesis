import sys
from pathlib import Path

#Defining the path to the src/systems directory and adding it to sys.path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))
sys.path.append(str(ROOT_DIR / "src" / "systems"))

#Dependency imports
from src.systems.agriculture_system import AgricultureController
from src.systems.eating_system import EatingController
from src.systems import helpers 
menu_manager = helpers.MenuManager()
while True:
    command=menu_manager.show_menu("Main",["Agriculture System","Eating System","Exit"])
    if command==0:
        agriculture_controller = AgricultureController()
        agriculture_controller.run()
    elif command==1:
        eating_controller = EatingController()
        eating_controller.run()
    elif command==2:
        print("Exiting the game...")
        sys.exit()