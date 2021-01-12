from pynput import keyboard
from pprint import pprint

import pickle
import time
import sys

sys.tracebacklimit = 0
    
def on_press(key):
    print(str(key))
    if key == keyboard.Key.pause:
        return False
    if key == keyboard.Key.delete:
        global restart
        restart = True
    if key in currently_down:
        return

    currently_down.add(key)
    
    new_entry = {
        "key": str(key),
        "motion": "down",
        "timestamp": stopwatch()
    }
    
    record.append(new_entry)

def on_release(key):
    if key not in currently_down:
        return
    
    currently_down.remove(key)
    
    new_entry = {
        "key": str(key),
        "motion": "up",
        "timestamp": stopwatch()
    }
    
    record.append(new_entry)
        
def save_recording(recording):
    with open("recording","wb") as file:
        pickle.dump(recording, file)

def setup():
    print("Recording Started - Press pause/break to save it or del to restart.")
    while not restart:
        listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release)
        listener.join()

    if restart:
        return
    
    save_recording(record)
    pprint(record)
    exit()

if __name__ == "__main__":
    while True:
        restart = False
        record = []
        currently_down = set()
        ti = time.time()
        stopwatch = lambda: time.time() - ti
        setup()