from tkinter import *
from tkinter import filedialog
import pytesseract
import cv2
import os
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps
from PIL import ImageFont
from pytesseract import image_to_string
pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
a=Tk()
a.title('Click below')
def mfileopen():
    i=0
    p='y'
    while(p=='y' or p=='Y'):
        a.f=filedialog.askopenfilename(title=u'select file',parent=a)
        f1=a.f
        a.destroy()
        print("Image you chose is",f1)
        im=Image.open(f1)
        im.show()
        output = pytesseract.image_to_string(im.convert("RGB"), lang='eng')
        name="file["+str(i)+'].txt'
        f=open(name,"w+",encoding="utf-8")
        f.write(output)
        f.close()
        os.startfile(name)
        i=i+1
        print("Do you want editted text to be converted back to image?\n")
        x=input("Enter y/Y or n/N")
        if(x=='y' or x=='Y'):
            image = text_image(name)
            image.show()
            name=name+'.png'
            image.save(name)
        print("Are there more images?")
        p=input("Enter y/Y or n/N")
    print("------ Done -------")
def text_image(text_path, font_path=None):
    grayscale = 'L'
    PIXEL_ON = 0  # PIL color to use for "on"
    PIXEL_OFF = 255  # PIL color to use for "off"
    with open(text_path) as text_file:  
        lines = tuple(l.rstrip() for l in text_file.readlines())
    large_font = 20  
    font_path = font_path or 'cour.ttf'  
    try:
        font = PIL.ImageFont.truetype(font_path, size=large_font)
    except IOError:
        font = PIL.ImageFont.load_default()
    pt2px = lambda pt: int(round(pt * 96.0 / 72))  
    max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
    test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' # to find max height of each line
    max_height = pt2px(font.getsize(test_string)[1])
    max_width = pt2px(font.getsize(max_width_line)[0])
    height = max_height * len(lines)  # exact height required
    width = int(round(max_width + 50))  # increased to avoid error
    image = PIL.Image.new(grayscale, (width, height), color=PIXEL_OFF)
    draw = PIL.ImageDraw.Draw(image)
    vertical_position = 5
    horizontal_position = 5
    line_spacing = int(round(max_height * 0.8))  # remove extra spacing
    for line in lines:
        draw.text((horizontal_position, vertical_position),line, fill=PIXEL_ON, font=font)
        vertical_position += line_spacing
    c_box = PIL.ImageOps.invert(image).getbbox()
    image = image.crop(c_box)
    return image
button=Button(text="select image",bg="lightgray",font="Algerian",width=30,command=mfileopen).pack()
a.mainloop()