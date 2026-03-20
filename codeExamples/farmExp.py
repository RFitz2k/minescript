import minescript as ms

crop = "cane"  # Example crop, can be "cane", "wheat", or "carrot"
def farmer(crop):
    if crop == "cane":
        return 10, 10
    if crop == "wheat":
        return 20, 20
    if crop == "carrot":
        return 30, 30

yaw, pitch = ms.player_orientation()

ms.echo(f"Player orientation: {yaw}, {pitch}")

yaw, pitch = farmer(crop)

ms.player_set_orientation(yaw, pitch)