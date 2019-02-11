import random
from colorharmonies import Color, complementaryColor, triadicColor, splitComplementaryColor, tetradicColor, analogousColor, monochromaticColor
from PIL import Image,ImageFont,ImageDraw
import randomcolor
import ctypes
import os
import requests
import json
import pandas
import textwrap

r = random.randint(0,255)
g = random.randint(0,255)
b = random.randint(0,255)


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


rand_color = randomcolor.RandomColor()
cor = hex_to_rgb(rand_color.generate()[0])
fundo = Color(cor,"","")



img = Image.new('RGBA',(1920,1080),(r, g, b) )

lines = open('D:/Users/rafae/Documents/Script/dicionario.txt', encoding="utf8").read().splitlines()
while True:
    myline =random.choice(lines)
    response= requests.get('http://dicionario-aberto.net/search-json/'+myline)
    try:
        data = response.json()
    except ValueError:
        continue
    if data.get('entry') is not None:
        significado = data['entry']['sense'][0]['def']
        break
    continue

    
str1 = myline.upper()

font =ImageFont.truetype("arial.ttf",75)
w,h= font.getsize(str1)

draw = ImageDraw.Draw(img)



def sombra(N,font,str1,shadowcolor,x,y,a):
    draw.text((x-N, y-N-a), str1, font=font, fill=shadowcolor)
    draw.text((x+N, y-N-a), str1, font=font, fill=shadowcolor)
    draw.text((x-N, y+N-a), str1, font=font, fill=shadowcolor)
    draw.text((x+N, y+N-a), str1, font=font, fill=shadowcolor)


x = (1920-w)/2
y = (1080-h)/2
significado = significado.split('<',1)[0]
significado = significado.translate({ord(c): None for c in '!@#$_.'})
ws,hs= font.getsize(significado)
xs = (1920-ws)/2
ys = (1080-hs)/2




complementar = splitComplementaryColor(fundo)
a= complementar[0][0]
b=complementar[0][1]
c=complementar[0][2]
shadowcolor = (a,b,c)


draw.rectangle(((x-30, y-200), (x+w+30), h+y-180), shadowcolor)



sombra(1.2,font,str1,(0,0,0),x,y,200)

draw.text( (x, y-200), str1 , (255,255,255), font )
draw.textsize(significado,font)


lines = textwrap.wrap(significado, width=30)
y_text = ys+100
for line in lines:
    width, height = font.getsize(line)
    sombra(1.2,font,line,(0,0,0),(1920-width)/2,y_text,0)
    draw.text(((1920-width)/2, y_text), line, font=font, fill=shadowcolor, align="center")
    y_text += height


img.save("wallpaper.png")
ctypes.windll.user32.SystemParametersInfoW(20, 0, "wallpaper.png" , 0)
