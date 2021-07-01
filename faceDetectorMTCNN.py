"""
 FaceDetection Based on MTCNN
 The program reds frames from a webcam, detects faces. Extract and saves cropped faces.
 
 It also displays a faces with bounding boxes 

"""

import mtcnn as mt
import cv2 as cv 
import os 


'''create detector usonf the default waite'''
detector = mt.MTCNN()

def faceDetector(frame, dim=(640,480)):
    ''' Convert face image to RGB'''
    rgbFrame = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    rgbFrame =cv.resize(rgbFrame, dim)
    ''' face detection
       The results variable contains bounding boxes. each bounding boxes contains 
        the bottom-left corrner point, the width and the height of the bounding boxes
    '''
    faces=detector.detect_faces(rgbFrame)

    return faces

def drawFaces(frame, facesBB):
    for face in facesBB:
        ''' extract the face '''
        x1,y1,w,h =face['box']
        x1,y1 =abs(x1), abs(y1) 
        x1,y1,x2,y2=x1,y1,x1+w,y1+h
        cv.rectangle(frame, (x1,y1),(x2,y2),(0,250,100), 2)

    return frame


def saveFaces(frame, facesBB, outDirname=None, faceSize=(640,480)):
    """
       Input: frame is numpy arraycontaining faces. And faceBB = a dictionary containing face information
       Output: none
       Task: crop faces and faces 
       outDirName : The directory for saving files
    """
    counter=1
    fileName = "counter.txt"
    if not os.path.isfile(fileName):
        f=open(fileName,"w")
        f.write(str(1))
        f.close()
    else:
        fhandle = open(fileName,'r')
        counter= fhandle.read().strip()
        print(f'\n\nafter reading the values of file ',counter)
        fhandle.close()

    type(counter)
    counter=int(counter)
    if not outDirname is None:
        if not os.path.exists(outDirname):
            os.makedirs(outDirname)
    
    for face in facesBB:
        ''' extract the face '''
        x1,y1,w,h =face['box']
        x1,y1 =abs(x1), abs(y1) 
        x1,y1,x2,y2=x1,y1,x1+w,y1+h
        aface=frame[y1:y2,x1:x2].copy()
        aface = cv.resize(aface,faceSize)
        print(f'{outDirname}/face_no_{counter}.jpg')
        cv.imwrite(f'{outDirname}/face_no_{counter}.jpg', aface)
    
        print('face is saved succussfully')
        counter+=1
    with open(fileName,'w') as f:
        f.write(str(counter+1))



if __name__=='__main__':

    vstream = cv.VideoCapture(0)
    while True:
        ok, frame = vstream.read()
        faceBB = faceDetector(frame)
        """
             save faces 
        """
        
        saveFaces(frame,faceBB,outDirname="./data")
   
        """
           draw faces on a frame 
           
        """
        frameM = drawFaces(frame, faceBB)
        cv.imshow("Faces", frameM)
        if cv.waitKey(1) & 0xFF==27:
            break




