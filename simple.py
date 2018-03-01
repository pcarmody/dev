from PIL import Image
from PIL import ImageDraw

image = Image.new('RGB',(90,90),'white')
draw = ImageDraw.Draw(image)
draw.ellipse((0,0,90,90),'yellow','blue')
draw.ellipse((25,20,35,30),'yellow','blue')
draw.ellipse((50,20,60,30),'yellow','blue')
draw.arc((20,40,70,70), 0, 180, 0) #draw circle in black
image.show()
