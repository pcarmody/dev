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

def get_white_color(center, scope, trans):
  half = (scope[1] - scope[0] ) / 2
  first = (scope[1] - scope[0] ) / 4
  third = 3 * (scope[1] - scope[0] ) / 4
  red = 0
  blue = 0
  green = 0
  if(center < half):
    red = 255 * (first - abs(first - center))/first
  if(center > half):
    blue = 255 * (first - abs(third - center))/first
  if(center >= first and center < third):
    green = 255 * (first - abs(half - center))/first
  else:
    if center < first:
      green = 255 * (first - center)/first
      blue = 255 * (first - center)/first
      red = 255
    else:
      green = 255 * abs(third - center)/first
      red = 255 * abs(third - center)/first
      blue = 255
  return (red, green, blue, trans)

def get_black_color(center, scope):
  half = (scope[1] - scope[0] ) / 2
  first = (scope[1] - scope[0] ) / 4
  third = 3 * (scope[1] - scope[0] ) / 4
  if(center < half):
    red = 255 * (first - abs(first - center))/first
  else:
    red = 0
  if(center > first and center <= third):
    green = 255 * (first - abs(half - center))/first
  else:
    green = 0
  if(center < half):
    blue = 0
  else:
    blue = 255 * (first - abs(third - center))/first
  color = (red, green, blue, 255)
  return color

def get_color(center, scope):
  half = (scope[1] - scope[0] ) / 2
  if center > half:
    return get_white_color(center, scope, 255)
  return get_black_color(center, scope)

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
  num_wedges = 100
  delta_hour = num_wedges / 24
  wedge = 36000 / num_wedges
  for j in range(0,num_wedges):
    first = ((j*100)/num_wedges) * 24/100
    if(first == 23):
      second = 0
    else:
      second = first + 1
    delta_B = j % delta_hour
    delta_A = delta_hour - delta_B
    beg = wedge * j / 100
    end = (j+1) * wedge / 100
    temp1 = int(weather[first]['Teperature'][0]) * 10 + int(weather[first]['Teperature'][1])
    temp2 = int(weather[second]['Teperature'][0]) * 10 + int(weather[second]['Teperature'][1])
    temp = (temp1*delta_A + temp2*delta_B) / delta_hour
    print str(j)+':'+str(first)+':'+str(temp)+':'+str(beg)+':'+str(end)
    color = get_color(110-temp, (20, 110)) 
    draw.pieslice(shape, beg, end, color, color)
  return image

def draw_wind_ring(shape):
  image = Image.new('RGBA',(shape,shape),(0,0,0,0))
  draw = ImageDraw.Draw(image)
  wedge = 360 / 24
  for i in range(0,24):
    beg = wedge * i
    end = beg + wedge
    wind = weather[i]['Wind'].split(' ')
    dirstr = wind[0]
    if(dirstr == 'Calm'):
      color = (0, 0, 0, 255)
      speed = 0
    else:
      direction = 0
      tmp = 0
      for j in ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW' ]:
        if(j == dirstr):
          direction = tmp
        tmp = tmp + 1
      speed = int(wind[1])
      color = get_white_color(direction, (0,15), 255)

    draw.pieslice((0,0,shape,shape), beg, end, color, color)
  return image

def wind_speed(shape):
  image = Image.new('RGBA',(shape,shape),(0,0,0,0))
  draw = ImageDraw.Draw(image)
  wedge = 360 / 24
  for i in range(0,24):
    beg = wedge * i
    end = beg + wedge
    wind = weather[i]['Wind'].split(' ')
    dirstr = wind[0]
    if(dirstr == 'Calm'):
      color = (0, 0, 0, 255)
      speed = 0
    else:
      speed = int(wind[1])
    max_speed = 15
    speed_color = (0,0,0,255*(max_speed - speed)/max_speed)
    draw.pieslice((0,0,shape,shape), beg, end, speed_color, speed_color)
  return image

def precip_ring(shape):
  image = Image.new('RGBA',(shape,shape),(0,0,0,0))
  draw = ImageDraw.Draw(image)
  wedge = 360 / 24
  for i in range(0,24):
    beg = wedge * i
    end = beg + wedge
    precip = int(weather[i]['Precipitation'].split('%')[0])
    color = get_color(precip, (0,50)) #(0,0,0,255*speed/8)
    draw.pieslice((0,0,shape,shape), beg, end, color, color)
  return image

def humidity_ring(shape):
  image = Image.new('RGBA',(shape,shape),(0,0,0,0))
  draw = ImageDraw.Draw(image)
  wedge = 360 / 24
  for i in range(0,24):
    beg = wedge * i
    end = beg + wedge
    precip = int(weather[i]['Humidity'].split('%')[0])
    color = get_color(precip, (0,100)) #(0,0,0,255*speed/8)
    draw.pieslice((0,0,shape,shape), beg, end, color, color)
  return image

#temp_ring = draw.ellipse(ring_shape(0),'blue','blue')
img = draw_temp_ring(ring_shape(0))
image.paste(img, ring_shape(0), img)

#wind_ring = draw.ellipse(ring_shape(1),'red','blue')
img = draw_wind_ring(ring_size(1))
image.paste(img, ring_shape(1), img)

#wind_ring = draw.ellipse(ring_shape(1),'red','blue')
img = wind_speed(ring_size(1))
image.paste(img, ring_shape(1), img)

#precip_tide = draw.ellipse(ring_shape(2),'yellow','blue')
img = precip_ring(ring_size(2))
image.paste(img, ring_shape(2), img)

img = humidity_ring(ring_size(3))
image.paste(img, ring_shape(3), img)

precip_tide = draw.ellipse(ring_shape(4),'black','blue')

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
