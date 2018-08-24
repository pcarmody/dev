from PIL import Image
from PIL import ImageDraw
from PIL import ImageColor
import datetime
import json
import sys
from os.path import expanduser
home = expanduser("~")

window_size = 400
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
    if(hours != 12):
      hours = hours + 12
  return hours * 60 + minutes

def draw_halves(size, moon_rise, moon_set, day_color):
  image = Image.new('RGBA', (size, size), (0,0,0,0))
  draw = ImageDraw.Draw(image)
  rise_angle = 360 * moon_rise / min_per_day
  set_angle = 360 * moon_set / min_per_day
  night_color = (day_color[0]/4, day_color[1]/4, day_color[2]/4)
  draw.pieslice((0,0,size, size), set_angle, rise_angle, night_color, 'black')
  draw.pieslice((0,0,size, size), rise_angle, set_angle, day_color, 'black')
  return image

def relative_tide_position(feet):
  max_tide = 185
  min_tide = -50
#  feet = feet + 40
  tidal_range = max_tide - min_tide
  retval = 100*(feet - min_tide)/tidal_range
  return retval

#
# construct today's image
#

now = datetime.datetime.now()
print now
day = now.day
month = now.month
year = now.year

#
# retrieve the sun and moon data
#

sun_moon_file = open(home+'/bin/data/lunar_info_'+str(year)+("%0.02d" % month))
sun_moon = json.load(sun_moon_file)
sun_moon_file.close()

i = 0
while day != sun_moon[i]['Date']:
  i = i + 1

day = i

def time_to_min(time):
    return (time/100)*60 + time%100

moon_rise = time_to_min(sun_moon[day]['MoonRise'])
moon_set = (moon_rise + 1200) % 2400

if 'MoonSet' in sun_moon[day]:
  moon_set = time_to_min(sun_moon[day]['MoonSet'])

moon_color = ImageColor.getrgb('white')

if(moon_rise < moon_set):
  moon = draw_halves(moon_space, moon_set, moon_rise, moon_color)
else:
  moon = draw_halves(moon_space, moon_rise, moon_set, moon_color)
image.paste(moon, ring_shape(0), moon)

sun_rise = time_to_min(sun_moon[day]['SunRise'])
sun_set = time_to_min(sun_moon[day]['SunSet'])
sun_color = ImageColor.getrgb('yellow')
sun = draw_halves(sun_space, sun_rise, sun_set, sun_color)
image.paste(sun, ring_shape(1), sun)

# draw the tidal background
high_tidal_ring = ring_shape(2)
low_tidal_ring = ring_shape(3)
high_tide = draw.ellipse(high_tidal_ring,'blue','blue')
low_tide = draw.ellipse(low_tidal_ring,'red','blue')
lowest_tide = draw.ellipse(ring_shape(4),'black','blue')

# retrieve tidal information
#tides_file = open(home+'/bin/data/tides_201803')
#tides_file = open(home+'/bin/data/tides_'+str(year)+("%0.02d" % month))
#tides = json.load(tides_file)
#tides_file.close()
#tides = sun_moon

tides = [0] * 4
tides[0] = {}
tides[1] = {}
tides[2] = {}
tides[3] = {}

tides[0]['Time'] = time_to_min(sun_moon[day]['HighTide'][0]['Time'])
tides[0]['Height'] = relative_tide_position(sun_moon[day]['HighTide'][0]['Height'])
#tides[1]['Time'] = tides[0]['Time']
#tides[1]['Height'] = tides[0]['Height']
#if 1 in sun_moon[day]['HighTide'][1]:
tides[1]['Time'] = time_to_min(sun_moon[day]['HighTide'][1]['Time'])
tides[1]['Height'] = relative_tide_position(sun_moon[day]['HighTide'][1]['Height']) 

tides[2]['Time'] = time_to_min(sun_moon[day]['LowTide'][0]['Time'])
tides[2]['Height'] = relative_tide_position(sun_moon[day]['LowTide'][0]['Height'])
#tides[3]['Time'] = tides[2]['Time']
#tides[3]['Height'] = tides[2]['Height']
#if 1 in sun_moon[day]['LowTide']:
tides[3]['Time'] = time_to_min(sun_moon[day]['LowTide'][1]['Time'])
tides[3]['Height'] = relative_tide_position(sun_moon[day]['LowTide'][1]['Height'])

# sort the tidal data by time of day.

for i in [0, 1, 2]:
  for j in range(i,4):
    if(tides[i]['Time'] > tides[j]['Time']):
      tmp = tides[i]
      tides[i] = tides[j]
      tides[j] = tmp
print str(sun_moon[day])
print str(tides)
half_day = convert_time_to_minutes(11, 59, 'am')
num_tidal_wedges = 360
width_tidal_wedge = 360 / num_tidal_wedges

def get_weighted_avg_height(now):
  if(now <= tides[0]['Time']):
    when = "  pre-morning"
    i = -1
    left_time = tides[3]['Time'] - min_per_day
    left_height = tides[3]['Height']
    right_time = tides[0]['Time']
    right_height = tides[0]['Height']
  elif(now <= tides[1]['Time']):
    when = "  morning"
    i = 1
    left_time = tides[0]['Time']
    left_height = tides[0]['Height']
    right_time = tides[1]['Time']
    right_height = tides[1]['Height']
  elif(now <= tides[2]['Time']):
    when = "  noon"
    i = 0
    left_time = tides[1]['Time']
    left_height = tides[1]['Height']
    right_time = tides[2]['Time']
    right_height = tides[2]['Height']
  elif(now <= tides[3]['Time']):
    when = "  afternoon"
    i = 0
    left_time = tides[2]['Time']
    left_height = tides[2]['Height']
    right_time = tides[3]['Time']
    right_height = tides[3]['Height']
  else:
    when = "  night"
    i = 3
    left_time = tides[3]['Time']
    left_height = tides[3]['Height']
    right_time = min_per_day + tides[0]['Time']
    right_height = tides[0]['Height']

  space_between = (right_time - left_time)
  delta_B = (right_time - now) * 100 / space_between
  delta_A = (now - left_time) * 100 / space_between

  lowest = left_height
  highest = right_height
  if lowest > right_height:
    lowest = right_height
  if highest < left_height:
    highest = left_height

  retval =  (left_height * delta_B + right_height * delta_A) / 100

  if retval < lowest:
    return lowest
  if retval > highest:
    return highest
  return retval

tidal_image = Image.new('RGBA',(tide_space, tide_space),(0,0,0,0))
tidal_draw = ImageDraw.Draw(tidal_image)
tidal_color = (0,0,0, 200)
delta_time = min_per_day / num_tidal_wedges
arc_time = 0
beg = 0

for i in range(0,num_tidal_wedges):
  height = 100 - get_weighted_avg_height(arc_time)
  inner_ring = ring_size(4)
  outer_ring = ring_size(1)
  height = (inner_ring - outer_ring) * height/ 100 + inner_ring

  x_dist = (ring_size(4) - height)/2
  tide_arc_box = (x_dist, x_dist, tide_space-x_dist, tide_space-x_dist)

  end = beg + width_tidal_wedge 

  tidal_draw.pieslice(tide_arc_box, beg, end, tidal_color, tidal_color)

  arc_time = arc_time + delta_time
  beg = end

image.paste(tidal_image, high_tidal_ring, tidal_image)

def add_lines(beg, end):
  image3 = Image.new('RGBA',(window_size,window_size),(0,0,0,0))
  draw3 = ImageDraw.Draw(image3)
  non_color = (0, 0, 0, 0)
  line_color = (0, 0, 0, 50)
  if(beg % 90 == 0):
    line_color = (0,0,0,255)
  draw3.pieslice(ring_shape(0), beg, end, non_color, line_color)
  return image3

#draw hourly lines
for beg in [0, 60, 120, 180, 240, 300]:
  image3 = add_lines(beg, beg+90)
  image.paste(image3, ring_shape(0), image3)

# rotate the entire image based on the current time.

if(now.hour == 12):
  current_time = convert_time_to_minutes(now.hour, now.minute, 'pm')#(4, 45, 'PM')
else:
  current_time = convert_time_to_minutes(now.hour, now.minute, 'am')#(4, 45, 'PM')
xxx = image.rotate(360*current_time/min_per_day + 90)

image2 = Image.new('RGBA',(window_size,window_size),(0,0,0,255))
image2.paste(xxx,ring_shape(0),xxx)
image2.save(sys.argv[1])
image2.show()
