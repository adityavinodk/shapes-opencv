import cv2
import numpy as np
import os

font = cv2.FONT_HERSHEY_SIMPLEX
square=cv2.imread('./input_images/square.jpg')
square_gray=cv2.cvtColor(square,cv2.COLOR_BGR2GRAY)
ret,square_thresh=cv2.threshold(square_gray,100,255,0)
img1,contours_square,heirarchy=cv2.findContours(square_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# Edit this list with the names of the pictures you would like to test
images = ['circle','rectangle','rhombus','trapezium']

for image in images:
    img=cv2.imread('input_images/'+image+'.png')
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    hsv_img=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Lists for shapes of different colour
    shapes=[]

    #Range of green masked
    lower_green=np.array([45,100,100])
    higher_green=np.array([75,255,255])
    green_portion=cv2.inRange(hsv_img,lower_green,higher_green)

    #Range of red masked
    lower_red=np.array([0,100,100])
    higher_red=np.array([0,255,255])
    red_portion=cv2.inRange(hsv_img,lower_red,higher_red)

    #Range of blue masked
    lower_blue=np.array([105,100,100])
    higher_blue=np.array([135,255,255])
    blue_portion=cv2.inRange(hsv_img,lower_blue,higher_blue)

    ret,green_thresh=cv2.threshold(green_portion,127,255,0)
    ret,red_thresh=cv2.threshold(red_portion,127,255,0)
    ret,blue_thresh=cv2.threshold(blue_portion,127,255,0)

    img2,green_contours,heirarchy=cv2.findContours(green_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    img3,red_contours,heirarchy=cv2.findContours(red_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    img4,blue_contours,heirarchy=cv2.findContours(blue_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(img,green_contours,-1,(255,0,170),5)
    #cv2.imshow('pic1',img)
    cv2.drawContours(img,blue_contours,-1,(0,255,0),5)
    #cv2.imshow('pic2',img)
    cv2.drawContours(img,red_contours,-1,(255,170,0),5)
    #cv2.imshow('allcontours',img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    def findshapes(contours,colour,colourcode):
        for i in contours:
            nosides=len(cv2.approxPolyDP(i,0.01*cv2.arcLength(i,True),True))
            M=cv2.moments(i)
            cx=int(M['m10']/M['m00'])
            cy=int(M['m01']/M['m00'])
            centre=str((cx,cy))
            if nosides==3:
                shapes.append([colour,'Triangle',(cx,cy)])
                # writecsv(colour,'Triangle',cx,cy)
                cv2.putText(img,colour,(cx-20,cy-40),font,0.55,colourcode,2)
                cv2.putText(img,"Triangle",(cx-20,cy-20),font,0.55,colourcode,2)
                cv2.putText(img,centre,(cx-20,cy),font,0.55,colourcode,2)
            elif nosides==4:
                if cv2.contourArea(i)==((cv2.arcLength(i,True))/4)**2:
                    shapes.append([colour,'Square',(cx,cy)])
                    # writecsv(colour,'Square',cx,cy)
                    cv2.putText(img,colour,(cx-20,cy-40),font,0.55,colourcode,2)
                    cv2.putText(img,"Square",(cx-20,cy-20),font,0.55,colourcode,2)
                    cv2.putText(img,centre,(cx-20,cy),font,0.55,colourcode,2)
                else:
                    ret=cv2.matchShapes(contours_square[0],i,1,0.0)
                    if ret>0.1205: #parallelogram
                        shapes.append([colour,'Parallelogram',(cx,cy)])
                        # writecsv(colour,'Parallelogram',cx,cy)
                        cv2.putText(img,colour,(cx-20,cy-40),font,0.55,colourcode,2)
                        cv2.putText(img,"Parallelogram",(cx-20,cy-20),font,0.55,colourcode,2)
                        cv2.putText(img,centre,(cx-20,cy),font,0.55,colourcode,2)
                    elif 0<ret<0.09:  #rhombus
                        shapes.append([colour,'Rhombus',(cx,cy)])
                        # writecsv(colour,'Rhombus',cx,cy)
                        cv2.putText(img,colour,(cx-20,cy-40),font,0.55,colourcode,2)
                        cv2.putText(img,"Rhombus",(cx-20,cy-20),font,0.55,colourcode,2)
                        cv2.putText(img,centre,(cx-20,cy),font,0.55,colourcode,2)
            elif nosides==5:
                shapes.append([colour,'Pentagon',(cx,cy)])
                # writecsv(colour,'Pentagon',cx,cy)
                cv2.putText(img,colour,(cx-20,cy-40),font,0.55,colourcode,2)
                cv2.putText(img,"Pentagon",(cx-20,cy-20),font,0.55,colourcode,2)
                cv2.putText(img,centre,(cx-20,cy),font,0.55,colourcode,2)
            elif nosides==6:
                shapes.append([colour,'Hexagon',(cx,cy)])
                # writecsv(colour,'Hexagon',cx,cy)
                cv2.putText(img,colour,(cx-20,cy-40),font,0.55,colourcode,2)
                cv2.putText(img,"Hexagon",(cx-20,cy-20),font,0.55,colourcode,2)
                cv2.putText(img,centre,(cx-20,cy),font,0.55,colourcode,2)
            elif nosides>7:
                shapes.append([colour,'Circle',(cx,cy)])
                # writecsv(colour,'Circle',cx,cy)
                cv2.putText(img,colour,(cx-20,cy-40),font,0.55,colourcode,2)
                cv2.putText(img,"Circle",(cx-20,cy-20),font,0.55,colourcode,2)
                cv2.putText(img,centre,(cx-20,cy),font,0.55,colourcode,2)

    findshapes(green_contours,"Green",(255,0,170))
    findshapes(red_contours,"Red",(255,170,0))
    findshapes(blue_contours,"Blue",(0,255,0))

    os.chdir('./output_images')
    cv2.imshow('image',img)
    cv2.imwrite(image+'_output.png',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    os.chdir('..')
    print(shapes)