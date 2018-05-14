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
  max_tide = 200
  min_tide = 0
  feet = feet + 40
  tidal_range = max_tide - min_tide
  retval = 33+66*(feet - min_tide)/tidal_range
  return retval

#
# construct today's image
#

now = datetime.datetime.now()
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
    return time/100*60 + time%60

moon_rise = time_to_min(sun_moon[day]['MoonRise'])
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
tides = sun_moon

first_high = relative_tide_position(tides[day]['HighTide'][0]['Height'])
second_high = relative_tide_position(tides[day]['HighTide'][1]['Height'])
first_low = relative_tide_position(tides[day]['LowTide'][0]['Height'])
second_low = relative_tide_position(tides[day]['LowTide'][1]['Height'])

first_high_time = time_to_min(tides[day]['HighTide'][0]['Time'])
second_high_time = time_to_min(tides[day]['HighTide'][1]['Time'])
first_low_time = time_to_min(tides[day]['LowTide'][0]['Time'])
second_low_time = time_to_min(tides[day]['LowTide'][1]['Time'])

half_day = convert_time_to_minutes(11, 59, 'am')
delta_high = (second_high_time - first_high_time - half_day) / 2
delta_low = (second_low_time - first_low_time - half_day) / 2

def draw_quad(first, second, second_time, delta, tide_color):
  size = tide_space
  color = tide_color
  image = Image.new('RGBA', (size, size), (0,0,0,0))
  draw = ImageDraw.Draw(image)
  length = size*second/100
  height = size*first/100
  x_dist = (size-length)/2
  y_dist = (size-height)/2
  delta_degrees = 360 * delta / min_per_day
  draw.pieslice((x_dist, y_dist, size-x_dist, size-y_dist), 0, 90+delta_degrees, color, 'black')
  tide = image
  rotation_factor = -360*second_time/min_per_day
  tide1 = tide.rotate(rotation_factor)
  return tide1

num_tidal_wedges = 20
width_tidal_wedge = 360 / num_tidal_wedges

def draw_tide_quad(size, low_height, high_height, end, color):
  image = Image.new('RGBA', (size, size), (0,0,0,0))
  draw = ImageDraw.Draw(image)
  length = size*high_height/100
  height = size*low_height/100
  x_dist = (size-length)/2
  y_dist = (size-height)/2
#  draw.ellipse((x_dist, y_dist, size-x_dist, size-y_dist), color, 'black')
  draw.pieslice((x_dist, y_dist, size-x_dist, size-y_dist), 0, end, color, 'black')
  return image

def draw_tidal_arc(start, end):
  size = tide_space
  image = Image.new('RGBA', (size, size), (0,0,0,0))
  draw = ImageDraw.Draw(image)
  tide_color = (0, 0, 0, 200)
  beg_length = size * start[1] / 100
  end_length = size * end[1] / 100
  x_start = (size-end_length)/2
  y_start = (size-beg_length)/2
  print 'size = '+str(size)
  print 'beg_length = '+str(beg_length)
  print 'end_length = '+str(end_length)
  print 'x_start = '+str(x_start)
  print 'y_start = '+str(y_start)

  start_arc = 360*start[0]/min_per_day
  end_arc = 360*end[0]/min_per_day
#  draw.pieslice((x_start, y_start, x_start+end_length, y_start + beg_length), start_arc, end_arc, tide_color, tide_color)
#  return image
  num_arc = abs(start_arc - end_arc) / width_tidal_wedge
  delta_length = (end_length - beg_length) / num_arc

  beg_arc = start_arc
  for i in range(0,num_arc):

    end_arc = beg_arc + width_tidal_wedge
    end_length = beg_length + delta_length

    x_start = (size-end_length)/2
    y_start = (size-beg_length)/2
    print '  beg_length = '+str(beg_length)
    print '  end_length = '+str(end_length)
    print '  x_start = '+str(x_start)
    print '  y_start = '+str(y_start)
    draw.pieslice((x_start, y_start, x_start+end_length, y_start + beg_length), beg_arc, end_arc, tide_color, tide_color)
#    tmp = draw_tide_quad(size, low, high, width_tidal_wedge, tide_color).rotate(beg)
#    tmp = draw_delta_arc(beg_arc, end_arc, beg_length, end_length)
#    image.paste(tmp, high_tidal_ring, tmp)
    beg_arc = end_arc
    beg_length = end_length
  return image#.rotate(-start_arc)

# construct each tidal wedge and paste 

if(first_high_time > first_low_time):  #  build counter clockwise
  print "first path "+str(tides[day]['LowTide'])
  print "first path "+str(tides[day]['HighTide'])
  tide_color = (0, 0, 0, 200)
  start = (first_high_time, first_high)
  end = (first_low_time, first_low)
#  start = (6*60, 95)
#  end = (9*60, 70)
  
  tide1 = draw_tidal_arc(start, end)
  image.paste(tide1, high_tidal_ring, tide1)
#  tide_color = (0, 0, 0, 200)
#  tide1 = draw_quad(first_high, first_low, first_low_time, 0, (0,0,0,200))
#  image.paste(tide1, high_tidal_ring, tide1)
#  
#  tide1 = draw_quad(first_low, second_high, second_high_time, 0, (0,0,0,200))
#  image.paste(tide1, high_tidal_ring, tide1)
#  
#  tide1 = draw_quad(second_high, second_low, second_low_time, 0, (0,0,0,200))
#  image.paste(tide1, high_tidal_ring, tide1)
#  
#  tide1 = draw_quad(second_low, first_high, first_high_time, 0, (0,0,0,200))
#  image.paste(tide1, high_tidal_ring, tide1)
else:
  print "second path "+str(delta_low)+" "+str(delta_high)
  tide_color = (0, 0, 0, 200)
  start = (first_high_time, first_high)
  end = (first_low_time, first_low)
  
  tide1 = draw_tidal_arc(start, end)
  image.paste(tide1, high_tidal_ring, tide1)
  
#  tide1 = draw_quad(first_low, first_high, first_high_time, 0, tide_color)
#  image.paste(tide1, high_tidal_ring, tide1)
#  
#  tide1 = draw_quad(first_high, second_low, second_low_time, 0, tide_color)
#  image.paste(tide1, high_tidal_ring, tide1) 
#
#  tide1 = draw_quad(second_low, second_high, second_high_time, 0, tide_color)
#  image.paste(tide1, high_tidal_ring, tide1)
#  
#  tide1 = draw_quad(second_high, first_low, first_low_time, 0, tide_color)
#  image.paste(tide1, high_tidal_ring, tide1)

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

current_time = convert_time_to_minutes(now.hour, now.minute, 'am')#(4, 45, 'PM')
xxx = image#.rotate(360*current_time/min_per_day + 90)

image2 = Image.new('RGBA',(window_size,window_size),(0,0,0,255))
image2.paste(xxx,ring_shape(0),xxx)
image2.show()
