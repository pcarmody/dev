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

cloud_color_list = (
#    (0, 0, 255, 255),   # Bright Blue,
#    (0x87, 0xce, 0xeb, 255),   # sky blue #87ceeb
    (0x00, 0xbf, 0xff, 255),   # sky blue ##00bfff
    (255, 255, 255, 255), # Black,
    (0, 0, 0, 255),     # White,
    (0, 0, 0, 255),
)
cloud_color_count = 2

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
  red = trans * red / 100
  green = trans * green / 100
  blue = trans * blue / 100
  return (red, green, blue, 255)

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

def get_cloud_color_value(value, scope):
        
  delta = scope / cloud_color_count           # how wide the wedge of color is
  left = value / delta                  # the color of the wedge
#  right = (left + 1) % color_count      # the next color
  right = (left + 1)                     # the next color
  mod = value % delta                   # how deep into the wedge of color
  
  right_weight = mod * 100 / delta      
  left_weight = (delta - mod) * 100 / delta

  ret_val= []

  for i in range(0,4):
    ret_val.append( ( cloud_color_list[left][i] * left_weight + cloud_color_list[right][i] * right_weight) / 100 )

  return ( ret_val[0], ret_val[1], ret_val[2], ret_val[3])

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
  image = Image.new('RGBA',(shape,shape),(0,0,0,0))
  draw = ImageDraw.Draw(image)
#  num_wedges = 300
#  delta_hour = num_wedges / 24
#  wedge = 36000 / num_wedges
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
    temp1 = int(weather[first]['Temperature'])
    temp2 = int(weather[second]['Temperature'])
#    print str(temp1*100)+':'+str(temp2*100)
    temp = (temp1*100*delta_A + temp2*100*delta_B) / delta_hour
#    print str(j)+':'+str(first)+':'+str(temp)+':'+str(beg)+':'+str(end)
#    color = get_color(10000-temp, (2000, 10000)) 
    color = map_color_value(temp-1000, 10000)
    draw.pieslice((0,0,shape,shape), beg, end, color, color)
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
    speed_factor = (speed*100)/max_speed
    if(dirstr == 'Calm'):
      color = (0, 0, 0, speed_color)
    else:
      direction = 0
      tmp = 0
      for j in ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW' ]:
        if(j == dirstr):
          direction = tmp
        tmp = tmp + 1
      color = get_white_color(direction, (0,15), speed_factor)

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

def cloud_ring(shape):
  image = Image.new('RGBA',(shape,shape),(0,0,0,0))
  draw = ImageDraw.Draw(image)
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
    cloud1 = int(weather[first]['Condition'])
    cloud2 = int(weather[second]['Condition'])
    cloud = (cloud1*100*delta_A + cloud2*100*delta_B) / delta_hour
    color = get_cloud_color_value(cloud, 900) 
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

img = cloud_ring(ring_size(4))
image.paste(img, ring_shape(4), img)

precip_tide = draw.ellipse(ring_shape(5),'black','blue')

#draw hourly lines
for beg in [0, 60, 120, 180, 240, 300]:
  image3 = add_lines(beg, beg+90)
  image.paste(image3, ring_shape(0), image3)

# rotate the entire image based on the current time.

print now
current_time = convert_time_to_minutes(now.hour, now.minute, 'am')#(4, 45, 'PM')
xxx = image.rotate(360*current_time/min_per_day + 90)

image2 = Image.new('RGBA',(window_size,window_size),(0,0,0,255))
image2.paste(xxx,ring_shape(0),xxx)
image2.save(sys.argv[1])
#image2.show()
