import math

def get_wave(text, amplitude, wavelength, reps):
    base = ""

    for i in range(math.ceil(reps*wavelength*math.pi)):
        base += " " * int(amplitude * (math.sin(i/wavelength)**2)) + f"{text}\n"

    return base

print(get_wave("hi", 40, 5, 2))