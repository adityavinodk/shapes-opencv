#classes and subclasses to import
import cv2
import numpy as np
import os


filename = 'results1B_3686.csv'
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
    filep.close()

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
def blend_transparent(face_img, overlay_t_img):
    # Split out the transparency mask from the colour info
    overlay_img = overlay_t_img[:,:,:3] # Grab the BRG planes
    overlay_mask = overlay_t_img[:,:,3:]  # And the alpha plane

    # Again calculate the inverse mask
    background_mask = 255 - overlay_mask

    # Turn the masks into three channel, so we can use them as weights
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    # Create a masked out face image, and masked out overlay
    # We convert the images to floating point in range 0.0 - 1.0
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    # And finally just add them together, and rescale it back to an 8bit integer image    
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))


def main(video_file):

    cap = cv2.VideoCapture(video_file)
    image_red = cv2.imread("yellow_flower.png",-1)
    image_blue = cv2.imread("pink_flower.png",-1)
    image_green = cv2.imread("red_flower.png",-1)

#####################################################################################################
    square=cv2.imread('C:/Users/adsvi/Desktop/square.png')
    square_gray=cv2.cvtColor(square,cv2.COLOR_BGR2GRAY)
    ret,square_thresh=cv2.threshold(square_gray,100,255,0)
    img1,contours_square,heirarchy=cv2.findContours(square_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.mp4',fourcc, 20.0, (640,480))

    list=[]
    def findshapes(contours,colour):
        colourshapes=[]
        for i in contours:     
            nosides=len(cv2.approxPolyDP(i,0.01*cv2.arcLength(i,True),True))
            M=cv2.moments(i)
            if M["m00"]!=0:
                cx=int(M['m10']/M['m00'])
                cy=int(M['m01']/M['m00'])
                if nosides==3:
                    colourshapes.append([colour,'Triangle',cx,cy])         
                elif nosides==4:
                    if cv2.contourArea(i)==((cv2.arcLength(i,True))/4)**2:
                        colourshapes.append([colour,'Square',cx,cy] )                               
                    else:
                        ret=cv2.matchShapes(contours_square[0],i,1,0.0)
                        if ret>0.1205: #parallelogram
                            colourshapes.append([colour,'Parallelogram',cx,cy])                   
                        elif 0<ret<0.09:  #rhombus
                            colourshapes.append([colour,'Rhombus',cx,cy])                   
                elif nosides==5:
                    colourshapes.append([colour,'Pentagon',cx,cy])           
                elif nosides==6:
                    colourshapes.append([colour,'Hexagon',cx,cy])
                elif nosides>7:
                    colourshapes.append([colour,'Circle',cx,cy])
        return colourshapes       

    ret, frame = cap.read()
    median_blur=cv2.medianBlur(frame,5)
    prev_median_blur = median_blur
    prev_frame = frame
    current_frame = frame
    consecutive_frames = 0
    instantaneous_frame = frame
    while (ret):
        ret2,frame = cap.read()
        median_blur=cv2.medianBlur(frame,5)
        if ret2:
            difference_instantaneous = frame - instantaneous_frame
            difference_instantaneous_gray = cv2.cvtColor(difference_instantaneous, cv2.COLOR_BGR2GRAY)
            difference_instantaneous_area = np.sum(difference_instantaneous_gray * 1.0/255.0)
            full_area = np.sum(np.full(difference_instantaneous_gray.shape, 1.0))
            percent_instantaneous = difference_instantaneous_area / full_area
            if (percent_instantaneous < 0.005):
                consecutive_frames +=1
            else:
                consecutive_frames=0

            instantaneous_frame = frame

            if (consecutive_frames == 50) :
                consecutive_frames = 0
                difference = median_blur - prev_median_blur
                difference_gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
                
                diff_area = np.sum(difference_gray * 1.0/255.0)
                percent = diff_area / full_area
                if (percent < 0.005) :
                    current_frame = prev_frame

                else :
                    hsv_img = cv2.cvtColor(difference, cv2.COLOR_BGR2HSV)
                    # Range of green masked
                    lower_green = np.array([45, 100, 100])
                    higher_green = np.array([75, 255, 255])
                    green_portion = cv2.inRange(hsv_img, lower_green, higher_green)

                    # Range of red masked
                    lower_red = np.array([0, 100, 100])
                    higher_red = np.array([0, 255, 255])
                    red_portion = cv2.inRange(hsv_img, lower_red, higher_red)

                    # Range of blue masked
                    lower_blue = np.array([105, 100, 100])
                    higher_blue = np.array([135, 255, 255])
                    blue_portion = cv2.inRange(hsv_img, lower_blue, higher_blue)

                    ret, green_thresh = cv2.threshold(green_portion, 127, 255, 0)
                    ret, red_thresh = cv2.threshold(red_portion, 127, 255, 0)
                    ret, blue_thresh = cv2.threshold(blue_portion, 127, 255, 0)

                    img2, green_contours, heirarchy = cv2.findContours(green_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    img3, red_contours, heirarchy = cv2.findContours(red_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    img4, blue_contours, heirarchy = cv2.findContours(blue_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    greenshapes=findshapes(green_contours,'Green')
                    redshapes=findshapes(red_contours,'Red')
                    blueshapes=findshapes(blue_contours,'Blue')

                    max_green_area = 0
                    max_green_contour = green_contours[0]
                    for i in green_contours:
                        area = cv2.contourArea(i)
                        if (area > max_green_area):
                            max_green_area = area
                            max_green_contour = i

                    max_red_area = 0
                    max_red_contour = red_contours[0]
                    for i in red_contours:
                        area = cv2.contourArea(i)
                        if (area > max_red_area) :
                            max_red_area = area
                            max_red_contour = i

                    max_blue_area = 0
                    max_blue_contour = blue_contours[0]
                    for i in blue_contours:
                        area = cv2.contourArea(i)
                        if (area > max_blue_area):
                            max_blue_area = area
                            max_blue_contour = i

                    if (max_green_area > max_red_area) and (max_green_area > max_blue_area):                
                        x,y,w,h = cv2.boundingRect(max_green_contour)
                        overlay_image = cv2.resize(image_green,(w,h))
                        frame[y:y+h,x:x+w,:] = blend_transparent(frame[y:y+h,x:x+w,:], overlay_image)
                        current_frame = frame
                    elif (max_red_area > max_green_area) and (max_red_area > max_blue_area):
                        x,y,w,h = cv2.boundingRect(max_red_contour)
                        overlay_image = cv2.resize(image_red,(w,h))
                        frame[y:y+h,x:x+w,:] = blend_transparent(frame[y:y+h,x:x+w,:], overlay_image)
                        current_frame = frame
                    else :
                        x,y,w,h = cv2.boundingRect(max_blue_contour)
                        overlay_image = cv2.resize(image_blue,(w,h))
                        frame[y:y+h,x:x+w,:] = blend_transparent(frame[y:y+h,x:x+w,:], overlay_image)
                        current_frame = frame

                    greenshapes=findshapes(green_contours,'Green')
                    redshapes=findshapes(red_contours,'Red')
                    blueshapes=findshapes(blue_contours,'Blue')
                prev_median_blur = median_blur
                prev_frame = current_frame
                
            cv2.imshow('op_frame', current_frame)
            out.write(frame)
            cv2.waitKey(40)

        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    def callcsv(shapes):
        for element in shapes:
            colour,shape,cx,cy=element
            writecsv(colour,shape,cx,cy)
        outputfile=open(filename,'a')
        outputfile.write('\n\n')
        outputfile.close()

    callcsv(greenshapes);callcsv(redshapes);callcsv(blueshapes)

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    main(os.path.abspath("Video.mp4"))