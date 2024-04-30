# Tool to convert Ayca's .svg exports into a format suitable for MEGA65 vector-art
import xml.etree.ElementTree as ET
import re
import struct

def read_xml():
    return ET.parse('Anathema.svg').getroot()

LINE    = 0
CIRCLE  = 1
ELLIPSE = 2
BOX     = 3
POLY    = 4
COLOUR = 63
FILL_FLAG = 64

scalex = 640/640
scaley = 320. / 350.
offsx=-10
offsy=-100

map_svg_to_m65_clr = {
    'none': -1,
    'black': 0,
    'white': 1,
    '#880000': 2,
    '#AAFFEE': 3,
    '#664400': 9,
    '#DD8855': 8,
    '#FF7777': 10,
    '#333333': 11,
    '#0088FF': 14,
    '#BBBBBB': 15
}

map_clrname_to_m65clr = { }

previous_colour = -1
selected_colour = -1

def extract_colours(xml):
    clrs = xml[0][0].text.strip()
    for line in clrs.splitlines():
        line = line.strip()
        print(line)
        s = line.split(' ')
        name=s[0]
        m = re.match(r'.*:(.*)}', s[1])
        colval=m.groups()[0]
        map_clrname_to_m65clr[name] = map_svg_to_m65_clr[colval]

    print(map_clrname_to_m65clr)

    return map_clrname_to_m65clr

def check_for_colour_change(clr):
    global selected_colour
    if clr != selected_colour:
        selected_colour = clr
        outfile.write(struct.pack('B', COLOUR))
        outfile.write(struct.pack('B', clr))

def parse_polygon(poly):
    clr = map_clrname_to_m65clr['.'+poly['class']]
    # check_for_colour_change(clr)

    ptxt = poly['points']
    minx = 0
    miny = 0
    maxx = 0
    maxy = 0
    # scalex = 1
    # scaley = 1
    points = []
    for coord in ptxt.strip().split(' '):
        tx,ty = coord.split(',')
        x = int(tx)
        y = int(ty)
    #     if x<minx:
    #         minx = x
    #     if x>maxx:
    #         maxx = x
    #     if y<miny:
    #         miny=y
    #     if y>maxy:
    #         maxy=y
        points.append([x * scalex + offsx, y * scaley + offsy])

    # print(points)
    # print('minx={}, maxx={}'.format(minx, maxx))
    # print('miny={}, maxy={}'.format(miny, maxy))

    final_points = points
    # if maxx > 639:
    #     scalex = 639 / maxx
    # if maxy > 399:
    #     scaley = 399 / maxy

    # scale = scalex
    # if scaley < scalex:
    #     scale = scaley

    # final_points = []
    # for coord in points:
    #     x = coord[0] * scale
    #     y = coord[1] * scale
    #     final_points.append([x,y])

    # save out to vart file
    outfile.write(struct.pack('B', POLY + FILL_FLAG))
    outfile.write(struct.pack('B', len(final_points)))
    for coord in final_points:
        outfile.write(struct.pack('<H', int(coord[0])))
        outfile.write(struct.pack('<H', int(coord[1])))

def parse_path(path):
    clr = 'white' #map_clrname_to_m65clr['.'+path['class']]
    # check_for_colour_change(clr)

    absx = 0
    absy = 0

    points = []

    txt = path['d']
    print('txt = {}'.format(txt))
    while len(txt) > 0:
        m = re.match(r'[Mmchlzv](.*?)[Mmchlzv].*', txt)
        if m:
            t = m.groups()[0]
        else:
            t = ""
        cmd = txt[0]
        print('clr = {} : cmd = {} : t = {}'.format(clr, cmd, t))
        txt=txt[len(t)+1:]
        t = t.strip()

        if cmd == 'M':
            for coord in t.strip().split(' '):
                tx,ty = coord.split(',')
                x = float(tx)
                y = float(ty)
                absx = x
                absy = y
                points.append([absx * scalex + offsx, absy * scaley + offsy])

        if cmd == 'z':
            # save out to vart file
            v = POLY + FILL_FLAG
            if 'class' in path and path['class'] == 'fil3':
                v = POLY
            outfile.write(struct.pack('B', v))
            outfile.write(struct.pack('B', len(points)))
            for coord in points:
                print(coord)
                outfile.write(struct.pack('<H', int(coord[0])))
                outfile.write(struct.pack('<H', int(coord[1])))
            points=[]

        # if cmd == 'm':
        #     tx,ty = t.split(' ')
        #     x = int(tx)
        #     y = int(ty)
        #     absx += x
        #     absy += y
        #     points.append([absx * scalex, absy * scaley])
        if cmd == 'm':
            for coord in t.strip().split(' '):
                print 'coord={}'.format(coord)
                tx,ty = coord.split(',')
                print 'tx={}, ty={}, scaley={}'.format(tx,ty, scaley)
                absx += float(tx)
                absy += float(ty)
                points.append([absx * scalex + offsx, absy * scaley + offsy])

        if cmd == 'c':
            cnt = 0
            for coord in t.strip().split(' '):
                # print coord
                tx,ty = coord.split(',')
                if cnt == 2:
                    absx += float(tx)
                    absy += float(ty)
                    points.append([absx * scalex + offsx, absy * scaley + offsy])
                    cnt = 0
                else:
                    cnt += 1

        if cmd == 'l':
            for ival in t.strip().split(' '):
                for coord in ival.strip().split(' '):
                    tx,ty = coord.split(',')
                    absx += float(tx)
                    absy += float(ty)
                    points.append([absx * scalex + offsx, absy * scaley + offsy])

        if cmd == 'v':
            # todo: vertical line
            continue

xml = read_xml()

# colours = extract_colours(xml)

outfile = open('test.v', 'wb')
outfile.write(b'VEC')

# iterate over objects (polygons/paths)
for item in xml:
    print(item)
    if 'polygon' in item.tag:
        parse_polygon(item.attrib)
    elif 'path' in item.tag:
        parse_path(item.attrib)

    # print(item.tag)

outfile.close()

# scan their x,y coord details to keep track of minx/y and maxx/y

# store objects in a scaling that fits within 640x400 (or 640x320)

# save out a "uzbek.v" file in vart-format
