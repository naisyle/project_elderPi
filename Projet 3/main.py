from sense_hat import SenseHat
import time
import os
from dessins import *

s = SenseHat()
s.low_light = True

ggs = [noir_rouge(), noir_blanc()]
images = [trinket_logo, plus, raspi_logo, equals]
count1 = 0
count2 = 0

while True:
    event = s.stick.wait_for_event()
    if event.action == "pressed" and event.direction == "right":
      s.set_pixels(images[count1 % len(images)]())
      time.sleep(.5)
      count1 += 1
      
    if event.action == "pressed" and event.direction == "left":
      s.set_pixels(images[count1 % len(images)-1]())
      time.sleep(.5)
      count1 -= 1
      
    if event.action == "pressed" and event.direction == "up":
      s.set_pixels(ggs[count2 % 2])
      time.sleep(.5)
      count2 += 1

    if event.action == "pressed" and event.direction == "middle" and count1 == 1:
	

      """print(1)
	faire la saisie vocal pour le code secret"""

    if event.action == "pressed" and event.direction == "middle" and count1 == 2:
	

     """ print(2)
      faire la fonction speciale"""

    if event.action == "pressed" and event.direction == "middle" and count1 == 3:
	

      """print(3)
      faire la liste de course """ 

    if event.action == "pressed" and event.direction == "middle" and count1 == 4:
      s.show_message("shutdown", text_colour=[255, 0, 0])
      result = os.system("shutdown now -h")
      time.sleep(1)
    """print(4)
         quite et eteindre le rasp pi"""

