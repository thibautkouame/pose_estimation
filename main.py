import cv2
import time 
import mediapipe as mp
import numpy as np
from djitellopy import tello
import signal
import argparse

# use to estimate pose estimage using Tello drone camera
#me = tello.Tello()
#me.connect()
#print(me.get_battery())
#me.streamon()
#time.sleep(10)
#me.takeoff()

prevframe = 0
newFrame = 0



# initialize mediapipe pose solution / mise en place de la bibliothèque mediapipe 
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

#imageR = cv2.imread('ressources/video_2.mp4')

# take video input for pose detection
# you can put here video of your choice
cap = cv2.VideoCapture('ressources/dance.mp4')

# take live camera  input for pose detection
#cap = cv2.VideoCapture(0)

# read each frame/image from capture object
while True:
    #me.connect()
    #img = me.get_frame_read().frame
    ret, img = cap.read()
    # resize image/frame so we can accommodate it on our screen
    img = cv2.resize(img, (600, 400))
    img_tr = cv2.resize(img, (600, 400))
    font = cv2.FONT_HERSHEY_PLAIN
    newFrame = time.time()
    fps = 1/(newFrame-prevframe)
    prevframe = newFrame
    fps= str(fps)
    #me.send_rc_control(0,0,0,0)
 
    # do Pose detection / cette session permet d'estimer la pose depuis la video
    results = pose.process(img)
    # draw the detected pose on original video/ live stream
    mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                           mp_draw.DrawingSpec((0,255, 255), 2, 2),
                           mp_draw.DrawingSpec((255, 0, 255), 2, 1)
          
                      )
    # write text on video / le text sur la video
    cv2.putText(img, 'Video source', (10,30), font, 1, (255, 0, 0), 1, cv2.LINE_4)
    
    # Display pose on original video/live stream
    cv2.imshow("Video Source", img)

    # Extract and draw pose on plain white image
    h, w, c = img.shape   # get shape of original frame
    opImg = np.zeros([h, w, c])  # create blank image with original frame size
    opImg.fill(0)  # set white background. put 0 if you want to make it black

    # draw extracted pose on black white image
    mp_draw.draw_landmarks(opImg, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                           mp_draw.DrawingSpec((255, 0, 0), 2, 2),
                           mp_draw.DrawingSpec((255, 0, 255), 2, 2)
                           )
    
    cv2.putText(opImg, 'Pose Estimation', (450,30), font, 1, (0,255, 255), 1, cv2.LINE_4)
    cv2.putText(opImg, 'Thibaut Kouame', (10,30), font, 1, (136, 8, 8), 1)
    cv2.putText(opImg, 'project', (10,50), font, 1, (136, 8, 8), 1, cv2.LINE_8)
    cv2.putText(opImg, 'fps:'+fps, (10,70), font, 1, (255, 0, 0), 1, cv2.LINE_4)
        
    # display extracted pose on blank images / netoie la video avec un arrière noir
    cv2.imshow("Pose Estimation", opImg)    
    
    cv2.imshow("Video Source", img)

    # print all landmarks
    #print(results.pose_landmarks)

    # pour quitter la video appuyé sur la tache q
    if cv2.waitKey(1)==ord('q'):
        #me.streamoff()
        #me.land()
        break
#cap.release()
cv2.destroyAllWindows()

# this code is also written in order to use Dji Tello camera to estimate pose, if you do not understand somthing feel free to wrtie me at : thibautkouame10@gmail.com
# ce code est aussi de tel sorte a pouvoir utilsé la camera du drone Dji Tello pour estimer la pose, si vous ne comprenez pas quelque chose, ecrivez moi à : thibautkouame10@gmail.com