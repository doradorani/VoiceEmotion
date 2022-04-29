from pydub import AudioSegment
import matplotlib.pyplot as plt
import scipy.fftpack
import scipy.io.wavfile
import numpy as np
 
 
def print_wavfile_info(filepath):
    wav = AudioSegment.from_wav(filepath)
 
    # 샘플레이트(44100... 24000... 8000...등)
    print(wav.frame_rate)
 
    # 샘플의 바이트수 1은 8비트, 2는 16비트.(비트레이트)
    print(wav.sample_width)
 
    # 프레임의 바이트수. channel * 샘플의바이트수가 됨. 채널은 1은 모노, 2는 스테레오
    print(wav.frame_width)
    
print(print_wavfile_info('tmp/1651063837309.wav'))



def wavfile_bitrate_change(filepath, bitrate):
    wav = AudioSegment.from_wav(filepath)
    wav = wav.set_sample_width(sample_width=bitrate)
    wav.export(filepath, format='wav')
    print(wav.sample_width)
    
    
print(wavfile_bitrate_change('tmp/1651063837309.wav', 2))