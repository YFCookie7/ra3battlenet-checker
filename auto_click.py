from pynput import keyboard

import pydirectinput

keys_pressed = set()
curr = "f1"
isPlaceMode = False


def on_press(key):
    global isPlaceMode
    if key == keyboard.KeyCode.from_char("`") and not isPlaceMode:
        pydirectinput.press(curr)
        print("Key pressed: `")
        isPlaceMode = True


def on_release(key):
    global isPlaceMode, curr

    if key == keyboard.KeyCode.from_char("`"):
        isPlaceMode = False
        pydirectinput.click()
        pydirectinput.keyDown("shift")
        pydirectinput.press("e")
        pydirectinput.keyUp("shift")

    elif str(key) == r"'\x11'":
        return False

    else:

        for i in range(1, 10):
            if key == getattr(keyboard.Key, f"f{i}"):
                curr = f"f{i}"
                print(f"Current key is {curr}")
                break


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
