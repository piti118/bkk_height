import PIL.Image as Image
from itertools import product
from collections import defaultdict
from pprint import pprint
import sys
im = Image.open('Flood_01.png')
w,h = im.size
pix = im.load()
seekh = h/2

#xoffset
x_range = (102,3709)#inclusive
y_range = (177,2987)#inclusive

#startgrid
sg=(117,177)
sgx,sgy = sg

#gridend
ge=(3698,2929)
gex, gey = ge

gs = (11,11) #grid size
gsx,gsy = gs

# less than 0 65 79 209 3518,1526
# 0-0.5 79 199 255 3231,1863
# 0.5-1.0 181 227 255 3231,1843 
# 1.0-1.5 205 255 161 1294,2216
# 1.5-2.0 136 255 110 1317,2242
# 2.0-2.5 76 224 65 1316,2236
# 2.5-3.0 255 248 110 1325,2243
# 3.0-3.5 255 190 110 1338,2241
# more than 3.5 153 89 64 1368,2223
#ignore 239,228,190 976,309
#sea 190 232 255 1044,2928

hmap = {
    #pix[1337,1552]:-4, #inland river not used
    #pix[647,2767]:-3, #river not used 
    pix[1044,2928]:-2, #sea
    pix[976,309]:-1, #ignore
    pix[3518,1526]:0, #<0
    pix[3231,1863]:1, #0-0.5
    pix[2554,2845]:1, #alternate color
    pix[3231,1843]:2, #0.5-1
    pix[1294,2216]:3, #1-1.5
    pix[2620,2834]:3, #alternate color
    pix[1317,2242]:4, #1.5-2.0
    pix[2598,2834]:4, #alternate color
    pix[1316,2236]:5, #2.0-2.5
    pix[1325,2243]:6, #2.5-3.0
    pix[364,502]:7, #3.0-3.5 
    pix[1368,2223]:8, #>3.5
}

def pixlist(pix,tl):
    """topleft"""
    tlx,tly = tl
    w,h = gs
    ret = [ pix[tlx+i,tly+j] for i,j in product(xrange(w),xrange(h)) ]
    return ret

def mode(rgbas):
    count = defaultdict(int)
    for rgba in rgbas:
        if rgba in hmap:
            count[hmap[rgba]]+=1
        else:
            #print rgba
            pass
    if len(count) == 0: return -1
    ret = max(count, key=count.get)
    #if ret!=-1 : print ret
    return ret
def centerpix(p):
    x,y = p
    return (x+gsx/2+1,y+gsy/2+1)

def xy2latlon(p):
     #check the sign
    x,y = p
    lat_scale = 0.5/(2814-1141) #degree/pixel
    lat_start = 13.5
    y_offset = 2814 #pixel
    lat = (y_offset-y)*lat_scale+lat_start#y
    lon_scale = 0.5/(3043-1406)
    lon_start = 101.0
    x_offset = 3043
    lon = (x-x_offset)*lon_scale+lon_start#x
    return (lon,lat)
    
    

# pl = pixlist(pix,sg)
# print mode(pl)
# print pix[2367,2723]
def main():
    comment = 'lat,lon,hcode,cx,cy'
    print comment
    
    for tlx,tly in product(range(sgx,gex,gsx),range(sgy,gey,gsy)):
        pl = pixlist(pix,(tlx,tly))
        #print pl
        m = mode(pl)
        cx,cy = centerpix((tlx,tly))
        lat,lon = xy2latlon((cx,cy))
        print ','.join([str(lat),str(lon),str(m),str(cx),str(cy)])
        #if m is None: sys.exit()
if __name__ == '__main__':
    main()
#pic info
#top left 0,0
#start x = 100,101 - 3710,3711
#start y = 175,176 - 2988,2989

#ex block 1243-1523 1253,1533 11x11px

# less than 0 65 79 209 3518,1526
# 0-0.5 79 199 255 3231,1863
# 0.5-1.0 181 227 255 3231,1843 
# 1.0-1.5 205 255 161 1294,2216
# 1.5-2.0 136 255 110 1317,2242
# 2.0-2.5 76 224 65 1316,2236
# 2.5-3.0 255 248 110 1325,2243
# 3.0-3.5 255 190 110 1338,2241
# more than 3.5 153 89 64 1368,2223

#ignore 239,228,190 976,309
#sea 190 232 255 1044,2928

#horizontal 125 = 620000, 3150 = 720000
#vertical 200 = 1580000, 2619 = 1500000

#horizontal 3043 = 101.0.0, 1406 = 100.30.0
#vertical 2814 = 13.30.00,1141 = 14.0.0
