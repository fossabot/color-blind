import time


def is_key_pressed(keys_pressed, symbol):
    return symbol in keys_pressed.keys() and keys_pressed[symbol] is not None


def get_pressed_duration(keys_pressed, symbol):
    duration = None
    for key, time_start in keys_pressed.items():
        if key == symbol and time_start is not None: 
            duration = time.time() - time_start
    return duration
