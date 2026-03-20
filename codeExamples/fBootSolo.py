import minescript as ms
import utils as hf
import time
from lib_sign import Sign
import sys

crop = sys.argv[1] if len(sys.argv) > 1 else ms.echo("Please specify a crop, setting speed to 400.")  # gets a crop from input, defaults to echoing a message and setting speed to 400 if no crop is provided
boots = hf.farmersBoots() 
speed = boots.set_speed(crop)

ms.player_press_use(True)
ms.player_press_use(False)

time.sleep(1)  # wait for sign GUI

if Sign.write(speed, .01, .02, True, True):
    while Sign.is_writing():
        time.sleep(0.05)
# code to set the speed of the farmer's boots goes here, using the value of speed