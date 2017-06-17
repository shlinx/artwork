import time
import os
import sys
from gpiozero import MotionSensor
from gpiozero import LED
from signal import pause

AUDIOS = [
    'Waves & seagull.mp3'
]

LED_PINS = [
    17, 21, 22,
]

LED_COLORS = [
    [17],
    [21],
    [22],
    [17, 21],
    [17, 22],
    [21, 22],
    [17, 21, 22]
]

sys.path.append(os.getcwd())

try:
    from settings import *
except ImportError:
    pass


class Artwork:
    work_path = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, sensor_pin=4):
        self.pir = MotionSensor(sensor_pin)
        self.led_pins = {}
        self.count = int(time.time())
        self.pir.when_motion = self.on_when_motion
        self.pir.when_no_motion = self.on_when_no_motion
        self.audio_file_index = 0
        self.led_color_index = 0
        for pin in LED_PINS:
            self.led_pins[pin] = LED(pin)
        print('Artwork is watching motions...')
        pause()

    def on_when_motion(self):
        self.count = int(time.time())
        print('Motion detected!')
        self.control_led()
        self.play_sound()
        self.control_led(on=False)
        print("Sleeping for a while.")
        time.sleep(60)

    def on_when_no_motion(self):
        new_time = int(time.time())
        gap = new_time - self.count
        self.count = new_time
        print('Motion lost, lasted {gap} seconds.'.format(gap=gap))

    def play_sound(self):
        current = os.path.join(self.work_path, 'audios', AUDIOS[self.audio_file_index])
        print("Playing {}".format(AUDIOS[self.audio_file_index]))
        os.system('mpg123 -q "{}"'.format(current))
        print("Finish Playing {}.".format(AUDIOS[self.audio_file_index]))
        self.audio_file_index += 1
        try:
            AUDIOS[self.audio_file_index]
        except IndexError:
            self.audio_file_index = 0

    def control_led(self, on=True):
        led_pins = LED_COLORS[self.led_color_index]
        if on:
            print("Turning on LED for pins {}".format(led_pins))
            for pin in led_pins:
                self.led_pins[pin].on()
        else:
            print("Turning off LED for pins {}".format(led_pins))
            for pin in led_pins:
                self.led_pins[pin].on()
            self.led_color_index += 1
            try:
                LED_COLORS[self.led_color_index]
            except IndexError:
                self.led_color_index = 0

Artwork()
