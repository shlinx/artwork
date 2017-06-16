import time
import os, sys
from gpiozero import MotionSensor
from gpiozero import LED
from signal import pause

AUDIOS = [
    'Waves & seagull.mp3'
]

sys.path.append(os.getcwd())

try:
    from settings import *
except ImportError:
    pass

class Artwork:
    work_path = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, sensor_pin=4, led_pin=17):
        self.pir = MotionSensor(sensor_pin)
        self.led = LED(led_pin)
        self.count = int(time.time())
        self.pir.when_motion = self.on_when_motion
        self.pir.when_no_motion = self.on_when_no_motion
        self.audio_file_index = 0
        print('Artwork is watching motions...')
        pause()

    def get_audio_file(self):
        current = os.path.join(self.work_path, 'audios', AUDIOS[self.audio_file_index])
        self.audio_file_index += 1
        return current

    def on_when_motion(self):
        self.count = int(time.time())
        print('Motion detected!')
        self.control_led()
        self.play_sound()
        self.control_led(on=False)
        print('\n')
    
    def on_when_no_motion(self):
        new_time = int(time.time())
        gap = new_time - self.count
        self.count = new_time
        print('Motion lost, lasted {gap} seconds.'.format(gap=gap))
        print('\n')

    def play_sound(self):
        os.system('mpg123 -q {}'.format(self.get_audio_file()))
        time.sleep(60)

    def control_led(self, on=True):
        if on:
            self.led.on()
        else:
            self.led.off()

Artwork()
