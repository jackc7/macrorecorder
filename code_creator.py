import pickle
import time

def get_data():
    with open("recording", "rb") as recording:
        return pickle.load(recording)
    
def creator():
    strokes = get_data()
    total_time = get_data()[-1]["timestamp"]
    special_keys = {
        "Key.shift": "'shift'",
        "Key.ctrl_l": "'left_ctrl'",
        "Key.space": "' '",
        "Key.tab": "'tab'",
        "Key.alt_l": "'left_alt'",
        "Key.shift_r": "'right_shift'",
        "Key.alt_r": "'right_alt'",
        "Key.down": "'down'",
        "Key.up": "'up'",
        "Key.left": "'left'",
        "Key.right": "'right'"
    }
    
    code = f"""
# Execution Time: {round(total_time, 2)}s
import keyboard
import time

keyboard.wait("enter")


"""
    
    ti = time.time()
    
    send_up = lambda keyname : f"keyboard.send({keyname}, do_press=False)\n"
    send_down = lambda keyname : f"keyboard.send({keyname}, do_release=False)\n"

    for i, key in enumerate(strokes):
        key_name = key["key"]
        
        try:
            next_timestamp = strokes[i+1]["timestamp"]
        except IndexError:
            send_up(key_name)
            continue

        if key_name in special_keys:
            try:
                key_name = special_keys[key_name]
            except KeyError:
                print(f"{key_name} is not in special_keys list, you'll need to fix it")
        
        # uppercase = key_name.isupper()
        key_name = key_name.lower()
        
        # if uppercase:
            # code += send_down("'left_shift'")
            
        if key["motion"] == "up":
            code += send_up(key_name)
        elif key["motion"] == "down":
            code += send_down(key_name)
            
        code += f"time.sleep({next_timestamp - key['timestamp']})\n"
        
        # if uppercase:
        #     code += send_up("'left_shift'")
        
    with open("output.py", "w") as file:
        file.write(code)

creator()