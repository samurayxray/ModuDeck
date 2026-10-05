from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
p=Path(__file__).parent
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def page(title,sub):
 im=Image.new('RGB',(1600,1100),'#101b2b'); d=ImageDraw.Draw(im)
 def txt(x,y,s,size=25,col='#e5edf7'): d.text((x,y),s,font=ImageFont.truetype(font,size),fill=col)
 txt(60,35,'MODUDECK / MODULE MONITOR',24,'#4dd9c5');txt(60,90,title,42);txt(60,155,sub,22)
 txt(60,1020,'PRELIMINARY DESIGN / AI-assisted / Not built or hardware-tested',22,'#ffcd70')
 return im,d,txt
def box(d,t,x,y,w,h,label):
 d.rounded_rectangle((x,y,x+w,y+h),15,fill='#20364e',outline='#4dd9c5',width=3)
 for i,s in enumerate(label.split('\n')):t(x+20,y+20+i*34,s,24)
def line(d,pts,col='#4dd9c5'):d.line(pts,fill=col,width=4)
im,d,t=page('01 / System architecture','Three independent presence channels; USB powers the monitor only.')
box(d,t,70,330,300,140,'Computer\nUSB serial status\nUSB 5 V supply')
box(d,t,560,290,370,230,'Raspberry Pi Pico\n3.3 V GPIO logic\nDebounce: 30 ms\nUSB JSON output')
line(d,[(370,400),(560,400)])
for i in range(3):
 y=230+i*235;box(d,t,1140,y,370,145,f'Tray {i+1}\nCOM / NO switch\nClosed = present');line(d,[(930,350+i*50),(1030,350+i*50),(1030,y+70),(1140,y+70)])
box(d,t,560,740,370,110,'Three local status LEDs\nOne LED per tray');line(d,[(740,520),(740,740)])
t(65,910,'Presence detection only: no tray power, USB hub or battery charging.',25)
im.save(p/'docs/01-architecture.png')
im,d,t=page('02 / Input circuit x3','Repeat this channel for GP2, GP3 and GP4. All grounds are common.')
# functional wiring using labelled resistor boxes
box(d,t,80,460,250,95,'Pico GPIO input')
line(d,[(330,505),(690,505),(690,680),(950,680)])
box(d,t,580,300,220,90,'10 kohm pull-up');line(d,[(690,250),(690,300)]);t(620,205,'3V3 OUT',26);line(d,[(690,390),(690,505)])
box(d,t,950,630,210,100,'1 kohm series');line(d,[(1160,680),(1260,680),(1260,530)])
t(1170,450,'J: pin 1 / NO',24);d.ellipse((1253,513,1267,527),outline='white',width=3);line(d,[(1260,515),(1340,470)])
d.ellipse((1353,513,1367,527),outline='white',width=3);line(d,[(1360,527),(1360,760)]);t(1250,780,'J: pin 2 / COM / GND',21)
t(960,340,'External normally-open switch',25);t(960,385,'Closes when tray is seated',23)
t(80,840,'OPEN: GPIO reads 1 -> absent      CLOSED: GPIO reads 0 -> present',27)
t(80,900,'Connect only a dry switch contact; keep GPIO signals at 3.3 V logic.',23)
im.save(p/'docs/02-input-circuit.png')
im,d,t=page('03 / Pin and cable map','Pico physical pins refer to the original Raspberry Pi Pico 40-pin layout.')
rows=[('Tray 1 input','GP2 / pin 4','J1 pin 1 via 1k; 10k pull-up'),('Tray 2 input','GP3 / pin 5','J2 pin 1 via 1k; 10k pull-up'),('Tray 3 input','GP4 / pin 6','J3 pin 1 via 1k; 10k pull-up'),('Tray 1 LED','GP10 / pin 14','1k -> LED anode; cathode -> GND'),('Tray 2 LED','GP11 / pin 15','1k -> LED anode; cathode -> GND'),('Tray 3 LED','GP12 / pin 16','1k -> LED anode; cathode -> GND'),('Pull-up supply','3V3 OUT / pin 36','Three 10k resistors'),('Ground','GND / pin 38','J1/J2/J3 pin 2 and LED cathodes'),('PC connection','Pico micro-USB','USB data cable; sole power input')]
for i,row in enumerate(rows):
 y=255+i*73;d.rectangle((60,y-8,1540,y+55),fill=('#20364e' if i%2==0 else '#152638'))
 for x,s in zip([80,410,780],row):t(x,y,s,22)
im.save(p/'docs/03-pin-map.png')
im,d,t=page('04 / PCB placement proposal','Indicative arrangement only. Footprints, board size and routing remain to be verified.')
d.rounded_rectangle((220,260,1380,800),25,fill='#123f3b',outline='#4dd9c5',width=4)
box(d,t,285,390,380,210,'Pico socket\nUSB faces board edge\nKeep access to BOOTSEL')
for i in range(3):
 x=750+i*190;box(d,t,x,310,155,100,f'J{i+1}\nSIG / GND');box(d,t,x,465,155,115,'10k pull-up\n1k series');box(d,t,x,650,155,100,f'LED {i+1}\n1k resistor')
t(100,855,'Before manufacturing: schematic ERC, footprint check, routed PCB DRC,',25)
t(100,900,'connector polarity, USB clearance and a paper fit test.',25)
im.save(p/'docs/04-pcb-placement.png')
