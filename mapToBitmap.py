from PIL import Image, ImageDraw, ImageColor
import urllib.request
import sys
import random
import os

city = "Trondheim"
city = city.replace(' ','+')

#  address_from = "Kongens Gate 58A" + city
address_from = input('Fra (addresse): ')
#  address_from = "kirkegata 58"
address_from = address_from.replace(' ', '+') + "+" + city

#  address_to = "NTNU"
address_to = input('Til: ')
address_to = address_to.replace(' ', '+') + "+" + city

path_id = str(random.randrange(999,99999))
folder_name = address_from[0:10] + "_to_" + address_to[0:10] + path_id
os.mkdir(folder_name)
os.chdir(folder_name)
char_filename = "board-" + folder_name + ".txt"
orig_img = "im.png"
new_img = "rendered.png"

print("Map from " + address_from + " to " + address_to)

map_url = "https://maps.googleapis.com/maps/api/staticmap?&style=feature:all|element:labels|visibility:off&center="
map_data = "&zoom=14&size=640x640&maptype=roadmap"
#  marker_size = "tiny"
#  mark_from = "&markers=size:small%7Ccolor:0xff0000%7C"+address_from+"%"
#  mark_to = "&markers=size:small%7Ccolor:0xff0000%7C"+address_to+"%"
mark = "https://i.imgur.com/Khwdgwy.png"
mark_from = "&markers=icon:" + mark + "%7C"+address_from+"%"
mark_to = "&markers=icon:" + mark + "%7C"+address_to+"%"
api_key = "&key=AIzaSyBGPMQimnM2hqZeu4oLayKLk0mW1EYKRcY"
img_url = map_url + city + map_data + mark_from + mark_to + api_key
print(img_url)

def main():
    f = open(orig_img, 'wb')
    with urllib.request.urlopen(img_url) as res:
        f.write(res.read())
    f.close()

colors = {
    'w': (73, 216, 245),  # Water
    'm': (99, 99, 99),  # Mountain
    'f': (3, 82, 0),  # Forest
    'g': (50, 200, 50),  # Grass
    'r': (114, 80, 41),  # Road
    '.': (255, 255, 255),  # Nothing
    '#': (114, 114, 114),  # Wall
    'A': (255, 90, 90),  # Start
    'B': (255, 90, 90),  # End
    'v': (255, 0, 0),
    'c': (150, 150, 150)
    }

markers = ['A','B']
def identify_color(col):
    r,g,b = col
    avg_col = sum(col)/len(col)
    if avg_col > 240:
        return colors['r'],'r'
    elif avg_col > 215:
        return colors['f'],'f'
    elif avg_col < 50:
        return colors['f'],'f'
    dominant = max(col)
    if r > 210 and b < 160 and g < 160:
        if len(markers)>0:
            marker = markers[0]
            del(markers[0])
            return colors[marker], marker
        else:
            return colors['g'],'g'
    elif dominant == g and g > 150:
        return colors['g'],'g'
    elif dominant == b and b > 150:
        return colors['w'],'w'
    return colors['g'],'g'

def get_avg_col(rect, precise):
    w,h = rect.size
    step = 2
    iterations = int((w/step)**2)
    r,g,b = 0,0,0
    for x in range(1,w,step):
        for y in range(1,h,step):
            _r,_g,_b = rect.getpixel((x,y))
            # check for roads
            if _r > 250 and _g > 250 and _b > 250:
                return colors['r'], 'r'
            r+=_r
            g+=_g
            b+=_b
    avg_col = int(r/iterations),int(g/iterations),int(b/iterations)
    #  print ("AVERAGE RGB: " + str(sum(avg_col)/3))
    #  identified_col, identified_char = identify_color(avg_col)
    #  return identified_col, identified_char
    if precise:
        return identify_color(avg_col)
    else:
        return avg_col, ''

def handle_img(precise=True):
    im = Image.open(orig_img)
    im = im.convert('RGB')
    im2 = im.copy()
    draw = ImageDraw.Draw(im)
    draw2 = ImageDraw.Draw(im2)
    w,h = im.size # w == h
    step = 8
    # 640 px, step = 20 => 32 bitmaps
    # 640 px, step = 8 => 80 bitmaps
    #  print(char_array)
    char_array = [['' for i in range(int(w/step))] for j in range(int(h/step))]
    marks = ['A','B']
    foundStartMark, foundEndMark = False, False
    char_x, char_y = 0,0
    for x in range(0,w,step):
        for y in range(0,h,step):
            tmp_rectangle = im.crop((x,y,x+step,y+step))
            col, col_char = get_avg_col(tmp_rectangle, True)
            col2, _ = get_avg_col(tmp_rectangle, False)
            draw.rectangle([x,y,x+step,y+step],fill=col)
            draw2.rectangle([x,y,x+step,y+step],fill=col2)
            char_array[char_y][char_x] = col_char
            char_y += 1
        char_x += 1
        char_y = 0
    chr_file = open(char_filename,'wb')
    for row in char_array:
        for c in row:
            chr_file.write(c.encode())
        chr_file.write('\r\n'.encode())
    chr_file.close()

    im.save(new_img)
    im2.save("rough.png")


main()
handle_img(precise=True)
