import os
import time
import random

def random_choice(arr):
	return random.choice(arr)

def random_shuffle(arr):
	random.shuffle(arr)
	return arr

def clear_terminal():
	os.system('clear')

def set_pause(sec):
	time.sleep(20)

def play_signal_tact():
	duration = 0.15  # seconds
	freq = 200  # Hz
	os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))

#sudo apt install sox
def play_signal_end():
	duration = 0.25  # seconds
	freq = 110  # Hz
	os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))