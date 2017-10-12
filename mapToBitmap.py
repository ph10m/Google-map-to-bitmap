from PIL import Image, ImageDraw, ImageColor
import urllib.request
import sys


img_url = "https://maps.googleapis.com/maps/api/staticmap?&style=feature:all|element:labels|visibility:off&center=Trondheim&zoom=14&size=640x640&maptype=roadmap&markers=size:small%7Ccolor:0xff0000%7CKongens+gate+64%&markers=size:small%7Ccolor:0xff0000%7CNTNU%&key=AIzaSyBGPMQimnM2hqZeu4oLayKLk0mW1EYKRcY"
def main():
    print("hei")
    f = open('im.png', 'wb')
    with urllib.request.urlopen(img_url) as res:
        f.write(res.read())
    f.close()

colors = {
        'water': (0,0,255),
        'grass': (0,255,0),
        'land': (200,180,180),
        'mark': (255,0,0),
        'road': (255,255,255)
        }


def identify_color(col):
    r,g,b = col
    avg_col = sum(col)/len(col)
    if avg_col > 240:
        return colors['road']
    elif avg_col > 215:
        return colors['land']
    elif avg_col < 50:
        return colors['land']
    dominant = max(col)
    if r > 150 and g < 110 and b < 110:
        return colors['mark']
    elif dominant == g and g > 150:
        return colors['grass']
    elif dominant == b and b > 150:
        return colors['water']
    return colors['land']

def get_avg_col(rect):
    w,h = rect.size
    step = 2
    iterations = int((w/step)**2)
    r,g,b = 0,0,0
    for x in range(1,w,step):
        for y in range(1,h,step):
            _r,_g,_b = rect.getpixel((x,y))
            # check for roads
            if _r > 250 and _g > 250 and _b > 250:
                return (255,255,255)
            r+=_r
            g+=_g
            b+=_b
    avg_col = int(r/iterations),int(g/iterations),int(b/iterations)
    #  print ("AVERAGE RGB: " + str(sum(avg_col)/3))
    return identify_color(avg_col)
    #  return avg_col

def handle_img():
    im = Image.open('im.png')
    im = im.convert('RGB')
    draw = ImageDraw.Draw(im)
    w,h = im.size # w == h
    step = 6
    # 640 px, step = 20 => 32 bitmaps
    #  char_array = [['' for i in range(w)] for j in range(h)]
    #  print(char_array)
    for x in range(0,w,step):
        for y in range(0,h,step):
            tmp_rectangle = im.crop((x,y,x+step,y+step))
            col = get_avg_col(tmp_rectangle)
            parsed_col = identify_color(col)
            draw.rectangle([x,y,x+step,y+step],fill=col)

    im.save("converted.png")


#  main()
handle_img()
