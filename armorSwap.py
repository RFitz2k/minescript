import minescript as ms
import minescript_plus as msp
import slotFinder as sF


listy = [10,11,12,13]

ms.press_key_bind("key.inventory", True)

item = "minecraft:leather_helmet"

msp.Inventory.click_slot(sF.find_item(item))



def actual():
    for i in range(len(listy) -1):
        msp.Inventory.click_slot(listy[i])
        ms.echo("clicked", listy[i])
        msp.Inventory.click_slot(listy[i]+26)
        ms.echo("clicked", listy[i]+26)