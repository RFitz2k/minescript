import minescript as ms
import sys

item1 = sys.argv[1]
operation = sys.argv[2]

item2 = sys.argv[3]

match operation:
    case "+":
        result = int(item1) + int(item2)
    case "-":
        result = int(item1) - int(item2)
    case "*":
        result = int(item1) * int(item2)
    case "/":
        result = int(item1) / int(item2)
ms.chat(f"{item1} {operation} {item2} = {result}")