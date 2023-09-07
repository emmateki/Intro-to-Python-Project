from abstract_classes import AbstractDungeon
from copy import deepcopy
from map_entities import Hero, Goblin

import random

import  emmka_generator


class Dungeon(AbstractDungeon):
    def __init__(self, size: tuple, tunnel_number: int, hero_name: str):
        super().__init__(size)
        self.hero = Hero("@", hero_name, [1, 1], 5, 5, 1)
        self.tunnel_number = tunnel_number
        self.starting_entities = ["goblin", "goblin", "goblin", "goblin", "goblin", "goblin", "goblin", "goblin", "goblin", "goblin", "goblin", "goblin"]
        self.entities = []
        self.empty_space = []
        self.message = ""

    def __str__(self):
        printable_map = ""
        for row in self.current_map:
            for column in row:
                printable_map += column
            printable_map += "\n"
        return printable_map
    

    def create_dungeon(self):
        # generate dungeon
        self.dungeon_map = emmka_generator.generate_dungeon(
            self.size[0],
            self.size[1],
            self.tunnel_number
        )
        
        # locate empty spaces
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.dungeon_map[i][j] == '.':
                    self.empty_space.append(tuple([i, j])) 

        self.place_entities(self.starting_entities)
        self.current_map = deepcopy(self.dungeon_map)
        self.empty_space = list(map(list,set(self.empty_space)))
        self.current_map[self.hero.position[0]][self.hero.position[1]] = self.hero.map_identifier

    def hero_action(self, action):
        #print(self.hero.position)
        if action == "R":
            if self.dungeon_map[self.hero.position[0]][self.hero.position[1] + 1] != "▓":
                self.hero.position[1] += 1
        elif action == "L":
            if self.dungeon_map[self.hero.position[0]][self.hero.position[1] - 1] != "▓":
                self.hero.position[1] -= 1
        elif action == "D":
            if self.dungeon_map[self.hero.position[0] + 1][self.hero.position[1]] != "▓":
                self.hero.position[0] += 1
        elif action == "U":
            if self.dungeon_map[self.hero.position[0] - 1][self.hero.position[1]] != "▓":
                self.hero.position[0] -= 1
        elif action == "A":
            fighting = False
            for entity in self.entities:
                if tuple(self.hero.position) == entity.position:
                    if hasattr(entity, "attack"):
                        self.fight(entity)
                        fighting = True
            if not fighting:
                self.message ="Your big sword is hitting air really hard!"

        self.update_map(self.entities)

        if self.hero.hp < 1:
            self.message += "\nTHIS IS THE END"

    def place_entities(self, entities: list):
        #print(self.empty_space)
        position = random.sample(self.empty_space, len(entities))
        for idx, entity in enumerate(self.starting_entities):
            if entity == "goblin":
                self.entities.append(Goblin(identifier="\033[38;5;1mg\033[0;0m",
                                            position=position[idx], base_attack=-1,
                                            base_ac=0, damage=1))
        for entity in self.entities:
            self.dungeon_map[entity.position[0]][entity.position[1]] = entity.map_identifier

    def place_entities2(self, entities: list):
        #print(self.empty_space)
        for i in range(len(entities)):
            self.entities.append(Goblin(identifier="\033[38;5;1mg\033[0;0m",
                                            position=entities[i], base_attack=-1,
                                            base_ac=0, damage=1))
        for entity in self.entities:
            self.dungeon_map[entity.position[0]][entity.position[1]] = entity.map_identifier


    def update_map(self, entities: list):
        # TODO implement entities
        
        self.current_map = deepcopy(self.dungeon_map)
        self.current_map[self.hero.position[0]][self.hero.position[1]] = self.hero.map_identifier

    def fight(self, monster):
        hero_roll = self.hero.attack()
        monster_roll = monster.attack()
        if hero_roll["attack_roll"] > monster.base_ac:
            monster.hp -= hero_roll["inflicted_damage"]
            if monster.hp > 0:
                self.message = f"Hero inflicted {hero_roll['inflicted_damage']}"
            else:
                self.message = f"Hero Hero inflicted {hero_roll['inflicted_damage']} damage and slain {monster}"
                self.hero.gold += monster.gold
                self.hero.xp += 1
                self.dungeon_map[monster.position[0]][monster.position[1]] = "."
                self.entities.remove(monster)
        if monster_roll["attack_roll"] > self.hero.base_ac:
            self.message += f"\nMonster inflicted {monster_roll['inflicted_damage']} damage"
            self.hero.hp -= monster_roll['inflicted_damage']
            if self.hero.hp < 1:
                self.message += f"{self.hero.name} have been slained by {monster}"
        self.message += f"\nHero HP: {self.hero.hp}  Monster HP: {monster.hp}"
