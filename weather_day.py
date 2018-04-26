from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
import datetime
import json
from os.path import expanduser
home = expanduser("~")

window_size = 800
ring_width = 20

image = Image.new('RGBA',(window_size,window_size),(0,0,0,0))
draw = ImageDraw.Draw(image)

def ring_size(level):
  percentage = window_size * ring_width/100
  return window_size - (level * percentage)

def ring_disp(level):
  percentage = window_size * (ring_width/2)/100
  return level * percentage

def ring_shape(level):
  disp = ring_disp(level)
  size = ring_size(level)
  retval = (disp, disp, size+disp, size+disp)
  return retval

wind_color =  ( (255, 255, 255, 255),
                (255, 192, 192, 255),
                (255, 127, 127, 255),
                (255, 65, 65, 255),
                (255, 0, 0, 255),
                (192, 62, 0, 255),
                (127, 127, 0, 255),
                (65, 189, 0, 255),
                (0, 255, 0, 255),
                (0, 192, 62, 255),
                (0, 127, 127, 255),
                (0, 65, 189, 255),
                (0, 0, 255, 255),
                (62, 62, 255, 255),
                (127, 127, 255, 255),
                (189, 189, 255, 255) )

min_per_day = 60*24
temp_space = ring_size(0)
temp_disp = ring_disp(0)
wind_space = ring_size(1)
wind_disp = ring_disp(1)

def convert_time_to_minutes(hours, minutes, am):
  if(am == 'AM' or am == 'am'):
    if(hours == 12):
      hours = 0
  else:
    if(hours != 12):
      hours = hours + 12
  return hours * 60 + minutes

def draw_halves(size, temp_rise, temp_set, day_color):
  image = Image.new('RGBA', (size, size), (0,0,0,0))
  draw = ImageDraw.Draw(image)
  rise_angle = 360 * temp_rise / min_per_day
  set_angle = 360 * temp_set / min_per_day
  night_color = (day_color[0]/4, day_color[1]/4, day_color[2]/4)
  draw.pieslice((0,0,size, size), set_angle, rise_angle, night_color, 'black')
  draw.pieslice((0,0,size, size), rise_angle, set_angle, day_color, 'black')
  return image

#
# construct today's image
#

now = datetime.datetime.now()
day = now.day
month = now.month
year = now.year

#
# retrieve the sun and temp data
#

#wind_temp_file = open(home+'/bin/data/suntemp_'+str(year)+("%0.02d" % month))
wind_temp_file = open('hourly.json')
weather = json.load(wind_temp_file)
wind_temp_file.close()

def add_lines(beg, end):
  image3 = Image.new('RGBA',(window_size,window_size),(0,0,0,0))
  draw3 = ImageDraw.Draw(image3)
  non_color = (0, 0, 0, 0)
  line_color = (0, 0, 0, 50)
  if(beg % 90 == 0):
    line_color = (0,0,0,255)
  draw3.pieslice(ring_shape(0), beg, end, non_color, line_color)
  return image3

#
# draw the temperature ring
#

def draw_temp_ring(shape):
  image = Image.new('RGBA',(window_size,window_size),(0,0,0,0))
  draw = ImageDraw.Draw(image)
  wedge = 360 / 24
  for i in range(0,20):
    beg = wedge * i
    end = beg + wedge
    temp = int(weather[i]['Teperature'][0]) * 10 + int(weather[i]['Teperature'][1]) - 40 
    color = (0,0,255, 255 * temp / 20)
    draw.pieslice(shape, beg, end, color, color)
  return image

#temp_ring = draw.ellipse(ring_shape(0),'blue','blue')
img = draw_temp_ring(ring_shape(0))
image.paste(img, ring_shape(0), img)
wind_ring = draw.ellipse(ring_shape(1),'red','blue')
precip_tide = draw.ellipse(ring_shape(2),'black','blue')

#draw hourly lines
for beg in [0, 60, 120, 180, 240, 300]:
  image3 = add_lines(beg, beg+90)
  image.paste(image3, ring_shape(0), image3)

# rotate the entire image based on the current time.

current_time = convert_time_to_minutes(now.hour, now.minute, 'am')#(4, 45, 'PM')
xxx = image.rotate(360*current_time/min_per_day + 90)

image2 = Image.new('RGBA',(window_size,window_size),(0,0,0,255))
image2.paste(xxx,ring_shape(0),xxx)
image2.show()
