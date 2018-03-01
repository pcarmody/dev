from PIL import Image
from PIL import ImageDraw

name = 'RGB'
month = 5
day = 6
year = 63

image = Image.new(name,(200,200),'black')
draw = ImageDraw.Draw(image)
#draw.ellipse((0,0,90,90),'yellow','blue')
#draw.ellipse((25,20,35,30),'yellow','blue')
#draw.ellipse((50,20,60,30),'yellow','blue')
#draw.arc((20,40,70,70), 0, 180, 'red') #draw circle in black
#  cooridinates
#    horizontal left edge
#    vertical lower edge
#    horizontal right edge
#    vertical upper edge
#  start in degrees clockwise from positive real axis
#  end in degrees clockwise from positive real axis
#  color


def sub(nest, low, high, val):
    val_range = high - low

    if(val > 0 ):
      beg = 0 
      relative_end = val - low
      end = 360 * relative_end / val_range
    else:
      end = 0
      relative_beg = val # high - val
      beg = 360 * relative_beg / val_range

    left_corner =  nest*9
    right_corner = 200 - nest*9

    if( nest == 0 ):
      color = 'white'
    else:
      if( nest == 1 ):
        color = 'red'
      else: 
        if( nest == 2):
          color = 'orange'
        else: 
          if( nest == 3):
            color = 'yellow' 
          else: 
            if( nest == 4):
              color = 'green'
            else: 
              if( nest == 5):
                color = 'blue'
              else: 
                color = 'black' 

    draw.pieslice((left_corner, left_corner, right_corner, right_corner), beg-90, end-90, color, 'blue')

def date(day, month, year):
  sub(0, 0, 30, day)
  sub(1, 0, 12, month)
  if(year < 20):
    year = year + 100
  sub(2, 0, 200, year)

# 462.125

#sub(0, 0, 10, 5)
#sub(1, 0, 10, 2)
#sub(2, 0, 10, 1)
#sub(3, 0, 10, 2)
#sub(4, 0, 10, 6)
#sub(5, 0, 10, 4)

# 7,125
#sub(0, 0, 10, 5)
#sub(1, 0, 10, 0)
#sub(2, 0, 10, 1)
#sub(3, 0, 10, 7)
#sub(4, 0, 10, 0)
##dat4(15, 8, 5)(15, 8, 5)
#sub(5, 0, 10, 0)

sub(0, 0, 12, 4)    # since sunrise
sub(1, 0, 6, -3)    # until low tide
sub(2, 0, 28, -12)  # until full moon
image.show()
