#classes and subclasses to import
import cv2
import numpy as np
import os

filename = 'results1A_3686.csv'
#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#subroutine to write results to a csv
def writecsv(color,shape,cx,cy):
    global filename
    #open csv file in append mode
    filep = open(filename,'a')
    # create string data to write per image
    datastr = "," + color + "-" + shape + "-" + str(cx) + "-" + str(cy)
    #write to csv
    filep.write(datastr)

def main(path):
    font = cv2.FONT_HERSHEY_SIMPLEX
    square=cv2.imread('C:/Users/adsvi/Desktop/square.png')
    square_gray=cv2.cvtColor(square,cv2.COLOR_BGR2GRAY)
    ret,square_thresh=cv2.threshold(square_gray,100,255,0)
    img1,contours_square,heirarchy=cv2.findContours(square_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    images=['test1','test2','test3','test4','test5']
    for image in images:
        img=cv2.imread(image+'.png')
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
                    writecsv(colour,'Triangle',cx,cy)
                    cv2.putText(img,colour,(cx-20,cy-40),font,0.55,colourcode,2)
                    cv2.putText(img,"Triangle",(cx-20,cy-20),font,0.55,colourcode,2)
                    cv2.putText(img,centre,(cx-20,cy),font,0.55,colourcode,2)
                elif nosides==4:
                    if cv2.contourArea(i)==((cv2.arcLength(i,True))/4)**2:
                        shapes.append([colour,'Square',(cx,cy)])
                        writecsv(colour,'Square',cx,cy)
                        cv2.putText(img,colour,(cx-20,cy-40),font,0.55,colourcode,2)
                        cv2.putText(img,"Square",(cx-20,cy-20),font,0.55,colourcode,2)
                        cv2.putText(img,centre,(cx-20,cy),font,0.55,colourcode,2)
                    else:
                        ret=cv2.matchShapes(contours_square[0],i,1,0.0)
                        if ret>0.1205: #parallelogram
                            shapes.append([colour,'Parallelogram',(cx,cy)])
                            writecsv(colour,'Parallelogram',cx,cy)
                            cv2.putText(img,colour,(cx-20,cy-40),font,0.55,colourcode,2)
                            cv2.putText(img,"Parallelogram",(cx-20,cy-20),font,0.55,colourcode,2)
                            cv2.putText(img,centre,(cx-20,cy),font,0.55,colourcode,2)
                        elif 0<ret<0.09:  #rhombus
                            shapes.append([colour,'Rhombus',(cx,cy)])
                            writecsv(colour,'Rhombus',cx,cy)
                            cv2.putText(img,colour,(cx-20,cy-40),font,0.55,colourcode,2)
                            cv2.putText(img,"Rhombus",(cx-20,cy-20),font,0.55,colourcode,2)
                            cv2.putText(img,centre,(cx-20,cy),font,0.55,colourcode,2)
                elif nosides==5:
                    shapes.append([colour,'Pentagon',(cx,cy)])
                    writecsv(colour,'Pentagon',cx,cy)
                    cv2.putText(img,colour,(cx-20,cy-40),font,0.55,colourcode,2)
                    cv2.putText(img,"Pentagon",(cx-20,cy-20),font,0.55,colourcode,2)
                    cv2.putText(img,centre,(cx-20,cy),font,0.55,colourcode,2)
                elif nosides==6:
                    shapes.append([colour,'Hexagon',(cx,cy)])
                    writecsv(colour,'Hexagon',cx,cy)
                    cv2.putText(img,colour,(cx-20,cy-40),font,0.55,colourcode,2)
                    cv2.putText(img,"Hexagon",(cx-20,cy-20),font,0.55,colourcode,2)
                    cv2.putText(img,centre,(cx-20,cy),font,0.55,colourcode,2)
                elif nosides>7:
                    shapes.append([colour,'Circle',(cx,cy)])
                    writecsv(colour,'Circle',cx,cy)
                    cv2.putText(img,colour,(cx-20,cy-40),font,0.55,colourcode,2)
                    cv2.putText(img,"Circle",(cx-20,cy-20),font,0.55,colourcode,2)
                    cv2.putText(img,centre,(cx-20,cy),font,0.55,colourcode,2)

        shapes.insert(0,image)
        openfile=open(filename,'a')
        openfile.write(image)
        openfile.close()
        findshapes(green_contours,"Green",(255,0,170))
        findshapes(red_contours,"Red",(255,170,0))
        findshapes(blue_contours,"Blue",(0,255,0))
        openfile=open(filename,'a')
        openfile.write('\n')
        openfile.close()
        cv2.imwrite(image+'output.png',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print shapes 
    openfile=open(filename,'a')
    openfile.write('\n')
    openfile.close()
    opencsv=open('results_3686.csv','a')
    opencsv.write('\nt.e.s.t.2...p.n.g\nt.e.s.t.3...p.n.g\nt.e.s.t.4...p.n.g\nt.e.s.t.5...p.n.g')
    opencsv.close()
    exit()

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    mypath = '.'
    #getting all files in the directory
    onlyfiles = [str.join(mypath, f) for f in os.listdir(mypath) if f.endswith(".png")]
    #iterate over each file in the directory
    for fp in onlyfiles[:-1]:
        #Open the csv to write in append mode
        filep = open('results_3686.csv','a')
        #this csv will later be used to save processed data, thus write the file name of the image 
        filep.write(fp)
        #close the file so that it can be reopened again later
        filep.close()
        #process the image
        data = main(fp)
        print data
        #open the csv
        filep = open('results_3686.csv','a')
        #make a newline entry so that the next image data is written on a newline
        filep.write('\n')
        #close the file
        filep.close()
