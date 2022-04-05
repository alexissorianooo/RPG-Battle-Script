from re import I
from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

#Black Magic
fire = Spell("Fire", 25, 190, "Black")
thunder = Spell("Thunder", 29, 230, "Black")
blizzard = Spell("Blizzard", 26, 200, "Black")
meteor = Spell("Meteor", 36, 300, "Black")
tornado = Spell("Tornado", 30, 240, "Black")

#White Magic
cure = Spell("Cure", 22, 320, "White")
quraa = Spell("Quraa", 28, 500, "White")

#magic list
player_magic=[fire, thunder, blizzard, meteor, tornado, cure, quraa]
enemy_magic=[fire, thunder, blizzard, cure]


#Creating ITEMS
potion=Item("Potion", "potion", "Heals for 150 HP", 150)
hipotion=Item("Hi-Potion", "potion", "Heals for 200 HP", 200)
simppotion=Item("SIMP-Potion", "potion", "Heals for 600 HP", 600)
elixir=Item("Elixir", "elixir", "Fully Restores HP/MP of one party member", 9999)
megaelixir=Item("MegaElixir", "elixir", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

#item list
player_items= [{"itemName": potion, "quantity": 15}, {"itemName": hipotion, "quantity": 5}, 
                {"itemName": simppotion, "quantity": 5}, {"itemName": elixir, "quantity": 5}, 
                {"itemName": megaelixir, "quantity": 5}, {"itemName": grenade, "quantity": 5}]

#Chracter Creation
player1 = Person("Alexis  ",4460, 150, 150, 100, player_magic, player_items)
player2 = Person("Lawrence",4460, 100, 110, 150, player_magic, player_items)
player3 = Person("Ysabella",4460, 100, 100, 100, player_magic, player_items)


enemy1 = Person("Teostra ",1200, 300, 540, 25, enemy_magic, [])
enemy2 = Person("Imp     ",1200, 100, 600, 25, enemy_magic, [])
enemy3 = Person("Imp     ",1200, 100, 600, 25, enemy_magic, [])

players_list = [player1, player2, player3]
enemy_list = [enemy2, enemy1, enemy3]

running = True
i=0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("======================================")

    print("\n")
    print("NAME                   HP                                 MP")
    for player in players_list:
        player.get_stats()
        
        # print("Getting attribute.. " + getattr(player, 'name'))

    print("\n")

    for enemy in enemy_list:
        enemy.get_enemy_stats()
    
    for player in players_list:
        player.choose_action()
        choice = input("Choose action: ")
        index = int(choice)-1

        if index == 0:
            dmg = player.generate_damage()
            
            enemy = player.choose_target(enemy_list)
            enemy_list[enemy].take_damage(dmg)

            #deleting dead enemy
            if enemy_list[enemy].get_hp() == 0:
                print(enemy_list[enemy].name.replace(" ", "")+" has died.")
                del enemy_list[enemy]
            print("\n", player.name.replace(" ", ""), "attacked", enemy_list[enemy].name.replace(" ", ""),"for", dmg, "points of damage.")
        #----------------MAGIC SECTION------------------
        elif index == 1:
            player.choose_magic()
            magic_choice= int(input("Choose magic: "))-1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_dmg()
            
            if spell.cost > player.get_mp():
                print(bcolors.FAIL + "\n Not enough MP" + bcolors.ENDC)
                continue
            
            player.reduce_mp(spell.cost)

            if spell.type == "White":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg) + bcolors.ENDC)
            elif spell.type == "Black":
                enemy = player.choose_target(enemy_list)
                enemy_list[enemy].take_damage(magic_dmg)

                #deleting dead enemy
                if enemy_list[enemy].get_hp() == 0:
                    print(enemy_list[enemy].name.replace(" ", "")+" has died.")
                    del enemy_list[enemy]

                print(bcolors.OKBLUE + "\n", player.name.replace(" ", ""), " casted", spell.name, "magic, dealt", magic_dmg, "damage points to", str(enemy_list[enemy].name.replace(" ", "")) + bcolors.ENDC)
    #----------------ITEM SECTION------------------
        elif index ==2:
            player.choose_item()
            item_choice = int(input("Choose item: "))-1

            if item_choice == -1:
                continue

            item = player.items[item_choice]['itemName']

            if player.items[item_choice]['quantity'] == 0:
                print(bcolors.FAIL + "\n" + "None left.. " + bcolors.ENDC)
                continue
        
            player.items[item_choice]['quantity'] -= 1
            
            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop) + bcolors.ENDC)
            elif item.type == "elixir":
                if item.name == "MegaElixir":
                    for i in players_list:
                        i.hp = i.max_hp
                        i.mp = i.max_mp
                else:
                    player.hp = player.max_hp
                    player.mp = player.max_mp
                print(bcolors.OKGREEN + "\n" + item.name + "fully restored "+player.name.replace(" ", "")+" HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemy_list)
                enemy_list[enemy].take_damage(item.prop)

                #deleting dead enemy
                if enemy_list[enemy].get_hp() == 0:
                    print(enemy_list[enemy].name.replace(" ", "")+" has died.")
                    del enemy_list[enemy]
                print(bcolors.FAIL + "\nYou used " + item.name + " and dealt ", str(item.prop), " points of damage to", str(enemy_list[enemy].name.replace(" ", "")) + bcolors.ENDC)

            '''
                item = player.items[item_choice]['itemName']
                item.type
                example: item_choice = 1; potion

                player.items[item_choice] - refers to the position of the key and value in the dictionary, in this case the 0th position:
                    {"itemName": potion, "quantity": 15}

                ['itemName'] - refers to the key to retrieve the value, in this case:
                    "itemName": potion

                .type - since the value of the "itemName" is an object, this makes the class attributes accessible, in this case
                    .type = "potion"
                    .name = "Potion"
                    .prop = 50
            '''

    #=====enemy attack phase=====
    
    for enemy in enemy_list:

        enemy_choice = random.randrange(0,2)

        if enemy_choice == 0:
            target = random.randrange(0, len(players_list))
            enemy_dmg= enemy.generate_damage()

            players_list[target].take_damage(enemy_dmg)


            print(bcolors.FAIL + " Enemy", enemy.name.replace(" ", ""),"attacks "+players_list[target].name.replace(" ", "")+" for", enemy_dmg, "damage points." + bcolors.ENDC)

            #deleting dead player
            if players_list[target].get_hp() == 0:
                print(players_list[target].name.replace(" ", "")+" has died.")
                del players_list[target]

        elif enemy_choice == 1:
            target = random.randrange(0, len(players_list))
            spell,magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            
            if spell.type == "Black":
                players_list[target].take_damage(magic_dmg)
                print(bcolors.FAIL + " Enemy", enemy.name.replace(" ",""), "casted", spell.name, "dealt", str(magic_dmg), "to", players_list[target].name.replace(" ", "") + bcolors.ENDC)
                
                #deleting dead player
                if players_list[target].get_hp() == 0:
                    print(players_list[target].name.replace(" ", "")+" has died.")
                    del players_list[target]
            elif spell.type == "White":
                enemy.heal(magic_dmg)
                print(bcolors.WARNING + "\n" + spell.name + " heals", enemy.name.replace(" ", ""), "for", str(magic_dmg) + bcolors.ENDC)
            
        









    # checks if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemy_list:
        if enemy.get_hp() == 0:
            defeated_enemies += 1
    
    for player in players_list:
        if player.get_hp() == 0: 
            defeated_players += 1

    if defeated_enemies == 3:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif defeated_players == 3:
        print(bcolors.FAIL +"YOUR TEAM DIED" + bcolors.ENDC)
        running = False
