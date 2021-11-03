# Imports
import os, ctypes, keyboard, json, mss, PIL, PyQt5, time, sys, threading 
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL.Image import frombytes
from ctypes import wintypes
from os import system 

# Settings 
settings = json.load(open(os.getcwd()+'\\config.json'))

# System Constants
krnl32 = ctypes.WinDLL('kernel32', use_last_error=True)
user32 = ctypes.WinDLL('User32', use_last_error=True)

# Declarations
fovSize = settings['fovSize'] # area range
lenience = 5 # rgb offsets
r,g,b = (200,50,200) # color search 
screenWidth, screenHeight = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)) #monitor
fov = (int(screenWidth/2-fovSize), int(screenHeight/2-fovSize), int(screenWidth/2+fovSize), int(screenHeight/2+fovSize)) # search area 

# Functions
def toggle(): # Enable/Disable 
  settings['triggerBot'] = not settings['triggerBot'] 
  settings['triggerBot'] and krnl32.Beep(400,50), krnl32.Beep(600,100) or krnl32.Beep(600,50), krnl32.Beep(400,100)

# KeyBinds
keyboard.add_hotkey(settings['keyBind'], toggle, args=()) # toggle

# Fov Drawing
class FovVisualizer(QtWidgets.QWidget):
  def __init__(self):
    QtWidgets.QWidget.__init__(self, None)
    self.resize(screenWidth,screenHeight)
    self.pen = QtGui.QPen(QtGui.QColor(0, 255, 157)) 
    self.pen.setWidth(1)
    self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTransparentForInput)
    self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

  def paintEvent(self, event):
   brush = QtGui.QPainter(self)
   brush.setPen(self.pen)
   brush.drawRect(screenWidth/2-(fovSize*2/2),screenHeight/2-(fovSize*2/2), fovSize*2, fovSize*2)

# Triggerbot
def Triggerbot():
  while True: 
    if settings['triggerBot']:
      with mss.mss() as ssobj: # create screenshot object 
        grab = ssobj.grab(fov) # screenshot
        img = frombytes("RGB", grab.size, grab.bgra, "raw", "BGRX") 
        for y in range(0,fovSize): # y position
          for x in range(0,fovSize): # x position
            rp,gp,bp = img.getpixel((x,y)) # pixel color
            if (r-lenience < rp and r+lenience < rp and g-lenience < gp and g+lenience < gp and b-lenience < bp and b+lenience < bp):
              user32.mouse_event(0x0002)
              time.sleep(0.005)
              user32.mouse_event(0x0004)
              break
          else:
            continue
          break

# Trigger Bot 
threading.Thread(target=Triggerbot).start()

# Fov Visualizer
if settings['showFov']:
  app = QtWidgets.QApplication(sys.argv)
  visualize = FovVisualizer();
  visualize.show();
  sys.exit(app.exec_()) 
