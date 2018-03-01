from PIL import Image
from PIL import ImageDraw

name = 'RGBA'
month = 5
day = 6
year = 63

image = Image.new(name,(200,200),'black')
draw = ImageDraw.Draw(image)
#moon = draw.ellipse((0,0,200,200),'white','blue')
moon_day = draw.pieslice((0,0,200,200), 0, 180, 'white', 'blue')
moon_night = draw.pieslice((0,0,200,200), 180, 360, 'black', 'blue')
#sun = draw.ellipse((20,20,180,180),'yellow','blue')
sun_day = draw.pieslice((20,20,180,180),90, 270, 'yellow','blue')
sun_night = draw.pieslice((20,20,180,180),-90, 90, 'brown','blue')
high_tide = draw.ellipse((40,40,160,160),'blue','blue')
low_tide = draw.ellipse((60,60,140,140),'red','blue')
#tides = draw.ellipse((65,45,135,155),'black','blue')
# X1 = 60- todays-low - lowest-low
# Y1 = 40+ highest-high - todays-high
# X2 = 140+ todays-2ndlow - lowest-low
# Y2 = 160- highest-high - days-2ndhigh
#king_tides = draw.ellipse((80,40,120,160),'black','blue')
tmp_image = Image.new('RGBA', (120,120), (0,0,0,0))
tmp_draw = ImageDraw.Draw(tmp_image)
#king_tides = draw.ellipse((40,80,160,120),'black','blue')
king_tides = tmp_draw.ellipse((0,40,120,80),'black','blue')
tmp2 = tmp_image.rotate(45)

image.paste(tmp2, (40,40,160,160), tmp2)

image.show()
