import minescript as ms
import time

quan = ms.player_inventory()




while (bool(quan)):
    i = len(quan) - 1
    print (len(quan))
    print (quan[i].item, quan[i].nbt, quan[i].slot)
    quan.pop()

