import minescript as ms
import random
import time
from lib_sign import Sign

class General:
    def random_delay(self, time):
        "returns a random delay between a tenth and 1.5 times the provided time in seconds"
        return random.uniform(time*.1, time*1.5)
    
class farmersBoots:
    def set_speed(self, crop):
        "sets the speed of the farmer's boots based on the crop being farmed"
        if crop == "wart":
            speed = "371"
        elif crop == "cane":
            speed = "320"
        elif crop == "cac":
            speed = "100"
        else:
            speed = "400" # default speed for unknown crops
        
        return speed
        # code to set the speed of the farmer's boots goes here
    
    def set_boots(self, crop): #function to set speed on boots (for use in farmProp)
        speed = self.set_speed(crop)

        ms.player_press_use(True) #open boots sign gui
        ms.player_press_use(False)

        time.sleep(1)  # wait for sign GUI

        if Sign.write(speed):
            while Sign.is_writing():
                time.sleep(0.05)
