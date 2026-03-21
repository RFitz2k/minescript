import minescript as ms
import minescript_plus as msp
import random
import time
from lib_sign import Sign

class General:
    def random_delay(self, time):
        "returns a random delay between a tenth and 1.5 times the provided time in seconds"
        return random.uniform(time*.1, time*1.5)
    def write_out(f, data):
        "abc"

        

class items:
    def check_slot(slot): #checks the specified slot for an item and prints the item and its nbt data if found, or that no item was found if the slot is empty
        found = False #reset found to false before checking the slot
        inv = ms.player_inventory() #refresh inventory data, player_inventory() returns a stack of item objects with item, nbt, and slot attributes
        for i in inv: #for each item (i) in the inventory stack
            if i.slot == slot: #if the items slot matches the check slot, print the item and its nbt data, set found to true, and break the loop
                print("Found item in slot", slot, ":", i.item, i.nbt)
                found = True
                break
        if not found:
            print("No item found in slot", slot)
        
    def base_inv_click_remap(slot):

        #msp.inventory.find_item returns:
        #Hotbar: Left right 0-8
        #Inventory: topleft to bottom right 9-35
        #armor: boots, leggings, chestplate, helmet 36-39
        #with chest open: inventory gets added to chest slots, then hotbar

        #msp.inventory.click_slot in survival uses:
        #0-4: crafting interface
        #5-8: armor slots
        #9-35: inventory
        #36-44: hotbar
        #45: offhand

        r = 0  # rebound slot

        if slot is not None:  # safer than if(slot)
            if slot in range(0, 9):
                r = slot + 36
                return r
            elif slot in range(36, 40):
                r = 44 - slot
                return r
            else: #im too lazy to include offhand :P
                ms.echo("slot not found")
                return slot
        else:
            ms.echo("not a slot")
            return False
    def click_chest_remap(slot):
        if slot < 9:
            slot = slot + 81
        else:
            slot = slot + 45
        return slot
