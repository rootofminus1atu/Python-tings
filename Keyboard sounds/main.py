import tkinter as tk
import simpleaudio as sa
from pynput import keyboard


class App:
    def __init__(self, master):
        self.master = master
        self.sound = sa.WaveObject.from_wave_file('vineboom.wav')

        self.state = False
        self.button = tk.Button(self.master, text="Start Listening", command=self.toggle_state)
        self.button.pack(pady=20)

        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def toggle_state(self):
        self.state = not self.state
        if self.state:
            self.button.config(text="Stop Listening")
        else:
            self.button.config(text="Start Listening")

    def on_press(self, key):
        if self.state:
            self.sound.play()

    def close(self):
        self.listener.stop()
        self.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("300x200")
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()

