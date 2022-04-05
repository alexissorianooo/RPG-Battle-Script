import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Person:
    power = "destruction"
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name=name
        self.max_hp=hp
        self.max_mp=mp
        self.hp=hp
        self.mp=mp
        self.atkL=atk - 10
        self.atkH=atk + 10
        self.df=df
        self.magic=magic
        self.actions=["Attack", "Magic", "Items"]
        self.items=items

    def generate_damage(self):
        return random.randrange(self.atkL, self.atkH)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp
    
    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_mp(self):
        return self.mp
    
    def get_max_mp(self):
        return self.max_mp

    def reduce_mp(self,cost):
        self.mp -= cost
    
    def choose_action(self):
        i = 1
        print("\n" +bcolors.BOLD+self.name+bcolors.ENDC)
        print(""+bcolors.OKBLUE + bcolors.BOLD + "ACTIONS:" + bcolors.ENDC)
        for item in self.actions:
            print("    "+str(i) + ".", item)
            i += 1
    
    def choose_magic(self):
        i = 1
        print("\n"+bcolors.OKBLUE + bcolors.BOLD + "MAGIC:" + bcolors.ENDC)
        for spell in self.magic:
            print("    "+str(i) + ".", spell.name, "(cost:", str(spell.cost) + ")")
            i += 1
    
    def choose_target(self, enemies):
        i = 1
        print("\n"+bcolors.FAIL +bcolors.BOLD + "TARGET:" + bcolors.ENDC)

        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("   "+str(i) +"."+ enemy.name)
                i += 1
        choice = int(input("    Choose Target:")) -1
        return choice
    
    def heal(self, heal):
        self.hp += heal
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        
    def choose_item(self):
        i = 1
        print("\n"+bcolors.OKBLUE + bcolors.BOLD + "ITEMS:" + bcolors.ENDC)
        for something in self.items:
            print("    "+str(i) + ".", something['itemName'].name, "-", something['itemName'].description, " (x"+str(something['quantity'])+")")
            i += 1
        '''
            something['itemName'].name

            something - accessing items in self.items
            *when access the system reads the name and the quantity

            ['itemName'] - refers to the value of the key "itemName", which is an object. 

            hence, '.name' is accessed 
        '''

    def get_enemy_stats(self):
        hp_bar = ""
        
        HPbar_ticks = ((self.hp/self.max_hp)*100)/2 #to make 50 "▌"
        
        while HPbar_ticks > 0:
            hp_bar+= "▌"
            HPbar_ticks -= 1
        
        while len(hp_bar) <50:
            hp_bar += " "


        HP_characters = str(self.hp)
        HP_total_characters = len(str(self.hp)) 
        HP_spaces = " "
        if len(HP_characters) < HP_total_characters:
            while len(HP_characters) < HP_total_characters:
                HP_characters = HP_spaces + HP_characters

        #for the undescores
        total_spaces = len(self.name +": "+HP_characters+"/"+str(self.max_hp)+" |")
        add_spaces = ""
        while len(add_spaces) != total_spaces:
            add_spaces+=" "

        print(add_spaces+"__________________________________________________")
        print(bcolors.BOLD + self.name +": "+HP_characters+"/"+str(self.max_hp)+" |" + bcolors.FAIL + hp_bar + bcolors.ENDC +"|")

        print("mp:", str(self.mp), "/", str(self.max_mp) )

    def get_stats(self):
        hp_bar = ""
        mp_bar = ""
        
        HPbar_ticks = ((self.hp/self.max_hp)*100)/4
        MPbar_ticks = ((self.mp/self.max_mp)*100)/10

        while HPbar_ticks > 0:
            hp_bar+= "▌"
            HPbar_ticks -= 1
        while len(hp_bar) < 25:
            hp_bar += " "

        while MPbar_ticks > 0:
            mp_bar += "▌"
            MPbar_ticks -= 1
        while len(mp_bar) < 10:
            mp_bar+=" "

        '''
        multiplied by 100 because we want to get the percentage 
        divided by 4, because we have 25 bars in HP
        
        '''
        HP_characters = str(self.hp)
        HP_total_characters = len(str(self.hp)) # 4, just to make it more dynamic
        HP_spaces = " "
        if len(HP_characters) < HP_total_characters:
            while len(HP_characters) < HP_total_characters:
                HP_characters = HP_spaces + HP_characters
            #     HP_spaces += " "
            # HP_characters = str(HP_spaces) + HP_characters
            
        MP_characters = str(self.mp)
        MP_spaces = " "
        if len(MP_characters) < 4:
            while len(MP_characters) < 4:
                MP_characters = MP_spaces + MP_characters
            


        print("                       _________________________             __________")
        print(bcolors.BOLD + self.name +": "+HP_characters+"/"+str(self.max_hp)+"   |" + bcolors.OKGREEN + hp_bar + bcolors.ENDC + bcolors.BOLD+"|  "+MP_characters+"/"+str(self.max_mp)+" |"+bcolors.OKBLUE+mp_bar+bcolors.ENDC+"|")

    def choose_enemy_spell(self):
        max_hp = self.get_max_hp()
        hp = self.get_hp()
        bar = max_hp * .2

        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg_enemy = spell.generate_dmg()

        if (self.get_mp() < spell.cost) or (spell.type == "White" and hp > bar):
            self.choose_enemy_spell()
        else:
            return spell, magic_dmg_enemy
