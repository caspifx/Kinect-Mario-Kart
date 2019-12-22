import numpy as np
import cv2
import render_image
import pyautogui
import threading
import time

sdThresh = 20
font = cv2.FONT_HERSHEY_SIMPLEX


def distMap(frame1, frame2):
    """outputs pythagorean distance between two frames"""
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    dist = np.uint8(norm32*255)
    return dist


def always_forward():
    def press_gas(rate):
        while True:
            pyautogui.keyDown('Up')
            time.sleep(rate)
            pyautogui.keyUp('Up')
    print('Controlling Game In 3 Seconds...')
    time.sleep(3)
    thread = threading.Thread(target=press_gas, args=(0.5,))
    thread.start()


def turn_right():
    def press_right(rate):
        pyautogui.keyDown('Right')
        time.sleep(rate)
        pyautogui.keyUp('Right')

    thread = threading.Thread(target=press_right, args=(0.2,))
    thread.start()


def turn_left():
    def press_left(rate):
        pyautogui.keyDown('Left')
        time.sleep(rate)
        pyautogui.keyUp('Left')

    thread = threading.Thread(target=press_left, args=(0.2,))
    thread.start()


def stay():
    # pyautogui.keyUp('Right')
    # pyautogui.keyUp('Left')
    pass



def handle_movement(states):
    right = states['right']
    left = states['left']
    center = states['center']
    if right and not left:
        turn_right()
    if left and not right:
        turn_left()
    if center and not left and not right:
        stay()

cv2.namedWindow('frame')


#capture video stream from camera source. 0 refers to first camera, 1 referes to 2nd and so on.
cap = cv2.VideoCapture(0)
ret, frame1 = cap.read()
frame1s = render_image.slice(frame1, 3)
ret2, frame2 = cap.read()
initial_frames = [(frame1s), (render_image.slice(frame2, 3))]
facecount = 0

always_forward()

while(True):
    _, frame3 = cap.read()
    frames = render_image.slice(frame3, 3)
    frame_index = 0
    states = {'right': False, 'center': False, 'left': False}
    for frame in frames:
        frame1 = initial_frames[0][frame_index]
        frame2 = initial_frames[1][frame_index]
        rows, cols, _ = np.shape(frame)
        dist = distMap(frame1, frame)

        frame1 = frame2
        frame2 = frame

        # apply Gaussian smoothing
        mod = cv2.GaussianBlur(dist, (9,9), 0)

        # apply thresholding
        _, thresh = cv2.threshold(mod, 100, 255, 0)

        # calculate st dev test
        _, stDev = cv2.meanStdDev(mod)

        cv2.putText(frame2, 'SPLIT', (70, 70), font, 1.5, (255, 255, 255), 1, cv2.LINE_AA)
        if stDev > sdThresh:
            cv2.putText(frame2, 'SPLIT', (70, 70), font, 1.5, (100, 0, 0), 1, cv2.LINE_AA)
            if frame_index == 0:
                states['right'] = True
            if frame_index == 1:
                states['center'] = True
            if frame_index == 2:
                states['left'] = True
                #TODO: Face Detection 2
        handle_movement(states)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        frame_index += 1
    # cv2.imshow('dist', frame3)
    #     # dist = distMap(frame1, frame3)
    #     # mod = cv2.GaussianBlur(dist, (9, 9), 0)
    #     # cv2.imshow('dist', mod)
    height, width = frame3.shape[:2]
    cv2.line(frame3, (int(width / 3), 0), (int(width / 3), height), (0, 0, 0), 1)
    cv2.line(frame3, (int(width / 3) * 2, 0), (int(width / 3) * 2, height), (0, 0, 0), 1)
    cv2.imshow('frame', frame3)

cap.release()
cv2.destroyAllWindows()
