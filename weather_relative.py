from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
import datetime
import json
import sys
from os.path import expanduser

home = expanduser("~")

window_size = 400
ring_width = 16
num_wedges = 300
delta_hour = num_wedges / 24
wedge = 36000 / num_wedges

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

#  temperature color

color_list = (
    (0, 0, 0, 255),
    (255, 255, 255, 255),
    (238, 130, 238, 255),         # ee82ee
    (75, 0, 130, 255),           #4b0082
    #(189, 151, 230, 255),        #add8e6
    (0, 0, 255, 255),           #4b0082
    (0, 255, 0, 255),
    (255, 255, 0, 255),
    (255, 0, 0, 255),
    (0, 0, 0, 255),
)
color_count = 8

def map_color_value(value, scope):
        
  delta = scope / color_count           # how wide the wedge of color is
  left = value / delta                  # the color of the wedge
#  right = (left + 1) % color_count      # the next color
  right = (left + 1)                     # the next color
  mod = value % delta                   # how deep into the wedge of color
  
  right_weight = mod * 100 / delta      
  left_weight = (delta - mod) * 100 / delta

  ret_val= []

  for i in range(0,4):
    ret_val.append( ( color_list[left][i] * left_weight + color_list[right][i] * right_weight) / 100 )

  return ( ret_val[0], ret_val[1], ret_val[2], ret_val[3])

# wind color

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
#  if(am == 'AM' or am == 'am'):
#    if(hours == 12):
#      hours = 0
#  else:
#    if(hours != 12):
#      hours = hours + 12
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

wind_temp_file = open('hourly.json')
weather = json.load(wind_temp_file)
wind_temp_file.close()

#
# establish range of each field
#

high_temp = 0
low_temp = 200

for j in range(0,23):
  temperature = int(weather[j]['Temperature'])
  if high_temp < temperature:
    high_temp = temperature
  if low_temp > temperature:
    low_temp = temperature


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
#  high_temp = 100
#  low_temp = 0
  high_temp = 73
  low_temp = 53
  val = weather[now.hour]['Temperature']
  val = 70
#  if weather[now.hour-1]['Temperature'] > val:
#    val = val * -1
  val_range = high_temp - low_temp
  print str(high_temp)+':'+str(val)+':'+str(low_temp)

  if(val > 0 ):
    beg = 0 
    relative_end = val - low_temp
    end = 360 * relative_end / val_range
  else:
    end = 0
    relative_beg = high_temp - val
    beg = 360 * relative_beg / val_range

  left_corner =  shape
  right_corner = 300 - shape*25

#  color = map_color_value(abs(val), 100)
  color = map_color_value(abs(val), 100)
  image = Image.new('RGBA',(shape,shape),(0,0,0,0))
  draw = ImageDraw.Draw(image)
  draw.pieslice((0, 0, shape, shape), beg-90, end-90, color, 'black')
  return image

def draw_wind_ring(shape):
  image = Image.new('RGBA',(shape,shape),(0,0,0,0))
  draw = ImageDraw.Draw(image)
  max_speed = 18
  wedge = 360 / 24
  for i in range(0,24):
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
#  num_wedges = 200
#  delta_hour = num_wedges / 24
#  wedge = 36000 / num_wedges
  for j in range(0,num_wedges):
    first = ((j*100)/num_wedges) * 24/100
    beg = wedge * j / 100
    end = (j+1) * wedge / 100
    if(first == 23):
      second = 0
    else:
      second = first + 1
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
#  num_wedges = 200
#  delta_hour = num_wedges / 24
#  wedge = 36000 / num_wedges
  for j in range(0,num_wedges):
    first = ((j*100)/num_wedges) * 24/100
    beg = wedge * j / 100
    end = (j+1) * wedge / 100
    if(first == 23):
      second = 0
    else:
      second = first + 1
    delta_B = j % delta_hour
    delta_A = delta_hour - delta_B
    humid1 = int(weather[first]['Humidity'])
    humid2 = int(weather[second]['Humidity'])
    humid = (humid1*100*delta_A + humid2*100*delta_B) / delta_hour
    color = get_color(humid/100, (0,100)) #(0,0,0,255*speed/8)
    draw.pieslice((0,0,shape,shape), beg, end, color, color)
  return image

#temp_ring = draw.ellipse(ring_shape(0),'blue','blue')
img = draw_temp_ring(ring_size(0))
image.paste(img, ring_shape(0), img)

wind_ring = draw.ellipse(ring_shape(1),'red','blue')
img = wind_speed(ring_size(1))
image.paste(img, ring_shape(1), img)

#wind_ring = draw.ellipse(ring_shape(1),'red','blue')
img = draw_wind_ring(ring_size(1))
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

print now
current_time = convert_time_to_minutes(now.hour, now.minute, 'am')#(4, 45, 'PM')
xxx = image.rotate(0)#(360*current_time/min_per_day + 90)

image2 = Image.new('RGBA',(window_size,window_size),(0,0,0,255))
image2.paste(xxx,ring_shape(0),xxx)
image2.save(sys.argv[1])
image2.show()
