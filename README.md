# shapes-opencv
This project aims to work with OpenCV to detect, draw or crop shapes in images and videos

## Shape Detection in Images
The program will show draw the outline and centroid of the different shapes in the images

In the folder `input_images`, some test images are placed on which the shape detection will be run. 
To test more images, add the files in PNG format in `input_images`, then edit line 12 in `find_shapes.py`
To run this file, run the following in the terminal of this project directory
```shell
python find_shapes.py
```

## Cropping Shapes in Video
The program will detect the different shapes appearing in a video and place another image depending on the type of shape

To test this program add a video(must contain shapes) named `Video.mp4` to the parent folder
To run this file, run the following in the terminal of this project directory
```shell
python crop_shapes.py
```