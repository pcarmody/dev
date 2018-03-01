from PIL import Image
from PIL import ImageDraw

image = Image.new('RGB',(100,100),'white')
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

#draw.arc((5,5, 85, 85), 0, 270, 'red')
#draw.pieslice((10,10, 80, 80), 45, 136, 'red', 'blue')
#draw.pieslice((20, 20, 70,70), -90, 225, 'green', 'blue')

def sub(nest, low, high, val):
    val_range = high - low

    if(val < 0 ):
      beg = 0 
      relative_end = val - low
      end = 360 * relative_end / val_range
    else:
      end = 0
      relative_beg = high - val
      beg = 360 * relative_beg / val_range

    left_corner =  nest*5
    right_corner = 100 - nest*5

    color = 'white'
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

#draw.arc((5,5, 85, 85), 0, 270, 'red')
#sub(1, 0, 9, 2)
sub(2, 0, 9, 3)
sub(3, 0, 9, 7)
#sub(4, 0, 9, -4)
#draw.pieslice((10,10, 80, 80), 45, 136, 'red', 'blue')
#draw.pieslice((20, 20, 70,70), -90, 225, 'green', 'blue')
