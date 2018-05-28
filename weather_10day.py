from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
import datetime
import json
import sys
from os.path import expanduser

home = expanduser("~")

data_elements = 16
window_size = 400
ring_width = 16
pixel_ring_width = window_size * ring_width/100
num_wedges = 300
delta_hour = num_wedges / data_elements
wedge = 36000 / num_wedges

my_yellow = (150, 150, 255, 0)

image = Image.new('RGBA',(window_size,window_size),(0,0,0,255))
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

def inner_half_size(level):
  return ring_size(level) - pixel_ring_width/2

def inner_half_disp(level):
  return ring_disp(level) + pixel_ring_width/4

def inner_half_shape(level):
  disp = inner_half_disp(level)
  size = inner_half_size(level)
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
#wind_temp_file = open('hourly.json')
wind_temp_file = open('10day.json')
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

def draw_sun_ring(shape):
  image = Image.new('RGBA',(shape,shape),(0,0,0,0))
  draw = ImageDraw.Draw(image)
  for j in range(0,num_wedges):
    first = ((j*100)/num_wedges) * data_elements/100
    if(first == data_elements):
      second = 0
    else:
      second = (first + 1) % data_elements
    delta_B = j % delta_hour
    delta_A = delta_hour - delta_B
    beg = wedge * j / 100
    end = (j+1) * wedge / 100

    if delta_A <= delta_hour / 2:
      temp1 = int(weather[first]['Condition']['AM'])
      temp2 = int(weather[first]['Condition']['PM'])
    else:
      temp1 = int(weather[first]['Condition']['PM'])
      temp2 = int(weather[second]['Condition']['AM'])

    temp = 800 - (temp1*100*delta_A + temp2*100*delta_B) / delta_hour
#    print str(temp)

    my_yellow = (255, 255, 0, 55 + temp * 200 / 800)
    draw.pieslice((0,0,shape,shape), beg, end, my_yellow, my_yellow)
  return image

def draw_temp_high_ring(shape):
  image = Image.new('RGBA',(shape,shape),(0,0,0,0))
  draw = ImageDraw.Draw(image)
  offset = ring_width/2
  for j in range(0,num_wedges):
    first = ((j*100)/num_wedges) * data_elements/100
    if(first == data_elements):
      second = 0
    else:
      second = (first + 1) % data_elements
    delta_B = j % delta_hour
    delta_A = delta_hour - delta_B
    beg = wedge * j / 100
    end = (j+1) * wedge / 100

    temp1 = int(weather[first]['Temperature']['High'])
    temp2 = int(weather[second]['Temperature']['High'])
    temp = (temp1*100*delta_A + temp2*100*delta_B) / delta_hour
    color = get_color(11000-temp, (2000, 11000)) 
    draw.pieslice((0,0,shape,shape), beg, end, color, color)
  return image

def draw_temp_low_ring(shape):
  image = Image.new('RGBA',(shape,shape),(0,0,0,0))
  draw = ImageDraw.Draw(image)
  for j in range(0,num_wedges):
    first = ((j*100)/num_wedges) * data_elements/100
    if(first == data_elements):
      second = 0
    else:
      second = (first + 1) % data_elements
    delta_B = j % delta_hour
    delta_A = delta_hour - delta_B
    beg = wedge * j / 100
    end = (j+1) * wedge / 100
    temp1 = int(weather[first]['Temperature']['Low'])
    temp2 = int(weather[second]['Temperature']['Low'])
    temp = (temp1*100*delta_A + temp2*100*delta_B) / delta_hour
    color = get_color(11000-temp, (2000, 11000)) 
    draw.pieslice((0,0,shape,shape), beg, end, color, color)
  return image

def draw_wind_ring(shape):
  image = Image.new('RGBA',(shape,shape),(0,0,0,0))
  draw = ImageDraw.Draw(image)
  max_speed = 18
  wedge = 360 / data_elements
  for i in range(0,data_elements):
    beg = wedge * i
    end = beg + wedge
    dirstr = weather[i]['Wind']['Direction']
    speed = int(weather[i]['Wind']['Speed']) 
    speed_color = 255*(speed)/max_speed
    if(dirstr == 'Calm'):
      color = (0, 0, 0, speed_color)
    else:
      direction = 0
      tmp = 0
      for j in ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW' ]:
        if(j == dirstr):
          direction = tmp
        tmp = tmp + 1
      color = get_white_color(direction, (0,15), speed_color)

    draw.pieslice((0,0,shape,shape), beg, end, color, color)
  return image

def wind_speed(shape):      #draw a black background
  image = Image.new('RGBA',(shape,shape),(0,0,0,0))
  draw = ImageDraw.Draw(image)
  black = (0,0,0,255)
  draw.pieslice((0,0,shape,shape), 0, 360, black,black)
  return image

def precip_ring(shape):
  image = Image.new('RGBA',(shape,shape),(0,0,0,0))
  draw = ImageDraw.Draw(image)
  for j in range(0,num_wedges):
    first = ((j*100)/num_wedges) * data_elements/100
    beg = wedge * j / 100
    end = (j+1) * wedge / 100
    if(first == 23):
      second = 0
    else:
      second = (first + 1) % data_elements
    delta_B = j % delta_hour
    delta_A = delta_hour - delta_B
#    precip1 = int(weather[first]['Precipitation'].split('%')[0])
#    precip2 = int(weather[second]['Precipitation'].split('%')[0])
    precip1 = int(weather[first]['Precipitation'])
    precip2 = int(weather[second]['Precipitation'])
    precip = (precip1*100*delta_A + precip2*100*delta_B) / delta_hour
    #precip = (precip1 + precip2) / 2
    color = get_color(precip/100, (0,50)) #(0,0,0,255*speed/8)
    draw.pieslice((0,0,shape,shape), beg, end, color, color)
  return image

def humidity_ring(shape):
  image = Image.new('RGBA',(shape,shape),(0,0,0,0))
  draw = ImageDraw.Draw(image)
  for j in range(0,num_wedges):
    first = ((j*100)/num_wedges) * data_elements/100
    beg = wedge * j / 100
    end = (j+1) * wedge / 100
    if(first == 23):
      second = 0
    else:
      second = (first + 1) % data_elements
    delta_B = j % delta_hour
    delta_A = delta_hour - delta_B
    humid1 = int(weather[first]['Humidity'])
    humid2 = int(weather[second]['Humidity'])
    humid = (humid1*100*delta_A + humid2*100*delta_B) / delta_hour
    color = get_color(humid/100, (0,100)) #(0,0,0,255*speed/8)
    draw.pieslice((0,0,shape,shape), beg, end, color, color)
  return image

#temp_ring = draw.ellipse(ring_shape(0),'blue','blue')
img = draw_sun_ring(ring_size(0))
image.paste(img, ring_shape(0), img)

img = draw_temp_high_ring(ring_size(1))
image.paste(img, ring_shape(1), img)

#img = draw_temp_low_ring(ring_size(2))
#image.paste(img, ring_shape(2), img)
img = draw_temp_low_ring(inner_half_size(1))
image.paste(img, inner_half_shape(1), img)

wind_ring = draw.ellipse(ring_shape(2),'red','blue')
img = wind_speed(ring_size(2))
image.paste(img, ring_shape(2), img)

#wind_ring = draw.ellipse(ring_shape(1),'red','blue')
img = draw_wind_ring(ring_size(2))
image.paste(img, ring_shape(2), img)

#precip_tide = draw.ellipse(ring_shape(2),'yellow','blue')
img = precip_ring(ring_size(3))
image.paste(img, ring_shape(3), img)

img = humidity_ring(ring_size(4))
image.paste(img, ring_shape(4), img)

precip_tide = draw.ellipse(ring_shape(5),'black','blue')

#draw day lines
#for beg in [0, 60, 120, 180, 240, 300]:
#for beg in [0, 36, 72, 108, 144, 180, 216, 242, 278, 314]:
inc = 36000 / data_elements
for i in range(0, data_elements):
  beg = i*inc / 100
  image3 = add_lines(beg, beg+inc)
  image.paste(image3, ring_shape(0), image3)

# rotate the entire image based on the current time.

#current_time = convert_time_to_minutes(now.hour, now.minute, 'am')#(4, 45, 'PM')
xxx = image.rotate(90)
xxx.show()

#image2 = Image.new('RGBA',(window_size,window_size),(0,0,0,255))
#image2.paste(xxx,ring_shape(0),xxx)
#image2.show()
