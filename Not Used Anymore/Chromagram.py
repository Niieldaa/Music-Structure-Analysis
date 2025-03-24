from pydub import AudioSegment
from pydub.playback import play

# Load and play FLAC file
filename = r"C:\Users\nield\Desktop\GitHub\Music-Structure-Analysis\DO NOT TOUCH\Audio Files\Emmanuel\01. Vitalic - Polkamatic.flac"
audio = AudioSegment.from_file(filename, format="flac")
play(audio)
