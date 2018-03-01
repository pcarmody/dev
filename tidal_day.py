from PIL import Image
from PIL import ImageDraw

month = 5
day = 6
year = 63

image = Image.new('RGBA',(200,200),'black')
draw = ImageDraw.Draw(image)

min_per_day = 60*24
moon_space = 200
moon_disp = 0
sun_space = 160
sun_disp = 20
tide_space = 120
tide_disp = 40

highest_high_tide = 6
lowest_low_tide = 0

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
  draw.pieslice((x_dist, y_dist, size-x_dist, size-y_dist), 0, 120, color, 'black')
  return image

moon = draw_halves(moon_space, min_per_day/5, min_per_day*3/4, 'white', 'black')
image.paste(moon, (moon_disp,moon_disp,moon_space,moon_space), moon)
sun_rise = 0
sun_set = min_per_day/2
sun = draw_halves(sun_space, sun_rise, sun_set, 'yellow', 'brown')
image.paste(sun, (20,20, 180, 180), sun)

# draw the tidal background
high_tide = draw.ellipse((40,40,160,160),'blue','blue')
low_tide = draw.ellipse((60,60,140,140),'red','blue')

first_high = 95
second_high = 85
first_low = 55
second_low = 60
tide = draw_tide_quad(tide_space, first_low, first_high, (0, 0, 0, 100))
tide1 = tide.rotate(0)
image.paste(tide1, (40, 40, 160, 160), tide1)
tide = draw_tide_quad(tide_space, first_high, second_low, (0, 0, 0, 150))
tide1 = tide.rotate(90)
image.paste(tide1, (40, 40, 160, 160), tide1)
tide = draw_tide_quad(tide_space, second_low, second_high, (0, 0, 0, 200))
tide1 = tide.rotate(180)
image.paste(tide1, (40, 40, 160, 160), tide1)
tide = draw_tide_quad(tide_space, second_high, first_low, (0, 0, 0, 250))
tide1 = tide.rotate(270)
image.paste(tide1, (40, 40, 160, 160), tide1)

#sun = draw.ellipse((20,20,180,180),'yellow','blue')
#sun_day = draw.pieslice((20,20,180,180),90, 270, 'yellow','blue')
#sun_night = draw.pieslice((20,20,180,180),-90, 90, 'brown','blue')
#high_tide = draw.ellipse((40,40,160,160),'blue','blue')
#low_tide = draw.ellipse((60,60,140,140),'red','blue')
##tides = draw.ellipse((65,45,135,155),'black','blue')
## X1 = 60- todays-low - lowest-low
## Y1 = 40+ highest-high - todays-high
## X2 = 140+ todays-2ndlow - lowest-low
## Y2 = 160- highest-high - days-2ndhigh
##king_tides = draw.ellipse((80,40,120,160),'black','blue')
#tmp_image = Image.new('RGBA', (120,120), (0,0,0,0))
#tmp_draw = ImageDraw.Draw(tmp_image)
##king_tides = draw.ellipse((40,80,160,120),'black','blue')
#king_tides = tmp_draw.ellipse((0,40,120,80),'black','blue')
#tmp2 = tmp_image.rotate(45)
#
#image.paste(tmp2, (40,40,160,160), tmp2)

image.show()
