from PIL import Image
from PIL import ImageDraw
import sys

image = Image.new('RGB',(300,300),'black')
draw = ImageDraw.Draw(image)

def adjust( low, high, by):
    return int(low + (high - low) * by)

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

#    lightblue = (0xad, 0xd8, 0xe6)
#    darkblue = (0x00, 0x00, 0x8b)
#  green acutally
    lightblue = (0x90, 0xee, 0x90)
    darkblue = (0x00, 0x64, 0x00)
#  or orange
    lightblue = (0xff, 0xff, 0x00)
    darkblue = (0xff, 0xa5, 0x00)
    darkblue = (0xff, 0, 0)

    color = 'white'
    if( nest == 1 ):
      color = lightblue
#      color = 'red'
    else: 
      if( nest == 2):
        color = 'blue'
        color = (adjust(lightblue[0], darkblue[0], 0.25 ),
                   adjust(lightblue[1], darkblue[1], 0.25 ),
                   adjust(lightblue[2], darkblue[2], 0.5 ))
#        color = 'yellow'
      else: 
        if( nest == 3):
          color = (adjust(lightblue[0], darkblue[0], 0.5 ),
                   adjust(lightblue[1], darkblue[1], 0.5 ),
                   adjust(lightblue[2], darkblue[2], 0.5 ))
#          color = 'blue' 
        else: 
          if( nest == 4):
            color = 'green'
            color = (adjust(lightblue[0], darkblue[0], 0.75 ),
                   adjust(lightblue[1], darkblue[1], 0.75 ),
                   adjust(lightblue[2], darkblue[2], 0.75 ))
          else: 
            if( nest == 5):
              color = darkblue
            else: 
              color = 'black' 

    draw.pieslice((left_corner, left_corner, right_corner, right_corner), beg-90, end-90, color, 'blue')

value = int(sys.argv[1])

hundredk= value / 1000
remainder = value - hundredk * 1000
tenk= remainder / 1000
remainder = value - tenk * 1000
thousands = remainder / 1000
remainder = value - thousands * 1000
hundreds = remainder / 100
remainder = remainder - hundreds* 100
tens = remainder / 10
ones = remainder - tens* 10

sub(1, 0, 10, ones)
sub(2, 0, 10, tens)
sub(3, 0, 10, hundreds)
sub(4, 0, 10, tenk)
sub(4, 0, 10, hundredk)
image.show()
