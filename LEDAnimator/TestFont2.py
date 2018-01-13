import numpy as np
import cv2


msg="Ag"

#((w, h), b) = cv2.getTextSize(text, self.fontFace, self.fontScale, thickness)
((w,h),b)=cv2.getTextSize(msg,cv2.FONT_HERSHEY_SIMPLEX,1.0,1)

print "w,h,b",w,h,b

img=np.zeros((240,240,4),dtype=np.uint8)


def drawText(X,Y,msg,scale):
    ((w, h), b) = cv2.getTextSize(msg, cv2.FONT_HERSHEY_SIMPLEX, scale, 1)
    print "scale",scale,"w,h,b", w, h, b

    cv2.line(img, (X, Y), (X + w, Y), (255, 255, 255, 255))
    #cv2.line(img,(X,Y+h),(X+w,Y+h),(255,0,255,255))
    #cv2.line(img,(X,Y+h+b),(X+w,Y+h+b),(255,255,0,255))
    cv2.putText(img, msg, (X,Y), cv2.FONT_HERSHEY_SIMPLEX, scale, (0,255,0,255),1,cv2.LINE_8,
                False)

drawText(0,20,msg,1.0)
drawText(50,20,msg,0.5)

cv2.imshow("CV2 image",img)
cv2.waitKey(0)