from pydub import AudioSegment
from pydub.generators import Sine

duration = 500  # milliseconds
frequency = 440  # Hz
amplitude = 0.5  # 0.0 - 1.0

beep = Sine(frequency).to_audio_segment(duration=duration).apply_gain(amplitude * 100)

beep.export("beep.wav", format="wav")
