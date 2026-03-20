import minescript as ms
import minescript_plus as msp
import utils
import time

x=0
armorSlots = [5,6,7,8]

items = ["minecraft:leather_helmet", 
         "minecraft:leather_chestplate",
         "minecraft:leather_leggings",
         "minecraft:leather_boots"
        ]

ms.press_key_bind("key.inventory", True)


time.sleep(2)

try:
        for i in items:
                ms.echo("finding ", i)

                slot = msp.Inventory.find_item(i)

                ms.echo("msp slot for ", i, " is ", slot)

                time.sleep(1)

                newSlot = utils.items.click_inv_remap(slot)

                ms.echo("my slot is ", newSlot)

                msp.Inventory.click_slot(newSlot)

                time.sleep(1)
                msp.Inventory.click_slot(armorSlots[x])
                x += 1
except:
        ms.echo("i shidded :(")






