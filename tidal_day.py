from PIL import Image
from PIL import ImageDraw
import datetime
import json

month = 5
day = 6
year = 63
window_size = 400

image = Image.new('RGBA',(window_size,window_size),(0,0,0,0))
draw = ImageDraw.Draw(image)

def ring_size(level):
  percentage = window_size * 20/100
  return window_size - (level * percentage)

def ring_disp(level):
  percentage = window_size * 10/100
  return level * percentage

def ring_shape(level):
  disp = ring_disp(level)
  size = ring_size(level)
  retval = (disp, disp, size+disp, size+disp)
  return retval

min_per_day = 60*24
moon_space = ring_size(0)
moon_disp = ring_disp(0)
sun_space = ring_size(1)
sun_disp = ring_disp(1)
tide_space = ring_size(2) 
tide_disp = ring_disp(2)

highest_high_tide = 6
lowest_low_tide = 0

def convert_time_to_minutes(hours, minutes, am):
  if(am == 'AM' or am == 'am'):
    if(hours == 12):
      hours = 0
  else:
    hours = hours + 12
  return hours * 60 + minutes

def draw_halves(size, moon_rise, moon_set, day_color, night_color):
  image = Image.new('RGBA', (size, size), (0,0,0,0))
  draw = ImageDraw.Draw(image)
  rise_angle = 360 * moon_rise / min_per_day
  set_angle = 360 * moon_set / min_per_day
  draw.pieslice((0,0,size, size), rise_angle, set_angle, day_color, 'black')
  draw.pieslice((0,0,size, size), set_angle, rise_angle, night_color, 'black')
  return image

def draw_tide_quad(size, low_height, high_height, color):
  image = Image.new('RGBA', (size, size), (0,0,0,0))
  draw = ImageDraw.Draw(image)
  length = size*high_height/100
  height = size*low_height/100
  x_dist = (size-length)/2
  y_dist = (size-height)/2
#  draw.ellipse((x_dist, y_dist, size-x_dist, size-y_dist), color, 'black')
  draw.pieslice((x_dist, y_dist, size-x_dist, size-y_dist), -10, 100, color, 'black')
  return image

def relative_tide_position(feet):
  max_tide = 60
  min_tide = -10
  tidal_range = max_tide - min_tide
  retval = 33+66*(feet - min_tide)/tidal_range
  return retval

#
# retrieve the sun and moon data
#

sun_moon_file = open('/home/paul/bin/data/sunmoon_201803')
sun_moon = json.load(sun_moon_file)
sun_moon_file.close()

#
# construct today's image
#

now = datetime.datetime.now()

moon_rise = sun_moon[now.day]['MoonRise'][0].split(':')
moon_rise_am = sun_moon[now.day]['MoonRise'][1]
moon_rise = convert_time_to_minutes(int(moon_rise[0]), int(moon_rise[1]), moon_rise_am)
moon_set = sun_moon[now.day]['MoonSet'][0].split(':')
moon_set_am = sun_moon[now.day]['MoonSet'][1]
moon_set = convert_time_to_minutes(int(moon_set[0]), int(moon_set[1]), moon_set_am)
moon = draw_halves(moon_space, moon_rise, moon_set, 'white', 'black')
image.paste(moon, ring_shape(0), moon)

sun_rise = sun_moon[now.day]['SunRise'][0].split(':')
sun_rise_am = sun_moon[now.day]['SunRise'][1]
sun_rise = convert_time_to_minutes(int(sun_rise[0]), int(sun_rise[1]), sun_rise_am)
sun_set = sun_moon[now.day]['SunSet'][0].split(':')
sun_set_am = sun_moon[now.day]['SunSet'][1]
sun_set = convert_time_to_minutes(int(sun_set[0]), int(sun_set[1]), sun_set_am)
sun = draw_halves(sun_space, sun_rise, sun_set, 'yellow', 'brown')
image.paste(sun, ring_shape(1), sun)

# draw the tidal background
high_tidal_ring = ring_shape(2)
low_tidal_ring = ring_shape(3)
high_tide = draw.ellipse(high_tidal_ring,'blue','blue')
low_tide = draw.ellipse(low_tidal_ring,'red','blue')
lowest_tide = draw.ellipse(ring_shape(4),'black','blue')

# retrieve tidal information
tides_file = open('/home/paul/bin/data/tides_201803')
tides = json.load(tides_file)
tides_file.close()

first_high = relative_tide_position(int(float(tides[now.day]['High_1_Height'])*10.0))
second_high = relative_tide_position(int(float(tides[now.day]['High_2_Height'])*10.0))
first_low = relative_tide_position(int(float(tides[now.day]['Low_1_Height'])*10.0))
second_low = relative_tide_position(int(float(tides[now.day]['Low_2_Height'])*10.0))

def parse_tidal_time(in_time):
  tmp_time = in_time.split(':')
  hours = int(tmp_time[0])
  minutes = int(tmp_time[1].split(' ')[0])
  am = tmp_time[1].split(' ')[1]
  return (hours, minutes, am)

tmp = parse_tidal_time(tides[now.day]['High_1_Time'])
first_high_time = convert_time_to_minutes(tmp[0], tmp[1], tmp[2])#
tmp = parse_tidal_time(tides[now.day]['High_2_Time'])
second_high_time = convert_time_to_minutes(tmp[0], tmp[1], tmp[2])#(11, 7, 'PM')
tmp = parse_tidal_time(tides[now.day]['Low_1_Time'])
first_low_time = convert_time_to_minutes(tmp[0], tmp[1], tmp[2])#(4, 10, 'AM')
tmp = parse_tidal_time(tides[now.day]['Low_2_Time'])
second_low_time = convert_time_to_minutes(tmp[0], tmp[1], tmp[2])#(4, 39, 'PM')

def draw_quad(first, second, second_time, tide_color):
  tide = draw_tide_quad(tide_space, first, second, tide_color)
  rotation_factor = -360*second_time/min_per_day
  tide1 = tide.rotate(rotation_factor)
  return tide1

# construct each tidal wedge and paste 

if(first_high_time > first_low_time):  #  build counter clockwise
  tide_color = (0, 0, 0, 200)
  tide1 = draw_quad(first_high, first_low, first_low_time, tide_color)
  image.paste(tide1, high_tidal_ring, tide1)
  
  tide1 = draw_quad(first_low, second_high, second_high_time, tide_color)
  image.paste(tide1, high_tidal_ring, tide1)
  
  tide1 = draw_quad(second_high, second_low, second_low_time, tide_color)
  image.paste(tide1, high_tidal_ring, tide1)
  
  tide1 = draw_quad(second_low, first_high, first_high_time, tide_color)
  image.paste(tide1, high_tidal_ring, tide1)
else:
  tide1 = draw_quad(first_low, first_high, first_high_time, tide_color)
  image.paste(tide1, high_tidal_ring, tide1)
  
  tide1 = draw_quad(first_high, second_low, second_low_time, tide_color)
  image.paste(tide1, high_tidal_ring, tide1)
  
  tide1 = draw_quad(second_low, second_high, second_high_time, tide_color)
  image.paste(tide1, high_tidal_ring, tide1)
  
  tide1 = draw_quad(second_high, first_low, first_low_time, tide_color)
  image.paste(tide1, high_tidal_ring, tide1)

#tide = draw_tide_quad(tide_space, first_low, first_high, tide_color)
#first_high_rotation_factor = -360*first_high_time/min_per_day
#tide1 = tide.rotate(first_high_rotation_factor)
#image.paste(tide1, high_tidal_ring, tide1)

#tide = draw_tide_quad(tide_space, first_high, second_low, tide_color)
#first_low_rotation_factor = -360*second_low_time/min_per_day
#tide1 = tide.rotate(first_low_rotation_factor)
#image.paste(tide1, high_tidal_ring, tide1)
#
#tide = draw_tide_quad(tide_space, second_low, second_high, tide_color)
#second_high_rotation_factor = -360*second_high_time/min_per_day
#tide1 = tide.rotate(second_high_rotation_factor)
#image.paste(tide1, high_tidal_ring, tide1)
#
#tide = draw_tide_quad(tide_space, second_high, first_low, tide_color)
#second_low_rotation_factor = -360*first_low_time/min_per_day
#tide1 = tide.rotate(second_low_rotation_factor)
#image.paste(tide1, high_tidal_ring, tide1)

# rotate the entire image based on the current time.
current_time = convert_time_to_minutes(now.hour, now.minute, 'am')#(4, 45, 'PM')
image.rotate(360*current_time/min_per_day + 90).show()
