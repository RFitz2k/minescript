from utils import items
from minescript import echo
import minescript_plus as msp

def remapCheck():
    slot = items.find_item("minecraft:leather_boots")

    echo("msp found at pos", slot)

    newSlot = items.click_inv_remap(slot)

    echo("remapped slot at pos", newSlot)

def slot_identify():
    echo("item is at slot", items.find_item("minecraft:leather_boots"))

slot_identify()