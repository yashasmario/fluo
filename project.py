import numpy as np
from numpy.fft import fft, fftfreq
from pydub import AudioSegment
from rich.console import Console
from rich import print as rprint
import os
import re

class fluo():
    def __init__(self, bars:int = 10, fps:int = 60):
        self.bars = bars
        self.fps = fps
        self.console = Console()
        self.duration = None
        self.data = None
    
    #Audio Processing
    def load_audio(self, audio_path:str, start=0, duration:float= 10.00, mono= False):
        duration = round(duration, 2)
        start = round(start, 2)
        audio_file = AudioSegment.from_file(audio_path)

        if mono == False:
            audio_file = audio_file.setchannels(1)

        audio_file = audio_file[start*1000, (start+duration)*1000]

        self.path = audio_path
        self.duration = duration
        self.start = start

        return audio_file

    def get_fft_data(self, audio_file):
        #get audio data
        audio_samples = np.array(audio_file.get_array_of_samples())
        audio_samplerate = audio_file.frame_rate
        
        #fft algorithm
        fft_data = fft(audio_samples)
        rprint(type(fft_data))
        audio_frequencies = fftfreq(len(audio_samples), 1/audio_samplerate)
        
       # modify amplitude data for the visualizer, volume meter, etc (convert arrays from complex domain to real by taking the absolute values)
        magnitude = np.abs(fft_data)
        magnitude = np.max(magnitude) #normalize the magnitude
        pos_index = audio_frequencies >= 0

        self.fft = (audio_frequencies[pos_index], magnitude[pos_index])
        
        return audio_frequencies[pos_index], magnitude[pos_index]

    def playlist(self, *paths:str, fade:float= 0):
        #initializes every audio
        playlist =  AudioSegment.empty()
        fade = round(fade, 2)

        for audio_path in paths:
            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            #dictionary for better playlist management or js add it all together
            try:
                audio = AudioSegment.from_file(audio_path)
                if fade > 0:
                    audio = audio.fade_in(fade).fade_out(fade)
                playlist += audio
                rprint(f"Successfully added file: {audio_path} \n")
            except FileNotFoundError:
                rprint(f"!File not found: {audio_path} \n")
            except Exception as e:
                rprint(f"Error loading file: {e} \n")
    

    #Rendering/Visualizing with rich
    def render_bars(self):
        ...

    def render_waveform(self):
        frequencies, magnitude = self.fft


#-------------------------------------------------------------------------------------------------------------------------
# cli functions

def cli_get_audio():
#use rich to add in line arguments passing or sys
    while True:
        try:
            audio_path = input("audio file path: ")
            audio_file = AudioSegment.from_file(audio_path)
            rprint("Successfully found audio file!")
            break
        except FileNotFoundError:
            rprint("File not found!")
            continue

def main():
    audio = fluo()
    audio.load_audio("krabbypatty.mp3")
    print(audio.path)

if __name__ == "__main__":
    main()
