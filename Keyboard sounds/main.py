from pynput.keyboard import Key, Listener
import winsound
import os


def on_press(key):
    sound_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vineboom.wav")
    winsound.PlaySound(sound_file, winsound.SND_ASYNC)


def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False


# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
