import minescript as ms
from minescript_plus import Inventory as msp
import time

slot = -1
item = "minecraft:leather_helmet"

inv = ms.player_inventory()
#Hotbar: Left right 0-8

#Inventory: topleft to bottom right 9-35

#armor: boots, leggings, chestplate, helmet 36-39

#with chest open: inventory gets added to chest slots, then hotbar

def find_item(item): #returns the slot of the first instance of the item in the player's inventory, or prints that it was not found
    if (slot := msp.find_item(item)): #uses minescript_plus to find the item in the player's inventory, sets slot to the slot number if found
        print("Found item in inventory in slot", slot) 
        return slot
    else:    
        print("Item not found in inventory")
        return -1

def check_slot(slot): #checks the specified slot for an item and prints the item and its nbt data if found, or that no item was found if the slot is empty
    global found #playing with global variables here, not the best practice but it works for this simple script
    found = False #reset found to false before checking the slot
    inv = ms.player_inventory() #refresh inventory data, player_inventory() returns a stack of item objects with item, nbt, and slot attributes
    for i in inv: #for each item (i) in the inventory stack
        if i.slot == slot: #if the items slot matches the check slot, print the item and its nbt data, set found to true, and break the loop
            print("Found item in slot", slot, ":", i.item, i.nbt)
            found = True
            break
    if not found:
        print("No item found in slot", slot)


        
        
    

slot = find_item(item)

