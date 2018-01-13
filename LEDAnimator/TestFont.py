import Font
import numpy as np
import cv2
from Constants import *

FONTSIZE=10

msg="A" #BCDEFGHIJKLMNOPQRSTUVWXYZyjqp"

f=Font.Font(FONT_HERSHEY_SIMPLEX,FONTSIZE)
w,h,b=f.getBbox(msg)

print "CV2 Bbox",w,h,b

#img=np.zeros((h+b+4,w+4,4),dtype=np.uint8)
img=np.zeros((100,100,4),dtype=np.uint8)


cv2.line(img,(0,FONTSIZE+2),(100,FONTSIZE+2),(0,0,255,255),1,LINE_8)
f.drawText(img,(2,h+2),msg,(255,255,0,255))

fBdf=Font.Font("BDF",FONTSIZE)
w,h,b=fBdf.getBbox(msg)

print "BDF Bbox",w,h,b

fBdf.drawText(img,(30,2),msg,(255,255,0,255))

cv2.imshow("CV2 image",img)
cv2.waitKey(0)