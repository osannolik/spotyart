import subprocess
import pigpio

def force(state='on'):
	subprocess.run(['xset', 'dpms', 'force', state])

def disable_blanking():
	subprocess.run(['xset', '-dpms'])
	subprocess.run(['xset', 's', 'off'])

class Hyperpixel(object):

	SIZE = (720,720)

	def __init__(self):
		super(Hyperpixel, self).__init__()
		self._gpio = pigpio.pi()

	# Assumes pigpiod deamon is running
	def backlight_brightness(self, percent):
		freq = 100
		max_duty = 1000000
		self._gpio.hardware_PWM(19, 100, int(percent*max_duty))

def main():
	import time

	# env var DISPLAY must be set
	disp = Hyperpixel()
	print('Turn on fully...')
	for duty in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
		disp.backlight_brightness(duty)
		time.sleep(1)

	print('Turn off!')
	disp.backlight_brightness(0.0)

if __name__ == '__main__':
	main()
