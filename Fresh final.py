import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx
import pyautogui
import math
mouse=Controller()

app=wx.App(False)
(sx,sy)=wx.GetDisplaySize()
# (camx,camy)=(760,420)

#blue er jonno
lowerBound=np.array([90,100,130])
upperBound=np.array([130,255,255])

#green er jonno
lowerBound2=np.array([34,80,80])
upperBound2=np.array([65,255,255])

cam= cv2.VideoCapture(0)

kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
kernelOpen2=np.ones((5,5))
kernelClose2=np.ones((25,25))

frame_x1 = 120;
frame_y1 = 120;
frame_x2 = 520;
frame_y2 = 340;

oldx = -1;
oldy = -1;
cnt = 0;
cnt2=0;
flag2=0; #activate
flag=0;
drag=0;


def distance(x1,y1,x2,y2):
    #distance from two obj
    # dist = sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
    dist = math.hypot(x2 - x1, y2 - y1)
    return dist



while True:
    ret, img=cam.read()
    img=cv2.resize(img,(640,460))
    img = cv2.flip(img, 1)

    #convert BGR to HSV
    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    # create the Mask
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    mask2=cv2.inRange(imgHSV,lowerBound2,upperBound2)

    #morphology
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskOpen2=cv2.morphologyEx(mask2,cv2.MORPH_OPEN,kernelOpen2)

    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    maskClose2=cv2.morphologyEx(maskOpen2,cv2.MORPH_CLOSE,kernelClose2)

    maskFinal=maskClose
    _,conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
   # h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    maskFinal2=maskClose2
    _,conts2,h2=cv2.findContours(maskFinal2.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)


    cv2.rectangle(img, (frame_x1,frame_y1), (frame_x2,frame_y2), (0,255,255), 2)
 
    for i in range(len(conts)):
       x1,y1,w1,h1=cv2.boundingRect(conts[i])
       cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(0,255,0),2)   

    mx=-1
    for i in range(len(conts2)):
       x2,y2,w2,h2=cv2.boundingRect(conts2[i])
       # cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,255),2)
       mx = max(mx,w2*h2)

    
    newx = -1
    newy = -1
   
    cnt2= cnt2 + 1;
    
    for i in range(len(conts2)):
       x2,y2,w2,h2=cv2.boundingRect(conts2[i])
       if(mx==w2*h2):
            cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
            # cx=(x2+w2)/2
            # cy=(y2+h2)/2

            newx = x2 - frame_x1;
            newy = y2 - frame_y1;
            if newx<0:
                newx=0
            if newy<0:
                newy=0
                
            newx = (newx*sx)/(frame_x2 - frame_x1);
            newy = (newy*sy)/(frame_y2 - frame_y1);
                
            if len(conts)>0:
               if(drag==1 and distance(x1,y1,x2,y2)>30):
                   mouse.release(Button.left)
                   drag=0
                   flag2=0
                   cnt=0
                   flag=0
               elif (cnt>=5 and flag==0):
                   flag=1;
                   flag2=1;
                   cnt=0
                   cnt2=0
               # print flag2 
            else:
                if flag2==1 and flag==1:
                    cnt=0
                if cnt2>=50 and flag2==1:
                    flag2=0
                    cnt=0
                    flag=0
                    cnt2=0
                flag=0;
                if(drag==1):
                   mouse.release(Button.left)
                   drag=0
                   flag=0;
                   flag2=0;
                   cnt=0
            
            if oldx == -1:
                 oldx = newx;
                 oldy = newy;
            
            else:

                 if abs(oldx - newx) > 20 or abs(oldy-newy)>20:
                     oldx = newx;
                     oldy = newy;
                     mouse.position = (newx, newy)
                     cnt = 0;
                
                 elif drag!=1:
                       cnt = cnt + 1;
                       # print cnt;
                       if cnt < 11:
                          continue;
                       # print flag2 
                       if(flag==0 and flag2==1):
                          mouse.click(Button.left, 1);

                       if(flag==1 and flag2==1 and (distance(x1,y1,x2,y2)>140)):
                           mouse.click(Button.left, 2);

                       if(flag==1 and flag2==1 and (distance(x1,y1,x2,y2)>50 and distance(x1,y1,x2,y2)<115)):
                          mouse.click(Button.right, 1);
                          
                       if(flag==1 and flag2==1 and (distance(x1,y1,x2,y2)<35)):
                          mouse.press(Button.left)
                          drag=1

                       if drag==1:
                           oldx=newx
                           oldy=newy
                       else:    
                           flag=0;
                           flag2=0;
                           cnt=0
                           cnt2=0
                           oldx=newx
                           oldy=newy
                
       break;
    cv2.imshow("Mouse",img)

    if cv2.waitKey(10) == 27:
        break

cam.release()
cv2.destroyAllWindows()
