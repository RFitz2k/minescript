import minescript as ms


ms.echo("Hello, World!")
ms.chat("This is a test message.")
ms.execute("/tp @s 100 64 100")
name = ""
ms.sleep(1000)
name = ms.player_name()
ms.echo(f"Player name: {name}")