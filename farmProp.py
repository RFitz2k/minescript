# final farming thingy:
import sys
import minescript as ms
import minescript_plus as msp
import time
# feed program which crop to farm, check every piece of armor/accessory/tool for currently equipped and equip everything for that crop
# tp to garden, walk to start of farm, orientate, set speed on farmers boots and start farming
#for this, need to know how to do:
# - input for crop type
    #make a calculator
crop = sys.argv[1]
# - check what armor/accessory/tool is equipped in each slot
    #book crafter
# - create array for each type of equipment
    #pretty much the only reason for this
# - equip best piece of equipment for each slot
    #also book crafter
# - tp to garden
    #ms.execute("/warp garden")
# - walk to start of farm
    #walk to nearby entities
# - set farmer boots speed
    #edit signs?
# - get player orientation
# - set player orientation