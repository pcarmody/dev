from PIL import Image
from PIL import ImageDraw
import sys

image = Image.new('RGB',(300,300),'black')
draw = ImageDraw.Draw(image)

def sub(nest, low, high, val):
    val_range = high - low

    if(val > 0 ):
      beg = 0 
      relative_end = val - low
      end = 360 * relative_end / val_range
    else:
      end = 0
      relative_beg = high - val
      beg = 360 * relative_beg / val_range

    left_corner =  nest*25
    right_corner = 300 - nest*25

    color = 'white'
    if( nest == 1 ):
      color = 'red'
    else: 
      if( nest == 2):
        color = 'yellow'
      else: 
        if( nest == 3):
          color = 'blue' 
        else: 
          if( nest == 4):
            color = 'green'
          else: 
            if( nest == 5):
              color = 'blue'
            else: 
              color = 'black' 

    draw.pieslice((left_corner, left_corner, right_corner, right_corner), beg-90, end-90, color, 'blue')

value = int(sys.argv[1])
thousands = value / 1000
remainder = value - thousands * 1000
hundreds = remainder / 100
remainder = remainder - hundreds* 100
tens = remainder / 10
ones = remainder - tens* 10

sub(1, 0, 10, ones)
sub(2, 0, 10, tens)
sub(3, 0, 10, hundreds)
image.show()
