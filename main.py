from dungeon import Dungeon
from copy import deepcopy
import subprocess
import datetime

if __name__ == "__main__":
    load_game = input("wanna load a game: y/n")
    if load_game == 'n':
        hero_name = input("What is your name hero?")
        dungeon = Dungeon(size=(20, 20), tunnel_number=20, hero_name=hero_name)
        dungeon.create_dungeon()
    else:
        
        path = input("Write path to the file in form : myfile_datetime.py")
        # extract the filename by splitting the path and getting onlyt he last part
        filename = path.split("/")[-1]   
        hero_name = filename.split("_")[0]               
        dungeon = Dungeon(size=(20, 20), tunnel_number=20, hero_name=hero_name)
        dungeon.dungeon_map = []
        pos = []
        
        with open( path, 'r') as f:
            dungeon_map = f.readlines()  # Read all lines in the file and store them in a list
            for i in range (len(dungeon_map)):
                l = [] 
                if dungeon_map[i].strip() == "#": break
                for j in range(len(dungeon_map[0])-1):
                    if dungeon_map[i][j] == 'g': pos.append(tuple([i, j]))
                    l.append(dungeon_map[i][j])
                dungeon.dungeon_map.append(l)

            dungeon.hero.hp=int(dungeon_map[i+1])
            dungeon.hero.position[0] = int(dungeon_map[i+2])
            dungeon.hero.position[1] = int(dungeon_map[i+3])

        dungeon.place_entities2(pos)
        dungeon.current_map = deepcopy(dungeon.dungeon_map)
        dungeon.current_map[dungeon.hero.position[0]][dungeon.hero.position[1]] = dungeon.hero.map_identifier


    while True:
        #subprocess.Popen("cls", shell=True).communicate()
        print(dungeon)
        print(dungeon.message)
        action = input(f"Select an action {hero_name}: (L)EFT, (R)IGHT, (D)OWN, (U)P, (A)TTACK, (Q)UIT, (S)AVE")
        if action == "Q":
            print("You coward!")
            exit(0)
        elif action == "S":
            timestamp = str(datetime.datetime.now())
            with open(hero_name+"_"+timestamp+".dng", 'w') as file:
                for i in range(dungeon.size[0]):
                    for j in range(dungeon.size[1]):
                        if dungeon.dungeon_map[i][j] =='\x1b[38;5;1mg\x1b[0;0m':
                            file.write('g')                           
                        else:
                            file.write(dungeon.dungeon_map[i][j])
                    file.write('\n')
                #separator 
                file.write("#"+'\n')
                file.write(str(dungeon.hero.hp))
                file.write('\n')
                file.write(str(dungeon.hero.position[0]))
                file.write('\n')
                file.write(str(dungeon.hero.position[1]))
                
                

            exit(0)
        else:
            dungeon.hero_action(action)
        if dungeon.hero.hp < 1:
            print(dungeon.message)
            exit(0)