import minescript
import time
import threading
import random

PAUSE_KEY = 80 # P key

# COMMON KEY CODES:
# 32 = SPACE
# 49-57 = Numbers 1-9
# 65-90 = Letters A-Z
# 80 = P
# 256 = ESCAPE
# 257 = ENTER
# 258 = TAB
# 259 = BACKSPACE
# 340 = LEFT SHIFT
# 341 = LEFT CTRL
# Full list: https://www.glfw.org/docs/3.3/group__keys.html

ENABLE_MOB_KILLER = False # Set to True to enable mob killing during farming buggy on some farm like cooca bean farm bc of wood trapdoors not iron trapdoors

SLOT_SWITCH_DELAY = 0.5 # Delay after switching inventory slots (seconds)

HUB_DETECTION_ENABLED = True # Set to False to disable hub detection
HUB_CHAT_MESSAGE = "Sending to server" # Chat message that indicates server restart/hub teleport, modify if needed

AUTO_PAUSE_MESSAGES = [ # Messages to send when auto-pausing due to no inventory change, modify or add your own!
    "wth?", "whyy", "bruh", "brah", "Let me farm brah",
    "why.", "wth", "bruhhhh", "brahhh", "...bruhh",
    "Huh?", "C'mon man.", "Seriously?", "Brooo", "Ughhh",
    "Still here.", "Hello?", "What happened?",
    "This again?", "Oh, come on.", "For real?", "Again?"
]

FARM_PRESETS = { # Preset farm configurations you can customize or add your own
    "crops": { # Preset name, you can rename it to anything you want like uhh "sigma_farm_9000" or something
        "name": "Crops Farm (Sideways Drop)", # Display name of the farm, you can also rename it too
        "description": "Left/Right alternating with drops between layers", # Description of the farm pattern, and you can rename it too
        "rows": 1, # Actual rows determined by pattern length, and the more rows you want, the more times the pattern will repeat
        "warp_command": "/warp garden", # Command to warp to farm location, make sure you set your warp correctly
        "tool_slot": 0, # Inventory slot for the farming tool, and 0-8 corresponds to slots 1-9
        "snap_look_slot": 1, # Inventory slot for snap look item used to reset orientation after mob killing
        "vacuum_slot": 3, # Inventory slot for vacuum item used for mob killing, and yes i have it on slot 4 dont judge me.. too lazy to change..
        "reverse_pattern": True, # Whether to reverse the pattern directions (for mirrored farms)
        "has_drops": True, # Whether the farm requires drops between rows
        "pattern": [ # Movement pattern for harvesting rows, and if you put 1 on rows you can make a more complex pattern and it will repeat
            ('left', 1),
            ('right', 2),
            ('left', 3),
            ('right', 4),
            ('left', 5)
        ] #These are the movement patterns for each row.
          #And all the movements patterns are:
          #'right': 'left',
          #'forward': 'backward',
          #'diagonal-right-forward': 'diagonal-left-forward',
          #'diagonal-right-backward': 'diagonal-left-backward'
    },
    
    "crops_alt": { #crops alt if u want a horizontal farm without drops
        "name": "Crops Farm (Horizontal No-Drop)",
        "description": "Left -> Forward -> Right -> Forward (repeat), no drops",
        "rows": 8, #i dont got a horizontal so idk how many rows it has:sob emoji:
        "warp_command": "/warp garden",
        "tool_slot": 0,
        "snap_look_slot": 1,
        "vacuum_slot": 3,
        "reverse_pattern": False,
        "has_drops": False,
        "pattern": [
            ('left', 1),
            ('forward', 2),
            ('right', 3),
            ('forward', 4)
        ]
    },
    
    "sugar_cane": {
        "name": "Sugar Cane Farm",
        "description": "Hold Left, switch to Backward at wall",
        "rows": 1,
        "warp_command": "/warp garden",
        "tool_slot": 0,
        "snap_look_slot": 1,
        "vacuum_slot": 3,
        "reverse_pattern": False,
        "has_drops": False,
        "pattern": [
            ('left', 1),
            ('backward', 2),
            ('left', 3),    
            ('backward', 4),
            ('left', 5),
            ('backward', 6),
            ('left', 7),
            ('backward', 8),
            ('left', 9)
        ]
    },
    
    "cocoa": {
        "name": "Cocoa Bean Farm",
        "description": "Forward -> Left -> Backward -> Left (repeat)",
        "rows": 8,
        "warp_command": "/warp garden",
        "tool_slot": 0,
        "snap_look_slot": 1,
        "vacuum_slot": 3,
        "reverse_pattern": False,
        "has_drops": False,
        "pattern": [
            ('forward', 1),
            ('left', 2),
            ('backward', 3),
            ('left', 4)
        ]
    },
    
    "melon_pumpkin": {
        "name": "Melon/Pumpkin Farm",
        "description": "Right -> Forward -> Left -> Forward -> Right (repeat)",
        "rows": 6,
        "warp_command": "/warp garden",
        "tool_slot": 0,
        "snap_look_slot": 1,
        "vacuum_slot": 3,
        "reverse_pattern": False,
        "has_drops": False,
        "pattern": [
            ('right', 1),
            ('forward', 2),
            ('left', 3),
            ('forward', 4)
        ]
    },
    
    "mushroom": {
        "name": "Mushroom Farm",
        "description": "Hold Left+Forward -> Hold Backward -> Hold Right",
        "rows": 3,
        "warp_command": "/warp garden",
        "tool_slot": 0,
        "snap_look_slot": 1,
        "vacuum_slot": 3,
        "reverse_pattern": False,
        "has_drops": False,
        "pattern": [
            ('diagonal-left-forward', 1),
            ('backward', 2),
            ('right', 3)
        ]
    },
    
    "cactus": {
        "name": "Cactus Farm",
        "description": "Right -> Forward -> Left -> Forward -> Right (repeat)",
        "rows": 22,
        "warp_command": "/warp garden",
        "tool_slot": 0,
        "snap_look_slot": 1,
        "vacuum_slot": 3,
        "reverse_pattern": False,
        "has_drops": False,
        "pattern": [
            ('right', 1),
            ('forward', 2),
            ('left', 3),
            ('forward', 4)
        ]
    }
}

# Global state variables, do not modify if you don't know what you're doing

paused = False
detected_restart = False  # Flag for server restart detection

def check_pause():
    global paused
    if paused:
        minescript.echo("=== Farm PAUSED - Press configured key to resume ===")
        stop_all_movement()
        
        pause_start = time.time()
        while paused:
            time.sleep(0.1)
        
        pause_duration = time.time() - pause_start
        minescript.echo("=== Farm RESUMED ===")
        return pause_duration
    return 0

def stop_all_movement():
    minescript.player_press_left(False)
    minescript.player_press_right(False)
    minescript.player_press_forward(False)
    minescript.player_press_backward(False)
    minescript.player_press_attack(False)
    minescript.player_press_use(False)

def get_inventory_hash():
    inventory = minescript.player_inventory()
    inv_string = ""
    for item in inventory:
        inv_string += f"{item.item}:{item.count}:{item.slot}|"
    return inv_string

def smooth_look_at(target_x, target_y, target_z, steps=25, delay=0.02):
    import math
    
    player_data = minescript.player()
    px, py, pz = player_data.position
    current_yaw, current_pitch = minescript.player_orientation()
    
    dx = target_x - px
    dy = target_y - (py + 1.62)
    dz = target_z - pz
    
    horizontal_distance = math.sqrt(dx * dx + dz * dz)
    target_pitch = -math.degrees(math.atan2(dy, horizontal_distance))
    target_yaw = math.degrees(math.atan2(-dx, dz))
    
    def normalize_angle(angle):
        while angle > 180:
            angle -= 360
        while angle < -180:
            angle += 360
        return angle
    
    current_yaw = normalize_angle(current_yaw)
    target_yaw = normalize_angle(target_yaw)
    current_pitch = normalize_angle(current_pitch)
    target_pitch = normalize_angle(target_pitch)
    
    yaw_diff = target_yaw - current_yaw
    if yaw_diff > 180:
        yaw_diff -= 360
    elif yaw_diff < -180:
        yaw_diff += 360
    
    pitch_diff = target_pitch - current_pitch
    
    for i in range(1, steps + 1):
        progress = i / steps
        new_yaw = current_yaw + (yaw_diff * progress)
        new_pitch = current_pitch + (pitch_diff * progress)
        minescript.player_set_orientation(new_yaw, new_pitch)
        time.sleep(delay)

def kill_mobs(config):
    global detected_restart
    
    # Don't kill mobs if server restart was detected
    if detected_restart:
        return False
    
    if not ENABLE_MOB_KILLER:
        return False
    
    all_entities = minescript.entities(max_distance=15.0)
    armor_stands = [e for e in all_entities if "armor_stand" in e.type.lower()]
    bats = [e for e in all_entities if "bat" in e.type.lower()]
    
    if not armor_stands and not bats:
        return False
    
    player_data = minescript.player()
    px, py, pz = player_data.position
    
    all_mobs = armor_stands + bats
    mob = min(all_mobs, key=lambda e: 
        ((e.position[0]-px)**2 + (e.position[1]-py)**2 + (e.position[2]-pz)**2))
    
    minescript.echo(f"Targeting mob: {mob.type}")
    
    stop_all_movement()
    time.sleep(0.1)
    
    minescript.player_inventory_select_slot(config["vacuum_slot"])
    time.sleep(0.1)
    
    mob_x, mob_y, mob_z = mob.position
    smooth_look_at(mob_x, mob_y, mob_z, steps=25, delay=0.02)
    
    minescript.player_press_use(True)
    start_time = time.time()
    while time.time() - start_time < 3.0:
        all_entities = minescript.entities(max_distance=15.0)
        current_mobs = [e for e in all_entities if "armor_stand" in e.type.lower() or "bat" in e.type.lower()]
        
        if current_mobs:
            player_data = minescript.player()
            px, py, pz = player_data.position
            nearest = min(current_mobs, key=lambda e: 
                ((e.position[0]-px)**2 + (e.position[1]-py)**2 + (e.position[2]-pz)**2))
            mob_x, mob_y, mob_z = nearest.position
            smooth_look_at(mob_x, mob_y, mob_z, steps=4, delay=0.015)
        
        time.sleep(0.2)
    
    minescript.player_press_use(False)
    minescript.echo("Vacuumed mob!")
    
    minescript.player_inventory_select_slot(config["snap_look_slot"])
    time.sleep(SLOT_SWITCH_DELAY)
    minescript.player_press_attack(True)
    time.sleep(0.1)
    minescript.player_press_attack(False)
    minescript.echo("Used snap look item")
    
    minescript.player_inventory_select_slot(config["tool_slot"])
    time.sleep(SLOT_SWITCH_DELAY)
    
    return True

def reverse_direction(direction):
    opposites = {
        'left': 'right',
        'right': 'left',
        'forward': 'backward',
        'backward': 'forward',
        'diagonal-left-forward': 'diagonal-right-forward',
        'diagonal-right-forward': 'diagonal-left-forward',
        'diagonal-left-backward': 'diagonal-right-backward',
        'diagonal-right-backward': 'diagonal-left-backward'
    }
    return opposites.get(direction, direction)

def start_movement(direction):
    stop_all_movement()
    
    if direction == 'left':
        minescript.player_press_left(True)
    elif direction == 'right':
        minescript.player_press_right(True)
    elif direction == 'forward':
        minescript.player_press_forward(True)
    elif direction == 'backward':
        minescript.player_press_backward(True)
    elif direction == 'diagonal-left-forward':
        minescript.player_press_left(True)
        minescript.player_press_forward(True)
    elif direction == 'diagonal-right-forward':
        minescript.player_press_right(True)
        minescript.player_press_forward(True)
    elif direction == 'diagonal-left-backward':
        minescript.player_press_left(True)
        minescript.player_press_backward(True)
    elif direction == 'diagonal-right-backward':
        minescript.player_press_right(True)
        minescript.player_press_backward(True)

def harvest_row(direction, row_num, config):
    global paused, detected_restart
    
    if config.get("reverse_pattern", False):
        direction = reverse_direction(direction)
    
    minescript.echo(f"Row {row_num}: Moving {direction}")
    
    last_inventory = get_inventory_hash()
    last_inventory_change_time = time.time()
    
    start_movement(direction)
    time.sleep(0.05)
    
    minescript.player_press_attack(True)
    time.sleep(0.05)
    
    player_data = minescript.player()
    last_x, last_z = player_data.position[0], player_data.position[2]
    stuck_counter = 0
    
    while True:
        # Check if server restart was detected
        if detected_restart:
            stop_all_movement()
            return
        
        time.sleep(0.1)
        
        if kill_mobs(config):
            time.sleep(0.1)
            start_movement(direction)
            time.sleep(0.05)
            minescript.player_press_attack(True)
            time.sleep(0.05)
            stuck_counter = 0
            last_inventory_change_time = time.time()
            continue
        
        pause_duration = check_pause()
        if pause_duration > 0:
            last_inventory_change_time += pause_duration
            start_movement(direction)
            time.sleep(0.05)
            minescript.player_press_attack(True)
            time.sleep(0.05)
            stuck_counter = 0
        
        current_inventory = get_inventory_hash()
        if current_inventory != last_inventory:
            last_inventory = current_inventory
            last_inventory_change_time = time.time()
        
        time_since_change = time.time() - last_inventory_change_time
        if time_since_change > 2.0:
            minescript.echo(f"Inventory hasn't updated for 2 seconds on row {row_num}")
            random_message = random.choice(AUTO_PAUSE_MESSAGES)
            minescript.chat(random_message)
            minescript.echo("=== Auto-paused: Press configured key to resume ===")
            
            stop_all_movement()
            paused = True
            
            while paused:
                time.sleep(0.1)
            
            last_inventory_change_time = time.time()
            last_inventory = get_inventory_hash()
            minescript.echo(f"Resuming row {row_num}")
            
            start_movement(direction)
            time.sleep(0.05)
            minescript.player_press_attack(True)
            time.sleep(0.05)
            stuck_counter = 0
            continue
        
        player_data = minescript.player()
        current_x, current_z = player_data.position[0], player_data.position[2]
        distance_moved = abs(current_x - last_x) + abs(current_z - last_z)
        
        if distance_moved < 0.01:
            stuck_counter += 1
            if stuck_counter >= 2:
                minescript.echo(f"Hit wall on row {row_num}")
                break
        else:
            stuck_counter = 0
        
        last_x, last_z = current_x, current_z
    
    stop_all_movement()
    time.sleep(0.1)
    minescript.echo(f"Row {row_num} complete")

def drop_to_next_row(row_num):
    minescript.echo(f"Dropping to row {row_num + 1}")
    check_pause()
    time.sleep(0.1)

def run_farm(config):
    global paused, detected_restart
    
    minescript.echo(f"=== {config['name']} Started ===")
    minescript.echo(f"Description: {config.get('description', 'N/A')}")
    minescript.echo(f"Press key code {PAUSE_KEY} to PAUSE/RESUME")
    minescript.echo(f"Rows/Layers: {config['rows']}")
    minescript.echo(f"Mob Killer: {'Enabled' if ENABLE_MOB_KILLER else 'Disabled'}")
    minescript.echo(f"Hub Detection: {'Enabled' if HUB_DETECTION_ENABLED else 'Disabled'}")
    minescript.echo(f"Reverse Pattern: {'Yes' if config.get('reverse_pattern', False) else 'No'}")
    
    event_queue = minescript.EventQueue()
    event_queue.register_key_listener()
    
    # Register chat listener for server restart detection
    if HUB_DETECTION_ENABLED:
        event_queue.register_chat_listener()
    
    run_count = 0
    
    def check_key_events():
        global paused, detected_restart
        while True:
            try:
                event = event_queue.get(block=False)
                if event.type == "key":
                    if event.key == PAUSE_KEY and event.action == 1:
                        paused = not paused
                elif event.type == "chat":
                    # Check for server restart message
                    if HUB_CHAT_MESSAGE in event.message:
                        minescript.echo("=== SERVER RESTART DETECTED! ===")
                        minescript.echo("=== Farm will stop. ===")
                        detected_restart = True
            except:
                pass
            time.sleep(0.05)
    
    key_thread = threading.Thread(target=check_key_events, daemon=True)
    key_thread.start()
    
    while True:
        # Check if server restart was detected
        if detected_restart:
            stop_all_movement()
            minescript.echo("=== Farm stopped due to server restart. ===")
            return
        
        run_count += 1
        check_pause()
        
        minescript.echo(f"=== Starting run #{run_count} ===")
        
        for run in range(config['rows']):
            # Check if server restart was detected
            if detected_restart:
                stop_all_movement()
                minescript.echo("=== Farm stopped due to server restart. ===")
                return
            
            for i, (direction, row_num) in enumerate(config['pattern']):
                # Check if server restart was detected
                if detected_restart:
                    stop_all_movement()
                    minescript.echo("=== Farm stopped due to server restart. ===")
                    return
                
                check_pause()
                
                harvest_row(direction, row_num, config)
                
                if config.get('has_drops', False) and i < len(config['pattern']) - 1:
                    drop_to_next_row(row_num)
        
        check_pause()
        minescript.echo(f"=== Run #{run_count} complete! Teleporting back ===")
        time.sleep(0.1)
        
        minescript.execute(config['warp_command'])
        time.sleep(0.1)

def main():
    import sys
    
    if len(sys.argv) < 2:
        minescript.echo("=== Available Farms ===")
        for key, config in FARM_PRESETS.items():
            minescript.echo(f"  \\multi_farm_system {key}")
            minescript.echo(f"    {config['description']}")
            minescript.echo(f"    Rows: {config['rows']}, Drops: {config.get('has_drops', False)}")
            minescript.echo("")
        minescript.echo("Usage: \\multi_farm_system [farm_type]")
        minescript.echo("Example: \\multi_farm_system crops")
        minescript.echo("")
        minescript.echo("=== Configuration ===")
        minescript.echo(f"Pause Key Code: {PAUSE_KEY}")
        minescript.echo(f"Mob Killer: {'Enabled' if ENABLE_MOB_KILLER else 'Disabled'}")
        minescript.echo(f"Hub Detection: {'Enabled' if HUB_DETECTION_ENABLED else 'Disabled'}")
        minescript.echo(f"Slot Switch Delay: {SLOT_SWITCH_DELAY}s")
        minescript.echo("Edit top of script to change settings!")
        return
    
    farm_type = sys.argv[1].lower()
    
    if farm_type not in FARM_PRESETS:
        minescript.echo(f"Error: Unknown farm type '{farm_type}'")
        minescript.echo("Available types: " + ", ".join(FARM_PRESETS.keys()))
        return
    
    config = FARM_PRESETS[farm_type]
    run_farm(config)

if __name__ == "__main__":
    main()