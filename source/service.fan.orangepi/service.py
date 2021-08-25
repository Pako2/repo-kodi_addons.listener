# -*- coding: utf-8 -*-

from subprocess import check_output
from os import listdir
from xbmc import Monitor, LOGINFO, log as _log
from xbmcaddon import Addon
import OPi.GPIO as GPIO

BOARDS = ('PCPCPLUS', 'THREE', 'LITE2', 'ONEPLUS', 'PCPCPLUS', 'PC2', 'PCPCPLUS', 'PCPCPLUS', 'PCPCPLUS', 'PLUS2E')
addon       = Addon(id = 'service.fan.orangepi')
addonname   = addon.getAddonInfo('name')

def LANG(id):
    return addon.getLocalizedString(id)

def log(message):
    _log("%s: %s" % (addonname, message), level = LOGINFO)

def getSetting(id):
    return addon.getSetting(id)

def gettemp():
    temps = []
    sensors = [item for item in listdir('/sys/class/thermal') if item.startswith('thermal_zone')]
    for sensor in sensors:
        with open('/sys/class/thermal/%s/temp' % sensor) as f:
            line = f.readline().strip()
        if line.isdigit():
            temps.append(float(line)/1000)
    return max(temps)

def getcpuusage():
    pid = int(check_output(["pidof","-s","kodi.bin"]))
    top = check_output(["top", "-b", "-n", "1", "-p%i" % pid])
    line = top.split(b'\n')[-2]
    return float(line.split()[8])


class BackgroundService(Monitor):
    fan = None
    board = None

    def initGPIO(self, brd, pin):
        GPIO.setboard(brd)
        self.board = brd
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
        self.fan = pin

    def __init__(self):
        Monitor.__init__(self)
        log(LANG(30083))
        GPIO.setwarnings(False)
        self.initGPIO(self.getBoard(), self.getFanPin())

    def getBoard(self):
        return GPIO.__getattribute__(BOARDS[int(getSetting('board'))])

    def getFanPin(self):
        board = int(getSetting('board'))
        id = 'header26' if board in (1, 2, 3) else 'header40'
        return int(getSetting(id))

    def log_it(self, temp, usage, turn = None):
        kind = int(getSetting('log'))
        if kind == 0:
            return
        if kind == 1 and turn is None:
            return
        message = LANG(30082).format(temp, usage)
        message += LANG(turn + 30080) if turn is not None else ""
        log(message)

    def tick(self):
        pin = self.getFanPin()
        brd = self.getBoard()
        if pin != self.fan or brd != self.board:
            self.initGPIO(brd, pin)
        temp = gettemp()
        usage = getcpuusage()
        if GPIO.input(self.fan): # Fan is ON
            if getSetting('kodiusage'):
                if usage >= int(getSetting('cpubottom')):
                    self.log_it(temp, usage)
                    return
            if temp >= int(getSetting('tempbottom')):
                self.log_it(temp, usage)
                return
            GPIO.output(self.fan, 0)
            self.log_it(temp, usage, 0)
        else:                    # Fan is OFF
            if getSetting('kodiusage'):
                if usage >= int(getSetting('cputop')):
                    GPIO.output(self.fan, 1)
                    self.log_it(temp, usage, 1)
                    return
            if temp >= int(getSetting('temptop')):
                GPIO.output(self.fan, 1)
                self.log_it(temp, usage, 1)
                return
        self.log_it(temp, usage)

if __name__ == '__main__':
    monitor = BackgroundService()
    while not monitor.abortRequested():
        if monitor.waitForAbort(int(getSetting('period'))):
            break
        monitor.tick()
    log(LANG(30084))
    GPIO.cleanup()
    del monitor
