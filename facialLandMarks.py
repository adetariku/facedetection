"""
   This program detects FAcial Landmarks and displays it on the face

   USing the mediapipe package 


"""

import time
import cv2 as cv 
from mediapipe import solutions

mediaFaceMesh = solutions.face_mesh
face_mesh = mediaFaceMesh.FaceMesh(max_num_faces=5)
drawArgs = solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=1)
mediaDraw = solutions.drawing_utils
vstream =cv.VideoCapture(0)# connecting to the default webcam
count=0.0
period=0.0
while vstream.isOpened():
    startTime = time.perf_counter()
    '''READ FRAME BY FRAME '''
    _, frame= vstream.read()
    '''CONVERT IMAGE COLOR SPACE FROM BGR TO RGB'''
    imgRGB = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    ''' CREATE INSTANCE OF THE MESH CLASS '''
    mesh=face_mesh.process(imgRGB)

    if mesh.multi_face_landmarks:
        for faceLM in mesh.multi_face_landmarks:
            mediaDraw.draw_landmarks(frame, faceLM, mediaFaceMesh.FACE_CONNECTIONS, drawArgs, drawArgs)

    count+=1.0
    period+= (time.perf_counter()-startTime)
    fps = round(count/period, 2)
    cv.putText(frame, f'FPS : {fps}', (30,40),cv.FONT_HERSHEY_PLAIN, 2,(20,200,30), 2)
    cv.imshow('landmarks', frame)
    if cv.waitKey(1) & 0xFF==27:
        break







