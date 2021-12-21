
import os; 
if os.name != 'nt': raise SystemExit
import time
import json 
import mss  
import ctypes 
import sys
from keyboard import add_hotkey
from PIL.Image import frombytes
from threading import Thread as thread 
from art import *
from collections import namedtuple

CFG_PTH = 'valorant-config.json'
CWD = os.getcwd()
CLEAR = lambda:os.system('cls')
CFG_EXISTS = os.path.isfile(CWD+'/'+CFG_PTH)
KRNL32 = ctypes.WinDLL('kernel32', use_last_error=True)
USER32 = ctypes.WinDLL('User32', use_last_error=True)
WIDTH, HEIGHT = (USER32.GetSystemMetrics(0), USER32.GetSystemMetrics(1))

CONFIG = CFG_EXISTS and json.load(open(CFG_PTH)) 
SETTINGS = namedtuple('SETTINGS', ['color','tapShoot','tapShootDelay','fovX','fovY','key','lenience'])
STATUS = False
VALID_COLORS = ['yellow', 'purple']

def setup(): 
  global SETTINGS
  global CONFIG
  os.system('color b')
  """Create user settings"""

  while True: 
    CLEAR()
    print(text2art('SETUP'))

    try: 
      CONFIG = dict([
        ('color', str(input('Color type (yellow, purple): '))),
        ('tapShoot', int(input('Tap Shoot (0:true 1:false): '))),
        ('tapShootDelay', int(input('Tap Shoot Delay (ms): '))),
        ('fovX', int(input('Fov X size: '))), 
        ('fovY', int(input('Fov Y size: '))), 
        ('key', str(input('Toggle bind: '))),
        ('lenience', int(input('Color Lenience (recommended 5-20): ')))
      ])
      
      if (CONFIG['color'] not in VALID_COLORS): 
        CLEAR()
        print('[ERR] Supported colors (yellow & purple)')
        time.sleep(5)
        continue
      if (CONFIG['tapShoot'] not in [0,1]):
        CLEAR()
        print('[ERR] Select 0 or 1 for tap shoot')
        time.sleep(5)
        continue
    except: 
      continue 
    break

  config_file = open(CFG_PTH, 'a+')
  config_file.write(json.dumps(CONFIG, indent=2))

  CLEAR()
  print('Finished! Enjoy!')
  time.sleep(2)

def toggle():
  global STATUS
  """Toggles triggerbot"""

  STATUS = not STATUS
  STATUS and KRNL32.Beep(400,50), KRNL32.Beep(600,100) or KRNL32.Beep(600,50), KRNL32.Beep(400,100)
  print('Status: '+ (STATUS and 'Enabled ' or 'Disabled'), end='\r', flush=True)

def main(): 
  global SETTINGS 
  """Main Loop""" 

  if (not CFG_EXISTS): setup()
  SETTINGS = SETTINGS(**CONFIG)
  LE = SETTINGS.lenience 
  RGB = SETTINGS.color == 'purple' and (200,50,200) or SETTINGS.color == 'yellow' and (255,255,0)
  FOV = (int(WIDTH/2-SETTINGS.fovX), int(HEIGHT/2-SETTINGS.fovY), int(WIDTH/2+SETTINGS.fovX), int(HEIGHT/2+SETTINGS.fovY))
  add_hotkey(SETTINGS.key, toggle, args=())
  CLEAR();print(text2art('V-BOT'));print('Keybind: '+SETTINGS.key)

  while True: 
    if STATUS:
      with mss.mss() as ssobj:  
        grab = ssobj.grab(FOV) 
        img = frombytes("RGB", grab.size, grab.bgra, "raw", "BGRX") 
        for y in range(0,SETTINGS.fovY): 
          for x in range(0,SETTINGS.fovX):
            rp,gp,bp = img.getpixel((x,y)) 
            if (RGB[0]-LE < rp and RGB[0]+LE < rp and RGB[1]-LE < gp and RGB[1]+LE < gp and RGB[2]-LE < bp and RGB[2]+LE < bp):
              USER32.mouse_event(0x0002)
              time.sleep(0.005)
              USER32.mouse_event(0x0004)
              break
          else:
            continue
          break
    time.sleep(SETTINGS.tapShoot == 0 and (SETTINGS.tapShootDelay*0.001) or 0)

if (__name__ == '__main__'):
  main()

# dd
