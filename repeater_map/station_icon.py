from PIL import Image
from PIL import ImageDraw
import datetime
import json
import sys

freq = float(sys.argv[1])

CTCSS_tone = 0.0
DCS_tone = 0 

if '.' in sys.argv[2]:
  CTCSS_tone = float(sys.argv[2])
else:
  DCS_tone = int(sys.argv[2])

window_size = 40

image = Image.new('RGBA',(window_size,window_size),(0,0,0,255))
draw = ImageDraw.Draw(image)

def ring_size(level):
  percentage = window_size * 30/100
  return window_size - (level * percentage)

def ring_disp(level):
  percentage = window_size * 15/100
  return level * percentage

def ring_shape(level):
  disp = ring_disp(level)
  size = ring_size(level)
  retval = (disp, disp, size+disp, size+disp)
  return retval

CTCSS_bottom = 67.0
CTCSS_top = 254.1
CTCSS_range = CTCSS_top - CTCSS_bottom

DCS_bottom = 6
DCS_top = 754
DCS_range = DCS_top - DCS_bottom

bandplan_file = open("bandplan.csv")

#while(row = bandplan_file.readline()):
bandplan = []
for row in bandplan_file:
  entries = row.split(",")
  if entries[0] == "Name":
    continue
  bandplan.append(entries)
  if float(entries[1]) < freq:
    band_name = entries[0]
    band_color = (int(entries[4], 16), int(entries[5], 16), int(entries[6], 16), 252)
    band_bottom = float(entries[1])
    band_top = float(entries[2])
    band_range = band_top - band_bottom

  print band_name+", "+str(band_color)+", "+str(band_range)

freq_space = ring_size(0)
freq_disp = ring_disp(0)
sun_space = ring_size(1)
sun_disp = ring_disp(1)
tide_space = ring_size(2) 
tide_disp = ring_disp(2)

def draw_halves(size, rise_angle, set_angle, day_color, night_color):
  image = Image.new('RGBA', (size, size), (0,0,0,0))
  draw = ImageDraw.Draw(image)
#  rise_angle = 360 * freq_rise / min_per_day
#  set_angle = 360 * freq_set / min_per_day
  black = (255, 255, 255, 0)
  draw.pieslice((0,0,size, size), rise_angle, set_angle, day_color, day_color)
  draw.pieslice((0,0,size, size), set_angle, rise_angle, night_color, night_color)
  return image

#
# construct today's image
#

ring_number = 0

today = datetime.date.today()
birthday = datetime.date(1973, 7, 14)
days_alive = today - birthday

def draw_circle(level, repeat, day_color, night_color):
  half_repeat = repeat / 2 
  days = days_alive.days - half_repeat
  first_mod = days % repeat
  degrees = (first_mod - half_repeat) * 360 / half_repeat
  if(degrees > 0):
    freq = draw_halves(ring_size(level), 0, degrees, day_color, night_color)
  else:
    freq = draw_halves(ring_size(level), 0, degrees, night_color, day_color)
  return freq

night_color = (0,0,0,0)
def draw_freq_arc():
  degrees = ( freq - band_bottom ) * 360 / band_range
  freq_ring = draw_halves(ring_size(0), 0, degrees, band_color, night_color)
  return freq_ring

def draw_tone_arc():
  if CTCSS_tone > 0.0:
    degrees = ( CTCSS_tone - CTCSS_bottom ) * 260 / CTCSS_range
    color = 'violet'
  else:
    degrees = ( DCS_tone - DCS_bottom ) * 260 / DCS_range
    color = 'orange'
  tone_ring = draw_halves(ring_size(1), 0, -degrees, color, night_color)
  return tone_ring

def draw_center():
  return draw_halves(ring_size(2), 0, 360, "green", night_color)

freq = draw_freq_arc()
image.paste(freq, ring_shape(0), freq)

tone = draw_tone_arc()
image.paste(tone, ring_shape(1), tone)

center = draw_center()
image.paste(center, ring_shape(2), center)

# rotate the entire image based on the current time.
#image.rotate(90).show()

file_name = "icons/stations/" + sys.argv[1] + "_" + sys.argv[2] + ".png"
image.rotate(90).save(file_name);
