import RPG_MapEdit
import RPG_Arena

out_of_menu = False
while not out_of_menu:
    key = input('Welcome to Spellbook 0.0.1. What do you want to do ?')
    if key == '-EDITOR':
        out_of_menu = True
        RPG_MapEdit.main()
    elif key == '-GAME':
        out_of_menu = True
        RPG_Arena.main()
