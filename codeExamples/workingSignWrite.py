import minescript as ms
import time
from lib_sign import Sign

ms.player_press_use(True)
ms.player_press_use(False)

time.sleep(1)  # wait for sign GUI

if Sign.write("Testing sign writing", .01, .02, True):
    while Sign.is_writing():
        time.sleep(0.05)