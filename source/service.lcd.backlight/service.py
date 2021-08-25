# -*- coding: utf-8 -*-

from xbmc import Monitor, log as _log, LOGINFO
from xbmcaddon import Addon
import OPi.GPIO as GPIO

BOARDS = ('PCPCPLUS', 'THREE', 'LITE2', 'ONEPLUS', 'PCPCPLUS', 'PC2', 'PCPCPLUS', 'PCPCPLUS', 'PCPCPLUS', 'PLUS2E')
addon       = Addon(id = 'service.lcd.backlight')
addonname   = addon.getAddonInfo('name')

def LANG(id):
    return addon.getLocalizedString(id)

def log(message):
    _log("{}: {}".format(addonname, message), level = LOGINFO)

def getSetting(id):
    return addon.getSetting(id)


class SmartMonitor(Monitor):
    pwm = None

    def __init__(self, *args, **kwargs):
        Monitor.__init__(self)
        GPIO.setwarnings(False)
        brd, pin, logic, value = self.getSettings()
        GPIO.setboard(brd)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, 500)
        self.pwm.start(value)

    def getSettings(self):
        board = int(getSetting('board'))
        brd = GPIO.__getattribute__(BOARDS[board])
        id = 'header26' if board in (1, 2, 3) else 'header40'
        pin = int(getSetting(id))
        log("pin = {}".format(pin))
        logic = ['true', 'false'].index(getSetting('logic'))
        log("logic = {}".format(logic))
        value = int(getSetting('value'))
        log("value = {}".format(value))
        value = value if logic else 100 - value
        return (brd, pin, logic, value)

    def setupGpio(self):
        self.pwm.stop()
        brd, pin, logic, value = self.getSettings()
        GPIO.setboard(brd)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, 500)
        self.pwm.start(value)

    def onSettingsChanged(self):
        log(LANG(30085))
        self.setupGpio()

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    monitor = SmartMonitor()
    log(LANG(30083))
    while not monitor.abortRequested():
        if monitor.waitForAbort(60):
            break
    log(LANG(30084))
    monitor.cleanup()
    del monitor

