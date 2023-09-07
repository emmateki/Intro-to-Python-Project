def generate_dungeon( height, width, nof_tundels):
    """Generating of dungeon/labyrinth
    
    This function will first create a maze full of walls "▓" and then it will generate the path "."
    When the user chose the number of paths the cycle will repaet itself until the number of path is achievd. 
    It is creating path in random direction and with random lenght.
    If the path recah the end it will come back to the beginning.
    It also alwazs chcek if the path is continous.

    Args:
        pocet_tunelov (int) : number of paths 
        height (int) : the height of the whole maze
        width (int) : the with of the whole maze

    Returns:
        Maze-it will return the whole labzrinth with all the paths.

    Raises:
        Format error when users input is not int.

    """
    import random
    """
    This module implements pseudo-random number generators for various distributions.
    """
    #definícia premenných
    wall = "▓"
    path = "."
    tunel=0
    width_rndm=1
    height_rndm=1
    #pocet tunelov sa načíta od užívatela
    # pocet_tunelov=int(input("Koľko chceš aby mal labyrint tunelov ?"))
    pocet_tunelov=nof_tundels

    #deklaracia a inicializacia prazdneho labyrintu
    maze = [[wall for x in range(width)] for y in range(height)]
    maze [1][1]=path

    #cyklus ktroý sa bude opakovať až pokým nebudeme mať náš počet tunelov
    while tunel<=pocet_tunelov:
        direction=random.randint(0,1) 
        #kontorla, či naše nové raidky a stĺpce nie sú mimo nášho zvoleného pola
        #ak to nieje splnené, začína sa oda začiatku
        if height_rndm>height-1 or 1>height_rndm or width_rndm>width-1 or 1>width_rndm:
                height_rndm=1
                width_rndm=1
        else: 
            #ak je direction nula bude sa robiť path v smere riadku teda sprava dolava       
            if direction == 0:       
                x=random.randint((0+width_rndm),(width-1))
                change=random.randint(1,x)
                #kontorla, či tá path na seba nadvezuje ak áno-pohneme sa dalej
                if maze[height_rndm][width_rndm-1]=="." or maze[height_rndm][width_rndm+1]=="." or maze[height_rndm][width_rndm]==".":
                    for i in range (width_rndm, x):
                        maze[height_rndm][i]=path

                    width_rndm=x-change
                    #tunel sa pripočíta len ak sa tunel úspešne vytvorí
                    tunel+=1
                #ak path nenadvezuje tak sa hodnota stlpca zmeni
                else:
                    change=random.randint(1,x)
                    width_rndm=x-change
                    continue 
            #ak je direction 1 bude sa robiť path zhora nasol 
            else: 
                y=random.randint((0+height_rndm),(height-1))
                change=random.randint(1,y)
                #kontorla, či tá path na seba nadvezuje ak áno-pohneme sa dalej
                if maze[height_rndm-1][width_rndm]=="." or maze[height_rndm][width_rndm]=="." or maze[height_rndm+1][width_rndm]==".":

                    for i in range (height_rndm, y):
                        maze[i][width_rndm]=path   

                    height_rndm=y-change
                    tunel+=1
                #ak path nenadvezuje tak sa hodnota riadku zmeni
                else:
                    change=random.randint(1,y)
                    height_rndm=y-change
                    continue 
    return maze


