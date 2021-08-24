#-*- coding: utf-8 -*-
from xbmc import Monitor
from xbmcaddon import Addon
from time import sleep, time as ttime

try:
    import OPi.GPIO as GPIO
except Exception as ex:
    import xbmc
    xbmc.log("===========================================================",level=xbmc.LOGINFO)
    xbmc.log(repr(ex),level=xbmc.LOGINFO)
try:
    from evdev import UInput, ecodes as e
except Exception as ex:
    import xbmc
    xbmc.log("===========================================================",level=xbmc.LOGINFO)
    xbmc.log(repr(ex),level=xbmc.LOGINFO)

addon       = Addon(id = 'service.gpio-keyboard')
addonname   = addon.getAddonInfo('name')
monitor = None
BOARDS = ('PCPCPLUS', 'THREE', 'LITE2', 'ONEPLUS', 'PCPCPLUS', 'PC2', 'PCPCPLUS', 'PCPCPLUS', 'PCPCPLUS', 'PLUS2E')
KEYS = (
    None,
    e.KEY_C,
    e.KEY_E,
    e.KEY_F,
    e.KEY_I,
    e.KEY_P,
    e.KEY_R,
    e.KEY_S,
    e.KEY_X,
    e.KEY_SPACE,
    e.KEY_LEFT,
    e.KEY_RIGHT,
    e.KEY_UP,
    e.KEY_DOWN,
    e.KEY_ENTER,
    e.KEY_BACKSPACE,
    e.KEY_ESC,
    e.KEY_F8,
    e.KEY_KPMINUS,
    e.KEY_KPPLUS,
    e.KEY_HOME
    )

def LANG(id):
    return addon.getLocalizedString(id)

def log(message):
    level = xbmc.LOGINFO
    xbmc.log("{}: {}".format(addonname, message), level = level)

def getSetting(id):
    return addon.getSetting(id)

def buttcallback(pin):
    global monitor
    monitor.buttcallback(pin)

class BackgroundService(Monitor):
    pins = []
    keys = {}
    buttimes = {}
    twofunc = 0
    twotime = 0
    numofbutt = 0
    ui = None

    def __init__(self):
        Monitor.__init__(self)
        log(LANG(30083))
        self.ui = UInput()
        GPIO.setwarnings(False)
        self.setup()


    def setup(self):
        brd, bouncetime, pullup = self.getSettings()
        GPIO.setboard(brd)
        GPIO.setmode(GPIO.BOARD)
        for pin in self.pins:
                GPIO.setup(pin, GPIO.IN, pullup)
                GPIO.add_event_detect(pin, GPIO.BOTH, callback=buttcallback, bouncetime=bouncetime)


    def getSettings(self):
        self.twofunc = ['false', 'true'].index(getSetting('twofunc'))
        pullup = ['false', 'true'].index(getSetting('intpullup'))
        pullup = GPIO.PUD_UP if pullup else GPIO.PUD_OFF
        board = int(getSetting('board'))
        brd = GPIO.__getattribute__(BOARDS[board])
        header = [0, 1, 2, 2, 0, 3, 0, 0, 0, 0][board]
        numofbutt = int(getSetting('numofbutt{}'.format([0, 1, 2, 2, 0, 0, 0, 0, 0, 0][board])))
        self.numofbutt = numofbutt
        tmp = []
        tmpdict={}
        for ix in range(numofbutt):
            pin = int(getSetting('butt{}{}'.format(ix+1, header)))
            if pin:
                tmp.append(pin)
                f1 = int(getSetting('first{}'.format(ix+1)))
                f2 = int(getSetting('sec{}'.format(ix+1))) if self.twofunc else None
                tmpdict[pin] = (f1, f2)
        self.keys = tmpdict
        self.pins = tmp
        bouncetime = int(getSetting('debtime'))
        self.twotime = int(getSetting('twotime'))
        return (brd, bouncetime, pullup)


    def buttcallback(self, pin):
        level = GPIO.input(pin)
        if not level:
            self.buttimes[pin] = ttime()
            return
        t = self.buttimes[pin]
        self.buttimes[pin] = None
        if t is not None:
            #log("pin = {}".format(pin))
            delta = 1000 * (ttime() - t)
            ix = 0
            if self.twofunc and delta > self.twotime:
                ix = 1
                #log("longpress ({} ms)".format(delta))
            #else:
            #    log("shortpress ({} ms)".format(delta))
            key = self.keys[pin][ix]
            if key:
                key = KEYS[key]
                self.ui.write(e.EV_KEY, key, 1)
                self.ui.write(e.EV_KEY, key, 0)
                self.ui.syn()


    def onSettingsChanged(self):
        log(LANG(30085))
        for pin in self.pins:
            GPIO.remove_event_detect(pin)
        self.setup()


    def cleanup(self):
        try:
            self.ui.close()
        except Exception as ex:
            log("Exception: {}".format(repr(ex)))
        for pin in self.pins:
            GPIO.remove_event_detect(pin)
        GPIO.cleanup()


if __name__ == '__main__':
    monitor = BackgroundService()
    while not monitor.abortRequested():
        if monitor.waitForAbort(60):
            monitor.cleanup()
            break
    log(LANG(30084))
    del monitor

