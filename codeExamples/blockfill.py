import minescript

x, y, z = minescript.player_position()

minescript.echo(f"My position: {x} {y} {z}")

minescript.execute(f"setblock {int(x)} {int(y)-1} {int(z)} diamond_block")