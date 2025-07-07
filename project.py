import numpy as np
from numpy.fft import fft, fftfreq
from pydub import AudioSegment
from rich.console import Console
from rich import print as rprint

class fluo():
    def __init__(self, bars:int = 10, fps:int = 60):
        self.bars = bars
        self.fps = fps
        self.console = Console()
        self.duration = None
        self.data = None
    
    # Program functions
    def initialize(self):
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
        self.path = audio_path
        return audio_file

    def live_input(self):
        ...
    def transform(self, audio_file):
        #get audio data
        audio_samples = AudioSegment.get_array_of_samples(audio_file)
        audio_samplerate = audio_file.frame_rate
        
        #fft algorithm
        fft_data = fft(audio_samples)
        rprint(type(fft_data))
        audio_frequencies = fftfreq(len(audio_samples), 1/audio_samplerate)
        
       # modify amplitude data for the visualizer, volume meter, etc (convert arrays from complex domain to real by taking the absolute values)
        magnitude = np.abs(fft_data)
        positive_frequency_index = audio_frequencies >= 0
        
        return audio_frequencies[positive_frequency_index], magnitude[positive_frequency_index]
        
    def visualize(self, audio_frequencies, magnitude):
        #visualize the data using rich
        self.console.clear()
        self.console.print("Visualizing audio data...")
    
    # Library functions
    def bar(self):
        ...
    def fspec(self):
        ...

def main():
    audio = fluo()
    audio.initialize()
    print(audio.path)

if __name__ == "__main__":
    main()
