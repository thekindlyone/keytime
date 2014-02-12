import pythoncom, pyHook
import time
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('keytime_config.ini')
isspecial = 0
buff = parser.get('settings', 'delay')
buff = float(buff)
lasthit = time.time()
isfirst = 1


def OnKeyboardEvent(event):
    t = time.time()
    global lasthit
    global isfirst
    global isspecial
    lasthit = t
    specials = ['Lcontrol', 'Rcontrol', 'Lshift', 'Rshift']
    #print event.Key
    if (event.Key in specials):
        isspecial = 1
    else:
        isspecial = 0
    isfirst = 0
    return True


def OnMouseEvent(event):
    global isfirst
    global lasthit
    global buff
    global isspecial
    diff = time.time() - lasthit
    rc = True
    if isfirst:
        rc = True
    if (diff < buff and not isfirst and not isspecial):
        rc = False

    if (diff > buff and not isfirst):
        rc = True
    return rc


class hookWork(object):
    def __init__(self, delay):
        self.buffer = delay


def main():
    print "App started. Close this window to stop. Ignore the error on exit"
    # create a hook manager
    hm = pyHook.HookManager()
    # watch for all mouse events
    hm.MouseAll = OnMouseEvent
    hm.KeyDown = OnKeyboardEvent
    # set the hook
    hm.HookKeyboard()
    hm.HookMouse()
    # wait forever
    pythoncom.PumpMessages()


if __name__ == '__main__':
    main()
