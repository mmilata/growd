import logging

from growd.hw.i2c import I2CBus

logger = logging.getLogger('raspberry')

try:
    import RPi.GPIO as GPIO
except ImportError:
    logger.error('RPi.GPIO not found!')
except RuntimeError:
    logger.error('Error importing RPi.GPIO! You probably need to run this as root.')

class Board(object):
    def __init__(self):
        pass

    def cleanup(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, ty, value, traceback):
        self.cleanup()

class Raspberry(Board):
    def __init__(self):
        super(Raspberry, self).__init__()

        if not 'GPIO' in globals():
            raise RuntimeError('GPIO module error');

        GPIO.setmode(GPIO.BOARD)

        self.i2c = {}
        self.gpios_set_up = False #avoid warning on cleanup

    def gpio_setup(self, num, is_output):
        GPIO.setup(num, GPIO.OUT if is_output else GPIO.IN)
        self.gpios_set_up = True

    def gpio_set(self, num, value):
        GPIO.output(num, value)

    def i2c_setup(self):
        device_number = 1
        i2c = I2CBus('/dev/i2c-%s' % device_number)
        self.i2c[device_number] = i2c

    def cleanup(self):
        for i2c_num in self.i2c.keys():
            self.i2c.pop(i2c_num).cleanup()

        if self.gpios_set_up:
            GPIO.cleanup()
