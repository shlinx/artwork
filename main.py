import time
import os
from gpiozero import MotionSensor
from signal import pause

class artwork():

    def __init__(self, sensor_pin=4, led_pin=17):
        self.work_path = os.path.dirname(os.path.abspath(__file__))
        self.pir = MotionSensor(sensor_pin)
        self.count = int(time.time())
        self.pir.when_motion = self.on_when_motion
        self.pir.when_no_motion = self.on_when_no_motion
        print('Artwork is watching motions...')
        pause()

    def on_when_motion(self):
        self.count = int(time.time())
        print('Motion detected!')
        self.play_sound()
        self.control_led()
        print('\n')
    
    def on_when_no_motion(self):
        new_time = int(time.time())
        gap = new_time - self.count
        self.count = new_time
        self.control_led(False)
        print('Motion lost, lasted {gap} seconds.'.format(gap=gap))
        print('\n')

    def play_sound(self):
        os.system('mpg123 -q {file}'.format(file=self.work_path + '/audio.mp3'))

    def control_led(self, on=True):
        if on:
            print('LED on')
        else:
            print('LED off')

artwork()
